/**
 * Created by andrius on 16.4.27.
 */

$(document).ready(function(){
    var obj = $.parseJSON($("#gradesJSON").text());
    for(var student in obj){ //loop through students
        //console.log(student);
        var studentDiv = $("<div class='studentDiv' id='"+student+"'></div>").text(student); //add a div for each student
        $("#gradesJSON").after(studentDiv);
        for(var problem in obj[student]){ //loop through problems
            var problemElem = $("<div class='problemDiv' id='"+student+"-"+obj[student][problem]['problemName']+"'></div>");
            //console.log(obj[student][problem]);
            var link = $("<a href='index.php?start="+obj[student][problem]['problemName']+"&student="+student+"'>"+obj[student][problem]['problemName']+"</a>");
            problemElem.append("Problema: ");
            problemElem.append(link);
            problemElem.append("<br>");
            problemElem.append("Išspręsta: "+obj[student][problem]['passed']+" "+obj[student][problem]['passDate']+"<br>");
            problemElem.append("Bandymų: "+obj[student][problem]['tries']+"<br>");

            studentDiv.append(problemElem);
        }
    }
});