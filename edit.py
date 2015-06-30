#!/usr/bin/python3

import sys, json, config, re

if __name__ == "__main__":
  db = config.connect()
  cursor = db.cursor()

  # should pass message which is a string
  def internal_error(message):
    db.commit()
    cursor.close()
    db.close()
    print(json.dumps(message))
    sys.exit(0)

  # should pass response which is an object
  def done(**response):
    db.commit()
    cursor.close()
    db.close()
    print(json.dumps(response))
    sys.exit(0)

  request = json.loads("".join(sys.stdin))

  authinfo = request['authinfo']
  if not authinfo["logged_in"]:
    internal_error("Only logged-in users can edit")
  problem = request['problem']
  action = request['action']
  
  def owner(slug):
    # really should be done with %s but ok since we sanitize
    cursor.execute(
      "select author, action from ws_sheets " +
      "WHERE problem = '"+slug+"' AND 1 ORDER BY ID DESC LIMIT 1;")
    result = "false"
    for row in cursor:
      author = row[0]
      action = row[1]
      if action == 'delete': return None
      return author
    return None

  def definition(slug, preview=False):
    cursor.execute(
      "select definition from ws_sheets " +
      "WHERE problem = '"+slug+"' AND action != 'preview' ORDER BY ID DESC LIMIT 1;")
    for row in cursor:
      return row[0]
    internal_error('Whoa, where did that row go?')

  def valid(slug):
    return re.match(r"^([\w-]+/)*[\w-]+$", slug)

  def canedit(slug):
    return owner(slug) in [None, authinfo['username']]
        
  def canread(slug):
    myowner = owner(slug)
    if myowner is None: return False
    if myowner == authinfo['username']: return True
    # ignoring previews, get the latest version
    cursor.execute(
      "select author, action, sharing from ws_sheets " +
      "WHERE problem = '"+slug+"' AND action != 'preview' ORDER BY ID DESC LIMIT 1;")
    result = "false"
    for row in cursor:
      author = row[0]
      action = row[1]
      sharing = row[2]
      return sharing.startswith('open')
    internal_error('Whoa, where did that row go?')

  if not valid(problem):
    if (action == 'load'):
      done(success=False, message="Requested name does not have valid format: <tt>" + problem + "</tt>")
    else:
      internal_error("Does not have valid format: " + problem)
    
  if (action in ['preview', 'save', 'delete']):
    if not canedit(problem):
      internal_error("You don't have edit permissions for " + problem)
    if action == 'delete':
      sharing = None
      definition = None
    else:
      definition = json.loads(request['definition'])
      sharing = 'open-nosol'
      if 'sharing' in definition:
        sharing = definition['sharing']
    # add a row
    cursor.execute("insert into ws_sheets (author, problem, definition, action, sharing)" +
                   " VALUES (%s, %s, %s, %s, %s)",
                   (authinfo['username'], problem, request['definition'], action, sharing))
    done(success=True, message=action + " of " + problem + " successful.")
      
  if (action in ['rename', 'copy']):
    if action == 'copy' and not canread(problem):
      internal_error("You don't have read permissions for " + problem)
    if action == 'rename' and not canedit(problem):
      internal_error("You don't have edit permissions for " + problem)
    newname = request['newname']
    if not valid(newname):
      done(success=False, message="New name does not have valid format: " + newname)
    if not canedit(newname):
      done(success=False, message="You are not allowed to edit: " + newname)

    definition = json.loads(request['definition'])
    sharing = 'open-nosol'
    if 'sharing' in definition:
      sharing = definition['sharing']

    cursor.execute("insert into ws_sheets (author, problem, definition, action, sharing)" +
                   " VALUES (%s, %s, %s, %s, %s)",
                   (authinfo['username'], newname, request['definition'], 'save', sharing))

    if action == 'rename':      
      cursor.execute("insert into ws_sheets (author, problem, action)" +
                     " VALUES (%s, %s, %s, %s, %s)",
                     (authinfo['username'], problem, 'delete'))
      
    done(success=True, message=action + " of " + problem + " to " + newname + " successful.")

  if action == 'load':
    myowner = owner(problem)
    # if it doesn't exist, everything is good
    if myowner == None:
      done(success=True, message="Loaded " + problem, new=True, canedit=True)
    # it exists
    if not canread(problem):
      done(success=False, message="You do not have read permissions for: " + problem)
    done(success=True, message="Loaded " + problem, new=False, canedit=myowner == authinfo['username'],
          definition= definition(problem))
      
  internal_error('Unknown action ' + action)
