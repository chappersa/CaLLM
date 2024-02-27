function getResponse() {
    var rawText = $("#textInput").val();
    var userHtml = '<p class="userText"><span>' + rawText + "</span></p>";
    var thinkingHtml = '<p class="thinkingText"><span> Let me think... </span></p>';
    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    $("#chatbox").append(thinkingHtml);
    document.getElementById("userInput").scrollIntoView({ block: "start", behavior: "smooth" });
    $.get("/getResponse", { msg: rawText }).done(function (data) {
        var botHtml = '<p class="botText"><span>' + data + "</span></p>";
        $(".thinkingText").remove();
        $("#chatbox").append(botHtml);
        document.getElementById("userInput").scrollIntoView({ block: "start", behavior: "smooth" });
    });
}

function authenticateAndAdd(){

    var password = prompt("Please enter the password:");

    // Check if the password is correct
    if (password === "password") {
        alert(addToRepo());
    } else {
        alert("Incorrect password. Please try again.");
    }
}


function addToRepo() {
    var url = prompt("Please provide the path the pdf or wikipedia URL you would like to add:");
    console.log(url)
    if (url) {
        $.get("/addToRepo", { msg: url }){
            
        };
    }

}

$("#textInput").keypress(function (e) {
    if (e.which == 13) {
        getResponse();
    }
});

$(document).ready(function () {
    $("#addToRepositoryBtn").click(function () {
        authenticateAndAdd();
    });
});
