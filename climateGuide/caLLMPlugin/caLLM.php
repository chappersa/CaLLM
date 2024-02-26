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
                width: 40%;
                margin-top: 60px;
              }
              #userInput {
                margin-left: auto;
                margin-right: auto;
                width: 40%;
                margin-top: 60px;
              }
              #textInput {
                width: 90%;
                border: none;
                border-bottom: 3px solid black;
                font-family: monospace;
                font-size: 17px;
              }
              .userText {
                color: white;
                font-family: monospace;
                font-size: 17px;
                text-align: right;
                line-height: 30px;
              }
              .userText span {
                background-color: #808080;
                padding: 10px;
                border-radius: 2px;
              }
              .botText {
                color: white;
                font-family: monospace;
                font-size: 17px;
                text-align: left;
                line-height: 30px;
              }
              .botText span {
                background-color: #446b46;
                padding: 10px;
                border-radius: 2px;
              }
              .thinkingText {
                color: white;
                font-family: monospace;
                font-size: 17px;
                text-align: left;
                line-height: 30px;
              }
              .thinkingText span {
                background-color: #446b46;
                padding: 10px;
                border-radius: 2px;
              }
              .boxed {
                margin-left: auto;
                margin-right: auto;
                width: 78%;
                margin-top: 60px;
                border: 5px solid #446b46;
              }
            </style>
        </head>
        <body>
        <div>
                <h1 align="center"><b>CaLLM</b></h1>
                <h4 align="center"><b>Climate Action Large Language Model</b></h4>
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
                    
                        // Call the function when the page is loaded
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
                            document.getElementById("userInput").scrollIntoView({ block: "start", behavior: "smooth" });
                            jQuery.get("http://vw-node04.cs.st-andrews.ac.uk:5002/getResponse", { msg: rawText }).done(function (data) {
                                var botHtml = '<p class="botText"><span>' + data + "</span></p>";
                                $(".thinkingText").remove();
                                jQuery("#chatbox").append(botHtml);
                                document.getElementById("userInput").scrollIntoView({ block: "start", behavior: "smooth" });
                            });
                        }
                        jQuery("#textInput").keypress(function (e) {
                            if (e.which == 13) {
                                getResponse();
                            }
                        });
                    </script>
                </div>
            </div>
        </body>
EOD;
        
        
    return $o;
    }
    
    add_shortcode('CaLLM', 'CaLLM_shortcode');
}


add_action('init', 'CaLLM_shortcodes_init');
