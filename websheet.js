
function websheet(textarea_id, fragments) {
  function compare(pos1, pos2) {
    // 1: pos1 later; -1: pos1 earlier; 0: identical
    if (pos1.line < pos2.line) return -1;
    if (pos1.line > pos2.line) return 1;
    if (pos1.ch < pos2.ch) return -1;
    if (pos1.ch > pos2.ch) return 1;
    return 0;
  }
  
  function contains_strictly(int1, int2) {
    return (compare(int1.from, int2.from) < 0)
      && (compare(int2.to, int1.to) < 0);
  }

  function skip_space(range) {
    var pos = range.from;
    // skip past the first, ineditable, character
    if (cm.getLine(pos.line).length == pos.ch) 
      pos = {line: pos.line+1, ch: 0};
    else
      pos.ch++;
    // skip past any spaces that immediately follow
    // but not out of the editable range
    var theline = cm.getLine(pos.line);
    while (theline.charAt(pos.ch)==' ') {
      var newpos = {line: pos.line, ch: pos.ch+1};
      if (compare(newpos, range.to) == 0) return pos;
      pos = newpos;
    }
    return pos;
  }

  // tab jumps you to the start of the next input field
  function next_blank(reverse) {
    if (typeof reverse === 'undefined') reverse = false;
    var pos = cm.getCursor();
    var first = null;
    var tgt = null;
    for (var i=(reverse ? editable.length-1 : 0); i>=0 && i<editable.length; i += (reverse ? -1 : 1)) {
      var ustart = skip_space(editable[i].find());
      if (compare(ustart, pos) == (reverse ? -1 : 1)) {
        cm.setCursor(ustart);
        return;
      }
    }
    cm.setCursor(skip_space(editable[reverse ? editable.length-1 : 0].find()));
  }

  var keyMap = {PageDown: function() {next_blank(false); return true;},
                PageUp: function() {next_blank(true); return true;},
                Tab: function() {
                  var lo = cm.getCursor("start").line;
                  var hi = cm.getCursor("end").line;
                  for (var i = lo; i <= hi; i++)
                    cm.indentLine(i, "smart");
                  cm.setCursor(cm.getCursor("end"));
                }
               };

  var cm = CodeMirror.fromTextArea(document.getElementById(textarea_id), {
    mode: "text/x-java",
    theme: "neat", tabSize: 3, indentUnit: 3,
    lineNumbers: true,
    styleSelectedText: true,
    viewportMargin: Infinity,
    extraKeys: keyMap,
    matchBrackets: true
  });

  cm.setValue(fragments.join(""));

  var inline = new Array();
  var block = new Array();
  var editable = new Array();

  var line = 0;
  var ch = 0;
  for (var i=0; i<fragments.length; i++) {
    var oldline = line;
    var oldch = ch;
    var lastNL = fragments[i].lastIndexOf("\n");

    if (lastNL == -1) {
      ch += fragments[i].length;
    }
    else {
      for (var j=0; j<fragments[i].length; j++)
        if (fragments[i].charAt(j)=='\n') line++;
      ch = fragments[i].length - lastNL - 1;
    }

    if (i%2 == 1) { // alternate chunks are for user input
      if (fragments[i].length < 2) {
        cm.toTextArea();
        var errmsg = "Error: fragment " + i + " is too short";
        console.log(errmsg, fragments);
        return;
      }
      
      // check for errors
      if (lastNL != -1) {
        if (fragments[i].charAt(0)!='\n'
            || fragments[i].charAt(fragments[i].length-1)!='\n') {
          cm.toTextArea();
          var errmsg = "Error: fragment " + i + " contains a newline, must start and end with a newline";
          console.log(errmsg, fragments);
          return;
        }
      }
      else {
        if (fragments[i].charAt(0)!=' '
            || fragments[i].charAt(fragments[i].length-1)!=' ') {
          cm.toTextArea();
          var errmsg = "Error: fragment " + i + " contains no newline, must start and end with a space";
          console.log(errmsg, fragments);
          return;
        }
      }
      
      var marker = cm.markText(
        {line: oldline, ch: oldch},
        {line: line, ch: ch},
        {className: lastNL==-1?"inline":"block"});
      editable.push(marker);
      if (lastNL==-1) { // inline
        inline.push(marker);
        // mark half-char widths
        cm.markText({line: oldline, ch: oldch},
                    {line: oldline, ch: oldch+1},
                    {className: "inlineL"});
        cm.markText({line: line, ch: ch-1},
                    {line: line, ch: ch},
                    {className: "inlineR"});
      }
      else { // block
        block.push(marker);
        for (var ell=oldline+1; ell<line; ell++)
          cm.indentLine(ell, "smart");
      }
    }
  }

  var retval;

  var override = false;
  
  // this is better than readOnly since it works when you surround read-only text
  // and try to change the whole selection
  cm.on("beforeChange", function(cm, change) {
	  
    if (override) return;
    if (retval.readOnly) {change.cancel(); return;}

    // cancel newlines in inline regions
    if (change.text.length > 1) // array of lines; is there a newline?
      for (var i=0; i<inline.length; i++) {
        var inlinerange = inline[i].find();
        if (contains_strictly(inlinerange, change)) {
          change.cancel();
          return;
        }
      }

    // only allow changes within editable regions
    for (var i=0; i<editable.length; i++) {
      var fixedrange = editable[i].find();
      if (contains_strictly(fixedrange, change)) return;
      // the editor often replaces '\n...' by '\n...', allow it
      if (compare(fixedrange.from, change.from)==0
          && compare(fixedrange.to, change.to)<0
          && cm.getLine(fixedrange.from.line).charAt(fixedrange.ch.from.ch)=='\n'
          && change.test.length > 1 && change[0] == '') // first char is '\n'
        return;
    }

    change.cancel();
  });
  
  cm.on("renderLine", function(cm, line, elt) {
    var ln = cm.getLineNumber(line);
    for (var i=0; i<block.length; i++) {
      var mrange = block[i].find();
      if (mrange && mrange.from.line < ln && mrange.to.line > ln) $(elt).addClass("block");
    }
  });
  
  var hhandle = null;
  cm.on("change", function() {
    if (hhandle != null) testWS.cm.removeLineClass(hhandle, "wrapper", "tempAlert");
    hhandle = null;
  });

  cm.refresh();

  var setUserAreas = function(data) {
      for (var i=0; i<data.length; i++) {
	  var f = editable[i].find().from;
	  var t = editable[i].find().to;
	  if (data[i].indexOf("\n") != -1) {
	      f = {line: f.line+1, ch: 0};
	      t = {line: t.line-1, ch: cm.getLine(t.line-1).length};
	  }
	  else {
	      f = {line: f.line, ch: f.ch+1};
	      t = {line: t.line, ch: t.ch-1};
	  }
	  cm.replaceRange(data[i].substring(1, data[i].length-1), f, t);
      }
  }

  retval = {
    getUserCode: function() {
      var result = new Array();
      for (var i=0; i<editable.length; i++) {
        var range = editable[i].find();
        result.push(cm.getRange(range.from, range.to));
      }
      return result;
    },
    getUserCodeAndLocations: function() {
      var result = new Array();
      for (var i=0; i<editable.length; i++) {
        var range = editable[i].find();
        result.push({
          code: cm.getRange(range.from, range.to),
          // add one since what the gutter displays is one more than the line index
          from: {line: range.from.line+1, ch: range.from.ch},
          to: {line: range.to.line+1, ch: range.to.ch}
        });
      }
      return result;      
    },
    tempAlert: function(line) {
      // subtract one since what the gutter displays is one less than the line index
      if (hhandle != null) testWS.cm.removeLineClass(hhandle, "wrapper", "tempAlert");
      hhandle = cm.addLineClass(line-1, "wrapper", "tempAlert");
    },
    readOnly: false,
    cm: cm,
    setUserAreas: setUserAreas
  };
  return retval;  
}
