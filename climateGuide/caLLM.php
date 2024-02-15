<?php
function send_message_to_chatbot($message) {
    $api_url = ' '; 
    $response = wp_remote_post($api_url, array(
        'body' => json_encode(array('message' => $message)),
        'headers' => array('Content-Type' => 'application/json'),
    ));

    if (is_wp_error($response)) {
        return "Error communicating with the CaLLM.";
    }

    $body = wp_remote_retrieve_body($response);
    $data = json_decode($body, true);

    return $data['result'];
}

// Shortcode to display the chatbot form
function chatbot_shortcode() {
    ob_start(); ?>
    <form id="chatbot-form">
        <input type="text" id="chat-message" placeholder="Type your message">
        <button type="button" onclick="sendMessage()">Send</button>
    </form>
    <div id="chatbot-response"></div>
    <script>
        function sendMessage() {
            var message = document.getElementById('chat-message').value;
            var responseDiv = document.getElementById('chatbot-response');
            
            // Call the PHP function to send message to the chatbot
            jQuery.post('<?php echo admin_url('admin-ajax.php'); ?>', {
                action: 'send_message_to_chatbot',
                message: message
            }, function(response) {
                responseDiv.innerHTML = response;
            });
        }
    </script>
    <?php
    return ob_get_clean();
}

// AJAX handler for sending messages to the chatbot
function send_message_to_chatbot_callback() {
    $message = $_POST['message'];
    $response = send_message_to_chatbot($message);
    echo $response;
    wp_die();
}

add_shortcode('chatbot', 'chatbot_shortcode');
add_action('wp_ajax_send_message_to_chatbot', 'send_message_to_chatbot_callback');
add_action('wp_ajax_nopriv_send_message_to_chatbot', 'send_message_to_chatbot_callback');
?>
