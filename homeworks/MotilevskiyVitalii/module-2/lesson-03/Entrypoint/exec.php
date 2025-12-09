#!/usr/bin/env php
<?php

if (php_sapi_name() !== 'cli') {
    fwrite(STDERR, "Цей скрипт призначений для запуску з командного рядка.\n");
    exit(1);
}

if ($argc < 3) {
    fwrite(STDERR, "Використання: php {$argv[0]} <a> <b> [output_file]\n");
    exit(2);
}

$rawA = $argv[1];
$rawB = $argv[2];
echo "Result: $rawA * $rawB = " . ($rawA * $rawB);
echo "\n";

exit(0);
