import config, json, cgi, sys, Websheet, re, os
from utils import *

cfg = config.config_jo
jail = "/tmp/" # could use Config

void_functions = []
msgs = []
suffix = '.cs'

def execute(command, stdin):
  return config.execute(command, stdin, output_encoding='Latin-1')

def compile( jail, dir, slug, code, tag="reference|student", translate_line=None ):
   
    os.makedirs( jail + dir, 0o755, exist_ok=True);
    os.chdir(jail + dir)
    
    # SAVE to FILE
    with open(slug + ".cs", "w") as f:
      f.write(code)
      
    # remove previous compilation result (if such exists)
    if os.path.isfile( slug + '.exe' ):
        os.remove( slug + '.exe' )
    
    
    # COMPILE
    compiler_cmd = [cfg["cs_compiler"],   slug+".cs"]
    compiling = execute(compiler_cmd, "")
    
    def check_compile_err():
        
        if (compiling.stderr != "" or compiling.returncode != 0
        or not os.path.isfile(jail + dir + slug + suffix)):

            if 'student' in tag.lower():   #  humanreadable info for students
                errmsg = re.sub('(\.cs:)(\d+)(?!\d)',   # should  be adapted for C#
                       lambda m : m.group(1)+translate_line(m.group(2)),  
                       compiling.stderr)
                return errmsg
                
            else:     # for reference compilation - more detailed dump
                return  (
                    "Internal Error (Compiling %s)"%tag +
                    "cmd:"+pre(" ".join(compiler_cmd))+ # websheet.slug + suffix
                    "<br>stdout:"+pre(compiling.stdout)+
                    "<br>stderr:"+pre(compiling.stderr)+
                    "<br>retval:"+pre(str(compiling.returncode))
                    )                    
                    
    compiling.error  =  check_compile_err()
    return compiling
        
        
def run(slug, tag="reference|student" ):
    
    cmd = [cfg["safeexec-executable-abspath"]]
    #~ cmd += ["--chroot_dir", cfg["java_jail-abspath"]]
    #~ cmd += ["--exec_dir", "/" + refdir]
    cmd += ["--fsize", "5"]
    cmd += ["--nproc", "1"]
    cmd += ["--clock", "1"]
    cmd += ["--mem", "40000"]
    cmd += ["--exec", slug+'.exe']
    #~ cmd += args
    
    running = execute(cmd, "")

    def check_run_error():

        if running.returncode != 0 or not running.stderr.startswith("OK"):

            if 'student' in tag.lower():   #  for students -- humanreadable info 
                result = "<div>Crashed! "
                errmsg = running.stderr
                if "elapsed time:" in errmsg:
                  errmsg = errmsg[:errmsg.index("elapsed time:")]
                errmsg = errmsg.replace("Command terminated by signal (8: SIGFPE)",
                                        "Floating point exception")
                errmsg = errmsg.replace("Command terminated by signal (11: SIGSEGV)",
                                        "Segmentation fault (core dumped)")
                if errmsg != "":
                  result += "Error messages:" + pre(errmsg)
                if running.stdout != "":
                  result += "Produced this output:"+pre(running.stdout)
        #        result += "Return code:"+pre(str(running.returncode))
                result += "</div>"
                
                return result

                
            else:   # for reference -- more detailed
              return ("<div>Reference solution crashed!"+
                      "<br>stdout:"+pre(runref.stdout)  +
                      "stderr:"+pre(runref.stderr)      +
                      "val:"+pre(str(runref.returncode))+
                      "</div>" 
                      )
        
    running.error = check_run_error()
    
    return running
    
        

def grade(reference_solution, student_solution, translate_line, websheet):


    # build reference
    if not websheet.example:
        refdir = config.create_tempdir()
        refcompile = compile( jail, refdir, websheet.slug, reference_solution )
        if refcompile.error: return refcompile.error


    # build student
    studir = config.create_tempdir()
    stucompile = compile( jail, studir, websheet.slug, student_solution, 'student', translate_line )
    
    # result = output to user/student
    result = "<div>Compiling: saving your code as "+tt(websheet.slug+".cpp")
    result += " and calling "+tt(" ".join(["compile"] ))
    if stucompile.stdout!="":
      result += pre(stucompile.stdout)
    result += "</div>"

    if stucompile.error:
        result += "<div>Did not compile. Error message:"+pre(stucompile.error)+"</div>"
        return ("Syntax Error", result)

    # RUN TESTS
    if len(websheet.tests)==0:
      return ("Internal Error", "No tests defined!")

    def example_literal(cpptype):
      known = {"int":"0", "double":"0.0", "bool":"false", "char":"'x'", "string":'""', "char*": '(char*)NULL', "char[]": '""'}
      if cpptype in known: return known[cpptype]
      return None

    #~ for test in websheet.tests:
    for test in json.loads(websheet.tests):

        if websheet.lang=='C#': # normal test, calling main

            stdin = test.get('stdin', "")
            args = test.get('args', [])

            cmd = websheet.slug
            cmd =  " ".join([cmd] + args)

            result += "<div>Running " + tt("./" + cmd)
            if stdin:  result += " on input " + pre(stdin)
            else:      result += "&hellip;"
            result += "</div>"


        # RUN REFERENCE
        if not websheet.example:
            os.chdir(jail + refdir)      

            runref = run( websheet.slug, tag='reference')

            if runref.error:
                return ("Internal Error", runref.error)

        # RUN STUDENT
        os.chdir(jail + studir)      
        runstu = run( websheet.slug, tag='reference')
        
        if runstu.error:
            return ("Sandbox Limit", runstu.error)
      
  
        # TODO
        if websheet.example:
            result += "<div>Printed this output:"
            result += pre(runstu.stdout) + "</div>"
            continue

        stucanon = re.sub(' +$', '', runstu.stdout, flags=re.MULTILINE)
        refcanon = re.sub(' +$', '', runref.stdout, flags=re.MULTILINE)

        if (stucanon == refcanon 
          or stucanon == refcanon + "\n" and not refcanon.endswith("\n")):
            result += "<div>Passed! Printed this correct output:"
            result += pre(runstu.stdout, True) + "</div>"
        elif stucanon == refcanon + "\n":
            result += "<div>Failed! Printed this output:"
            result += pre(runstu.stdout, True)
            result += "which is almost correct but <i>you printed an extra newline at the end</i>.</div>"
            return ("Failed Tests", result)
        elif refcanon == stucanon + "\n":
            result += "<div>Failed! Printed this output:"
            result += pre(runstu.stdout, True)
            result += "which is almost correct but <i>you are missing a newline at the end</i>.</div>"
            return ("Failed Tests", result)
        else:
            result += "<div>Failed! Printed this incorrect output:"
            result += pre(runstu.stdout, True)
            result += "Expected this correct output instead:"
            result += pre(runref.stdout, True) + "</div>"
            return ("Failed Tests", result)

    if websheet.example:
      return ("Example", result)
    else:
      result += "<div>Passed all tests!</div>"
      return ("Passed", result)
      
if __name__ == "__main__":

    test_code = """
          using System; 
          public class HelloWorld{
             static public void Main (){
                Console.WriteLine ("Hello, Mono!");
             }
          }
        """

    def test_exec():
        # /usr/bin/mcs hello.cs
        #./safeexec --fsize 5  --nproc 1 --exec /usr/bin/mono tests/hello.exe
        jail = "/tmp/"
        studir = "stud/"
        slug = "hello"
        
        testcompile = compile( jail, studir, slug, test_code )
        print( get_attrs( testcompile ) )
        #~ print( testcompile.error )
        
        testrun = run( slug )
        print( get_attrs( testrun ) )
        

    #~ test_exec()


    def test_grade():
        #~ from submit import translate_line
        def translate_line(ss_lineno):
            ss_lineno = int(ss_lineno)
            if ss_lineno in ss_to_ui_linemap:
              return str(ss_to_ui_linemap[ss_lineno])
            else:
              return "???("+str(ss_lineno)+")" + "<!--" + json.dumps(ss_to_ui_linemap) + "-->"
            
        
        
        # cs/hello
        definition = {"description":"\nFix this program so that it outputs <pre>Hello, Mono!</pre>\nfollowed by a newline character.\n","sharing":"open","remarks":"Export of cs/hello by dz0@users.noreply.github.com\nCopied from problem cpp/var-expr/hello (author: daveagp@gmail.com)\n","lang":"C#","source_code":"using System;\n \npublic class HelloWorld\n{\n    static public void Main ()\n    {\n\\[\n        Console.WriteLine (\"Hello, Mono!\");\n\\show:\n        Console WriteLine Hello Mono\n]\\\n    }\n}\n","tests":"[\n   {}\n]\n","attempts_until_ref":"1"}
        #~ grade(reference_solution, student_solution, translate_line, websheet)
        
        websheet = Websheet.Websheet.from_name("cs/hello", False, 'anonymous')
        print("TESTS:", repr(websheet.tests) )
        
        reference_solution = websheet.get_reference_solution("reference")
        #~ reference_solution = test_code
        #~ student_solution = test_code.replace('!', '')
        student_solution = test_code
        
        result = grade(reference_solution, student_solution, translate_line, websheet)
        print( "RESULT:\n", result )
  
    test_grade()
        
