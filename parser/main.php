<?php

StartCheck($argc, $argv);

$header = LocateHeader();

$instructions = ParseInstructions();

print_r($instructions);

function ParseInstructions() {
    $instructions = array();
    while ($line = fgets(STDIN)) {
        if(IsWholeLineComment($line) || IsWholeLineEmpty($line)) {
            continue;
        }
        $line = preg_replace('/#.*/', '', $line);
        $line = preg_replace('/\s+/', ' ', $line);
        $line = trim($line);
        if ($line == '') {
            continue;
        }
        $stuff = explode(' ', $line);
        $instruction = new Instruction($stuff[0], array_slice($stuff, 1));
        $instructions[] = $instruction;
    }
    return $instructions;
}

function LocateHeader() {
    $headReg = '/\.ippcode23/i';
    while ($line = fgets(STDIN)) {
        if(IsWholeLineComment($line) || IsWholeLineEmpty($line)) {
            continue;
        }
        if (preg_match($headReg, $line)) {
            $head = trim($line);
            return $head;
        }
        else {
            exit(21);
        }
    }
}

function StartCheck($argc, $argv) {
    // checks if the number of arguments is correct
    if ($argc > 2) {
        exit(10);
    }
    // checks if the argument is --help
    if ($argc == 2) {
        if ($argv[1] == '--help') {
            echo "Skript typu filtr (parse.php v jazyce PHP 8.1)\n";
            echo "načte ze standardního vstupu zdrojový kód v IPPcode23,\n"; 
            echo "zkontroluje lexikální a syntaktickou správnost kódu\n";
            echo "a vypíše na standardní výstup XML reprezentaci programu\n";
            exit(0);
        }
        else {
            exit(10);
        }
    }

}

function IsWholeLineComment($line) {
    $comment = '/^\s*#.*/';
    if (preg_match($comment, $line)) {
        return true;
    }
    else {
        return false;
    }
}

function IsWholeLineEmpty($line) {
    $empty = '/^\s*$/';
    if (preg_match($empty, $line)) {
        return true;
    }
    else {
        return false;
    }
}