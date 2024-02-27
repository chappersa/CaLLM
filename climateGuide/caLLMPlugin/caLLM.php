<?php
/**
 * Plugin Name: CaLLM
 */
 
// Load the TinyMCE plugin : editor_plugin.js (wp2.5)
add_filter( 'mce_external_plugins', 'chat_register_javascript' );

function chat_register_javascript( $plugin_array ) {
   $plugin_array['CaLLM'] = plugins_url( '/js/jquery.terminal.js',__FILE__ );
   return $plugin_array;
}

function CaLLM_shortcodes_init()
{
    function CaLLM_shortcode($atts = [], $content = null)
    {
        
        $o = <<<EOD
        <!DOCTYPE html>
        <html>
        <head>
            <title>CaLLM</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
			<link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Anton" />
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
            <style>
				* {
					box-sizing: border-box
				}
				body, html {
					height: 100%;
					margin: 0;
					font-family: Arial;
				}
				#chatbox {
				margin-left: auto;
				margin-right: auto;
				width: 85%;
				max-height: 350px;
				margin-top: 10px;
				overflow: auto;
			  }
			  #userInput {
				margin-left: auto;
				margin-right: auto;
				width: 40%;
				margin-top: 60px;
			  }
			  #textInput {
				border: none;
				width: 100%;
				border-bottom: 3px solid black;
				margin-bottom: 30px;
				font-size: 17px;
				background-color: #dbdbdb;
				font-family: monospace;
			  }
			  .userText {
				color: #404040;
				font-size: 17px;
				text-align: right;
				line-height: 30px;
				margin-bottom: 20px;
				font-family: monospace;
			  }
			  .userText span {
				background-color: #dbdbdb;
				padding: 10px;
				border-radius: 2px;
			  }
			  .botText {
				color: white;
				font-size: 17px;
				text-align: left;
				line-height: 30px;
				margin-bottom: 20px;
				font-family: monospace;
			  }
			  .botText span {
				background-color: #01726c;
				padding: 10px;
				border-radius: 2px;
			  }
			  .thinkingText {
				color: white;
				font-family: monospace;
				font-size: 17px;
				text-align: left;
				line-height: 30px;
				margin-bottom: 20px;
			  }
			  .thinkingText span {
				background-color: #01726c;
				padding: 10px;
				border-radius: 2px;
			  }
			  .boxed {
				margin-left: auto;
				margin-right: auto;
				width: 100%;
				max-height: 400px;
				margin-top: 60px;
				margin-bottom: 60px;
				border: 2px solid #e3815f;
				background-color: #f0f0f0;
			  }
			  h1 {
				font-family: 'Anton', sans-serif; 
				text-align: center;
				color: #e3815f;
				font-size: 60px;
        	}
			 h2 {
			 	font-family: 'Anton', sans-serif; 
				text-align: center;
				font-size: 20px;
				color: #404040;
        	}
      .buttonContainer {
            text-align: center;
            margin-top: 20px;
        }
        .button {
            padding: 10px 20px;
            background-color: #01726c;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            margin-right: 10px;
        }
        .button:last-child {
            margin-right: 0;
        }
        .button:hover {
            background-color: #015b52;
        }
    </style>
        </head>
        <body>
        <div>
			<h1 align="center">CaLLM</h1>
			<h2 align="center">Climate Action Large Language Model</h2>
                <div class="boxed">
                    <div>
                        <div id="chatbox">
                            <p class="botText">
                                <span>Hi! I'm CaLLM and I will be your climate action tour guide.</span>
                            </p>
                        </div>
                        <div id="userInput">
                            <input id="textInput" type="text" name="msg" placeholder="Ask CaLLM a Question">
                        </div>
                      </div>
                    <script>
                          function makeInitialCall() {
                            jQuery.get("http://vw-node04.cs.st-andrews.ac.uk:5002/", function() {
                                console.log("CaLLM awake");
                            });
                          }
                    
                        $(document).ready(function() {
                            makeInitialCall();
                        });

                        function getResponse() {
                            var rawText = jQuery("#textInput").val();
                            var userHtml = '<p class="userText"><span>' + rawText + "</span></p>";
                            var thinkingHtml = '<p class="thinkingText"><span> Let me think... </span></p>';
                            jQuery("#textInput").val("");
                            jQuery("#chatbox").append(userHtml);
                            jQuery("#chatbox").append(thinkingHtml);
                            document.getElementById("userInput");
                            jQuery.get"/wp-content/plugins/caLLM/query.php", { msg: rawText }).done(function (data) {
                                var botHtml = '<p class="botText"><span>' + data + "</span></p>";
                                $(".thinkingText").remove();
                                jQuery("#chatbox").append(botHtml);
                                document.getElementById("userInput");
                            });
                        }
                        jQuery("#textInput").keypress(function (e) {
                            if (e.which == 13) {
                                getResponse();
                            }
                        });
                    </script>
                </div>
                <div class="buttonContainer">
                  <!-- Buttons -->
                  <button class="button" id="logInBtn">Log In</button>
                  <button class="button" id="addToRepositoryBtn">Add To Repository</button>
              </div>
            </div>
        </body>
EOD;
        
        
    return $o;
    }
    
    add_shortcode('CaLLM', 'CaLLM_shortcode');
}


add_action('init', 'CaLLM_shortcodes_init');
