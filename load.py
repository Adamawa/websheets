#!/usr/bin/python3

if __name__ == "__main__":
  import sys
  from Websheet import Websheet
  student = sys.argv[2]
  classname = Websheet.from_filesystem(sys.argv[1]).classname

  import config, json
  websheet = Websheet.from_filesystem(classname)
  print(json.dumps({"template_code":websheet.get_json_template(),
                    "description":websheet.description,
                    "user_code": config.load_submission(student, classname)
                    }))
