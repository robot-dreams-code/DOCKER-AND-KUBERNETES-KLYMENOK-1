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
$outputFile = $argv[3] ?? 'result.txt';

if (!is_numeric($rawA) || !is_numeric($rawB)) {
    fwrite(STDERR, "Помилка: обидва параметри повинні бути числами. Ви передали: '{$rawA}' і '{$rawB}'.\n");
    exit(3);
}

$a = (float) $rawA;
$b = (float) $rawB;
$result = $a * $b;

$content = "a: {$a}\nb: {$b}\nresult: {$a} * {$b} = {$result}\n";

$written = @file_put_contents($outputFile, $content, LOCK_EX);

if ($written === false) {
    fwrite(STDERR, "Не вдалося записати у файл '{$outputFile}'. Перевірте права доступу.\n");
    exit(4);
}

fwrite(STDOUT, "Результат помноження записано в файл '{$outputFile}'.\n");
exit(0);
