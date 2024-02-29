<?php
/**
 * Plugin Name: CaLLM
 * Plugin URI: https://github.com/chappersa/CaLLM
 * Description: Creates a personalised climate action chatbot.
 * Author: Alice Chapman
 * Version: 0.2.4
 * Author URI: https://github.com/chappersa
 */


// Load the TinyMCE plugin: editor_plugin.js (WordPress 2.5)
add_filter('mce_external_plugins', 'chat_register_javascript');

function chat_register_javascript($plugin_array)
{
    $plugin_array['CaLLM'] = plugins_url('/js/jquery.terminal.js', __FILE__);
    return $plugin_array;
}

function callm_enqueue_scripts()
{
    wp_enqueue_script('jquery');
	
    wp_enqueue_script('callm-terminal', plugins_url('/js/jquery.terminal.js', __FILE__), array('jquery'), '1.0', true);
	
	wp_enqueue_script('callm-index', plugins_url('/js/index.js', __FILE__), array('jquery'), '1.0', true);
	
	wp_enqueue_script('sweetalert', "https://unpkg.com/sweetalert/dist/sweetalert.min.js", array(), null, true);
	
	wp_enqueue_script('font-awesome', "https://kit.fontawesome.com/b122309121.js", array(), null, true);
	
    wp_enqueue_style('callm-style', plugins_url('/css/style.css', __FILE__));
	
	
}

function CaLLM_shortcodes_init()
{
    function CaLLM_shortcode($atts = [], $content = null)
    {
        $o = <<<EOD
		<head>
			<title>CaLLM</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
			<link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Anton" />
		</head>
        <div>
            <h1 class="title">CaLLM</h1>
            <h2 class="smallerTitle">Climate Action Large Language Model</h2>
            <div class="boxed">
                <div>
                    <div id="chatbox">
                        <p class="botText">
                            <span>Hi! I'm CaLLM and I will be your climate action tour guide. How can  I help?</span>
                        </p>
                    </div>
                    <div id="userInput">
                        <input id="textInput" type="text" name="msg" placeholder="Ask CaLLM a Question">
						<button id="sendBtn" class=sendBtn><i class='fas fa-arrow-circle-up'></i></button>
                    </div>
                </div>
            </div>
            <div class="buttonContainer">
                <button class="button" id="addToRepositoryBtn">Add To Repository</button>
				<button class="button" id="aboutCallmBtn">Who is CaLLM?</button>
            </div>
        </div>
EOD;

        return $o;
    }

    add_shortcode('CaLLM', 'CaLLM_shortcode');
}

// Hook scripts and styles enqueue function to 'wp_enqueue_scripts'
add_action('wp_enqueue_scripts', 'callm_enqueue_scripts');
// Hook shortcode registration function to 'init'
add_action('init', 'CaLLM_shortcodes_init');
