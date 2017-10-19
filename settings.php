<?php require_once('auth.php'); ?>
<html>
<head>
<title>Websheets Settings</title>
</head>
<body>
<div id='info'><?php echo $GLOBALS['WS_AUTHINFO']['info_span']; ?> </div>
<p>
<?php
global $WS_AUTHINFO;
if (!$WS_AUTHINFO['logged_in']) {
  echo "You have to log in to change your settings.";
 }
 else {
  require_once('edit.php');
  $_REQUEST['action'] = 'settings';
  $editout = run_edit_py();
  //  echo $editout;
  $result = json_decode($editout, true);
  if (is_string($result))
    echo $result;
  else {
 ?>
<p>
    <form action='./settings.php' method='post'>
          Your instructor can see which problems you have completed, and when.
          Instructor (enter their Websheets account email address): 
          <input type='text' name='instructor' value='<?php echo $result['settings']['instructor']; ?>' >
          
          <br/>
          Your group/class/extra_info:
          <input type='text' name='group' value='<?php echo $result['settings']['group']; ?>' >
    
    <br/>
    <input type="submit"  name="saving" value="Save settings">
    </form>
<?php if( isset($_REQUEST["saving"]) ) echo "<b>Saved</b>"; ?>
<p>

<?php
  }

 }
?>
</body>
</html>
