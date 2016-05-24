/**
 * Created by andrius on 16.4.27.
 */

$(document).ready(function(){
    var obj = $.parseJSON($("#gradesJSON").text());
    $("#gradesJSON").after("<div id='grades'></div>");
    for(var student in obj){ //loop through students
        var studentDiv = $("<div class='studentDiv' id='"+student+"'></div>").text(student); //add a div for each student
        studentDiv.append($("<hr>"));
        $("#grades").append(studentDiv);
        for(var problem in obj[student]){ //loop through problems
            var problemElem = $("<div class='problemDiv' id='"+student+"-"+obj[student][problem]['problemName']+"'></div>");
            var link = $("<a href='index.php?start="+obj[student][problem]['problemName']+"&student="+student+"'>"+obj[student][problem]['problemName']+"</a>");
            problemElem.append(link);
            problemElem.append("<br>");
            if(obj[student][problem]['passed']){
                problemElem.attr("class", "problemDiv passed");
                problemElem.append("Išspręsta: "+obj[student][problem]['passDate']+"<br>");
            }
            problemElem.append("Bandymų: "+obj[student][problem]['tries']+"<br>");
            problemElem.append("<span hidden>"+student+"</span>");

            studentDiv.append(problemElem);
        }
    }
});

$("#searchButton").on("click",function(){
    searchGrades();
});

$("#searchField").on("input", function(){
    searchGrades();
});
function searchGrades(){
    var string = $("#searchField").val();
    console.log("'"+string+"'");
    var grades = $("#grades");
    grades.children("div").hide("fast");
    var matchedStudents = grades.children("div:contains('"+string+"')"); //search through student names
    matchedStudents.stop(true,false); //remove from animation queue and do not jump to end
    matchedStudents.show("fast");
    matchedStudents.css("height",matchedStudents.outerHeight);
    grades.children("div").children("div").hide("fast");
    var matchedProblems = grades.children("div").children("div:contains('"+string+"')"); //search through problem divs
    matchedProblems.stop(true, false); //stop the animation again
    matchedProblems.show("fast");
}