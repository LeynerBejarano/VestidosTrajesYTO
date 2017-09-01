<?php
	//$resource = opendir("./");

	//while(($entry = readdir($resource)) !== FALSE){
	//	echo $entry."<br/>";
	//}
//$variablePasadaDeLaLista = $_POST['variable'];
        $file_url = '/home/vttpythonanywhere/vtt/VestidosTrajesYTO/uploads/pdf/recibo.pdf';
        header('Content-Type: application/pdf');
        header("Content-disposition: attachment; filename=\"$file_url\"");
        readfile($file_url);
?>


