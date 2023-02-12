<?php
ini_set('display_errors', 'stderr');

if ($argc > 2) {
    exit(10);
}
if ($argc == 2 && $argv[1] == '--help') {
    echo("print help");
}
else {
    exit(10);
}