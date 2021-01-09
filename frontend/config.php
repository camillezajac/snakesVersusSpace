<?php
define('DBSERVER', 'localhost'); //Database server
define ('DBUSERNAME', 'root'); //Database username
define('DBPASSWORD', ''); //Database password
define('DBNAME', 'login'); //Database name

/* connect to MySQL database */
$db = mysqli_connect(DBSERVER, DBUSERNAME, DBPASSWORD, DBNAME);

// Check db connection
if($db === false) {
	die("Error: connection err. ". mysqli_connect_error());

}
?>