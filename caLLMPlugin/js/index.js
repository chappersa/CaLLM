jQuery(document).ready(function($) {
   
    makeInitialCall();


    jQuery("#textInput").keypress(function(e) {
        if (e.which == 13) {
			if(jQuery("#textInput").val() != ""){
				getResponse();	
			}
        }
    });
   
    jQuery("#sendBtn").click(function() {
        	if(jQuery("#textInput").val() != ""){
				getResponse();	
			}
    });

    jQuery("#addToRepositoryBtn").click(function() {
        authenticateAndAdd();
    });
});


//Wakes up CaLLM
function makeInitialCall() {
	jQuery.get("/wp-content/plugins/caLLMPlugin/query.php", function() {
		console.log("CaLLM awake");
	});
}

//Gets the response from the back end using the user input
function getResponse() {
	var rawText = jQuery("#textInput").val();
	var userHtml = '<p class="userText"><span>' + rawText + "</span></p>";
	var thinkingHtml = '<p class="thinkingText"><span> Let me think... </span></p>';
	jQuery("#textInput").val("");
	jQuery("#chatbox").append(userHtml);
	jQuery("#chatbox").append(thinkingHtml);
	document.getElementById("userInput");
	jQuery.get("/wp-content/plugins/caLLMPlugin/query.php", { msg: rawText }).done(function (data) {
		var botHtml = '<p class="botText"><span>' + data + "</span></p>";
		jQuery(".thinkingText").remove();
		jQuery("#chatbox").append(botHtml);
		document.getElementById("userInput");
	});
}

//Authenticate the user and then add the information provided to the repository
function authenticateAndAdd() {
		swal({
				  
				  title:"Enter Admin Password",
				  content: {
					element: "input",
					attributes: {
						placeholder: "Type your admin password",
						type: "password",
						},
				  },
				  buttons:{
					  cancel: true,
					  confirm: true,
				  },
				})
				.then(password => {
				if(password){
						jQuery.get("/wp-content/plugins/caLLMPlugin/query.php", { pas: password}).done(function(authenticated) {
					if (authenticated == "correct") {

						swal({
							title:"Correct Password",
							icon: "success",
						  text: "Please think carefully about the resources you are adding to CaLLM's repository as it will influence the answers he provides. Provide either a file path to the pdf or wikipedia url to the data you want to add.",
						   content: {
							element: "input",
							attributes: {
								placeholder: "Path to pdf or Wikipedia url",
								},
						  },
						   buttons: {
							cancel: true,
							confirm: true,
						   }
						})
						.then(url => {
							if(url){
								jQuery.get("/wp-content/plugins/caLLMPlugin/query.php", { url: url })
								.done(function(data) {
								swal("Adding to the Repository", data, "info");
							});	
							}
						})

					} else {
						swal("Incorrect password","Please try again","error");
					}
				})
					.fail(function() {
					swal("Error", "An error occurred while authenticating","error");
				});
						}
		})

	}																				
																					
																					





