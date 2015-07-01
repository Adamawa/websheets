<?php // security stuff first
include_once('auth.php');

if (!array_key_exists("folder", $_GET)) $_GET['folder'] = '';

if (1 != preg_match('~^(([\\w-]+/)*[\\w-]+)?$~', $_GET['folder']))
  die('Illegal characters in requested folder name.'); 
?>
<html>
<head>
   <title>Websheets</title>
   <link rel="icon" type="image/png" href="favicon.png">
   <script type="text/javascript" src="jquery.min.js"></script>
   <script type="text/javascript" src="CodeMirror/lib/codemirror.js"></script>
   <script type="text/javascript" src="CodeMirror/mode/clike/clike.js"></script>
   <script type="text/javascript"
    src="CodeMirror/addon/selection/mark-selection.js"></script>
   <script type="text/javascript" 
    src="CodeMirror/addon/edit/matchbrackets.js"></script>
   <script type="text/javascript">
   "use strict";
   </script>
   <script type="text/javascript" src="websheets.js"></script>
   <script type="text/javascript" src="index.js"></script>
   <script type="text/x-mathjax-config"> 
      MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]} });
   </script>
   <script type="text/javascript" 
    src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
   </script>

   <link rel="stylesheet" href="CodeMirror/lib/codemirror.css">
   <link rel="stylesheet" href="CodeMirror/theme/neat.css">
   <link rel="stylesheet" href="websheets.css">
   <link rel="stylesheet" href="index.css">
  
   <link href='http://fonts.googleapis.com/css?family=Source+Code+Pro:400,700'
    rel='stylesheet' type='text/css'>
   <script type='text/javascript'> 
   websheets.urlbase = "./";
   websheets.require_login = true;
   websheets.current_folder = <?php echo json_encode($_GET['folder']); ?>;
   websheets.authinfo = <?php echo json_encode($GLOBALS['WS_AUTHINFO']); ?>;
   websheets.sheets = <?php echo passthru("./Websheet.py list ".$_GET['folder']); ?>;
   websheets.subfolders = <?php echo passthru("./Websheet.py list-folders ".$_GET['folder']); ?>;
   </script>
</head>
<body>
 <div id="page">
  <div class="menu-bar noprint">
    <a href="mailto:daveagp@gmail.com">Report feedback</a>. 
    <a href="https://github.com/daveagp/websheets">Websheets is open-source</a>.    
   
    <div class='selectdiv'>
    <span class='selectspan'>
    Select an exercise:
    <select name="selectSheet" id="selectSheet">
    </select>
    </span>
    <span id="subfoldering" style='margin-left:30px; display: none;'>
        Current folder: <span id="currfolder"></span>. 
        <button name="enterSubfolder" id="enterSubfolder">Change folder:</button>
    <select name="selectSubfolder" id="selectSubfolder">
    </select>
    </span>
    </div>
    
  </div> <!-- menu-bar -->

  <div id="container">
  </div>

 </div> <!-- page -->
</body>
</html>
