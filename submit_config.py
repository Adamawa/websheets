import socket, os
from subprocess import Popen, PIPE
from Websheet import record

def execute(command, the_stdin):
    proc = Popen(command.split(" "), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    result = proc.communicate(input = the_stdin)
    return record(stdout = result[0].decode("UTF-8"),
                  stderr = result[1].decode("UTF-8"),
                  returncode = proc.returncode)
    

if socket.gethostname().endswith("uwaterloo.ca"):
    jail = "/home/cscircles/dev_java_jail/"
    scratch_dir = jail + "scratch/"
    javac = jail + "java/bin/javac -J-Xmx128M "
    java = "/java/bin/java -Xmx128M "
    safeexec = "/home/cscircles/dev/safeexec/safeexec"
    safeexec_args = " --chroot_dir "+ jail +" --exec_dir /scratch --env_vars '' --nproc 50 --mem 500000 --nfile 30 --clock 2 --exec "
    
    def run_javac(command, the_stdin = ""):
        os.chdir(scratch_dir)
        return execute(javac + command, the_stdin)

    def run_java(command, the_stdin = ""):
        return execute(safeexec + safeexec_args + java + command, the_stdin)  

elif socket.gethostname().endswith("princeton.edu"):
    javac = "javac -J-Xmx128M "
    java = "/usr/bin/java -Xmx128M "

    scratch_dir = "/n/fs/htdocs/dp6/scratch/"

    def run_javac(command, the_stdin = ""):
        os.chdir(scratch_dir)
        return execute(javac + command, the_stdin)

    def run_java(command, the_stdin = ""):
        os.chdir( "/n/fs/htdocs/dp6/")
        if the_stdin != "":
            raise Exception('Cannot handle stdin in run_java yet')
        cmd = "sandbox -M -i safeexec/safeexec -i scratch /usr/bin/python -u -S"

        input = """
import os, resource, sys
from subprocess import Popen, PIPE
cmd = 'safeexec/safeexec --exec_dir {scratch} --nproc 50 --mem 4000000 --clock 3 --nfile 30 --exec {java}{command}'
proc = Popen(cmd.split(' '), stdin=PIPE, stdout=PIPE, stderr=PIPE)
result = proc.communicate(input = '')
sys.stdout.write(result[0])
sys.stderr.write(result[1])
sys.exit(proc.returncode)
""".format(command=command, scratch=scratch_dir, java=java).encode('ASCII')
            
        return execute(cmd, input)
