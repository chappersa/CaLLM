<?php
if(isset($_GET['msg'])) {
	$result = file_get_contents("http://YOUR_SERVER/getResponse?msg=" . urlencode($_GET['msg']));
echo $result;
} 
else if(isset($_GET['url'])) {
	$result = file_get_contents("http://YOUR_SERVER/addToRepo?url=" . urlencode($_GET['url']));
echo $result;
} 
else if(isset($_GET['pas'])) {
	$result = file_get_contents("http://YOUR_SERVER5/authenticate?pas=" . urlencode($_GET['pas']));
echo $result;
} 
else {
	$result = file_get_contents("http://YOUR_SERVER/");
echo $result;
}