function makeInitialCall() {
	jQuery.get("/wp-content/plugins/caLLMPlugin/query.php", function() {
		console.log("CaLLM awake");
	});
}


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


    jQuery("#aboutCallmBtn").click(function() {
        callmInfo();
    });
});


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

function callmInfo(){
swal({
    title: "Who is CaLLM?",
    text: "CaLLM is a guide that is powered by the open-source Meta AI Llama2 large language model. This means he has been trained on their large dataset. However, to increase his specificity and knowledge base, I have used a Retrieval Augmentation Generation technique so that we can add to his repository of known information that he is able to call on when answering a question. This is all to try and provide some accuracy and precision in the use of LLMs, particularly around essential conversations including climate change and heritage. For more information on how this was achieved, check out my github.",
    buttons: {
        MoreOnLlama: {
            text: "Llama2",
            value: "more_on_llama",
        },
		confirm: true,
        dissReport: {
            text: "GitHub",
            value: "github"
        }
    }
}).then((value) => {
    switch (value) {
        case "more_on_llama":
             window.location.href = "https://llama.meta.com/llama2/";
            break;
        case "github":
            window.location.href = "https://github.com/chappersa/CaLLM";
            break;
        default:
            break;
    }
});
}
																				
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
																					
																					





