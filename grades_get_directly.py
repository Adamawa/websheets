import config

#~ authinfo = {}  
#~ authinfo['username'] = "jurgis.pralgauskis@gmail.com"


result = {}
for (student,) in config.get_rows(
  "select user from ws_settings " +
  ";"): # hack to get grades of all students
  #"WHERE value = %s AND keyname = 'instructor';", [authinfo['username']]):
  stuinfo = {}
  for (passed, time, problem) in config.get_rows(
    "SELECT passed, time, problem from ws_history where user = %s order by id asc;", [student]):
    if (problem not in stuinfo): prev = (False, 0)
    else: prev = stuinfo[problem]
    if not prev[0]: # if not yet passed
      if passed==1:
        curr = (True, prev[1]+1, time.strftime('%Y-%m-%d %H:%M:%S'))
      else:
        curr = (False, prev[1]+1)
      stuinfo[problem] = curr
  result[student] = stuinfo

from pprint import pprint
#pprint(result)

import json
with  open("grades.json", 'w') as f:
  f.write( json.dumps( result, indent=2 ))

