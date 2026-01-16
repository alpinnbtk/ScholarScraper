<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    
    $author = $input['author'] ?? '';
    $keyword = $input['keyword'] ?? '';
    $limit = isset($input['limit']) ? (int)$input['limit'] : 10;

    if (empty($author)) {
        echo json_encode(['error' => 'Nama Penulis wajib diisi untuk mode pencarian ini.']);
        exit;
    }

    $escaped_author = escapeshellarg($author);
    $escaped_keyword = escapeshellarg($keyword);
    $escaped_limit = escapeshellarg($limit);

    $pythonCmd = "python"; 
    $scriptPath = "../python/main.py";

    $command = "$pythonCmd $scriptPath -a $escaped_author -k $escaped_keyword -l $escaped_limit 2>&1";
    
    $raw_output = shell_exec($command);

    $start = strpos($raw_output, '{');
    $end = strrpos($raw_output, '}');

    if ($start !== false && $end !== false) {
        $output = substr($raw_output, $start, ($end - $start) + 1);
    } else {
        $output = $raw_output;
    }

    if (empty($output)) {
        echo json_encode(['error' => 'Gagal menjalankan Python. Output kosong.']);
    } else {
        echo $output;
    }
}
?>