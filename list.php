<?php require_once('auth.php'); ?>
<html>
<head>
<script type='text/javascript' src='jquery.min.js'></script>
<script type='text/javascript'> 
  websheets.authinfo = <?php echo json_encode($GLOBALS['WS_AUTHINFO']); ?>;
</script>
<style>
table#list tr td:first-child {text-align:right;}
</style>
</head>
<body>
<div id='info'><?php echo $GLOBALS['WS_AUTHINFO']['info_span']; ?></div>
<table id='list'>
<?php 
if ($GLOBALS['WS_AUTHINFO']['logged_in']) {
  require_once('edit.php');
  $_REQUEST['action'] = 'list';
  $result = json_decode(run_edit_py(), true);
  $author = '';
  $readonly = false;
  if (is_string($result))
    echo $result;
  else {
    foreach ($result['problems'] as $probleminfo) {
      $name = $probleminfo[0];
      $sharing = $probleminfo[1];
      echo "<tr><td>$name</td><td><a href='editor.php?edit=$name'>Edit</a></td>";
      if ($sharing != 'draft') echo "<td><a href='./?start=$name'>Solve</a></td>";
      echo '</tr>';
    }
  }
}
?>
</table>
</body>
</html>