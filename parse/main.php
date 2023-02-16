<?php

class ErrorCodes {
    const HEADER_ERROR = 21;
    const OPCODE_ERROR = 22;
    const LEXICAL_OR_SYNTAX_ERROR = 23;
}

StartCheck($argc, $argv);

LocateHeader();

$instructions = ParseInstructions();


$xml = GenerateXMLFromInstructions($instructions);

// Open the stdout stream for writing
$stdout = fopen('php://stdout', 'w');

// Write the XML document to stdout
fwrite($stdout, $xml);

// Close the stdout stream
fclose($stdout);


function GenerateXMLFromInstructions($instructions) {
    $xml = new SimpleXMLElement('<?xml version="1.0" encoding="UTF-8"?><program language="IPPcode23"></program>');
    $dom = new DOMDocument();
    $dom->preserveWhiteSpace = false;
    $dom->formatOutput = true;
    
    for($i = 0; $i < count($instructions); $i++) {
        $instruction = $xml->addChild('instruction');
        $instruction->addAttribute('order', $i + 1);
        $instruction->addAttribute('opcode', $instructions[$i]->getOpcode()->getOpcode());
        $args = $instructions[$i]->getArgs();
        for ($j = 0; $j < count($args); $j++) {
            if ($args[$j] instanceof Variable) {
                $arg = $instruction->addChild('arg' . ($j + 1));
                $arg[$j] = $args[$j]->getVar();
                $arg->addAttribute('type', 'var');
            }
            elseif ($args[$j] instanceof Label) {
                $arg = $instruction->addChild('arg' . ($j + 1));
                $arg[$j] = $args[$j]->getLabel();
                $arg->addAttribute('type', 'label');
            }
            elseif ($args[$j] instanceof Type) {
                $arg = $instruction->addChild('arg' . ($j + 1));
                $arg[$j] = $args[$j]->getType();
                $arg->addAttribute('type', 'type');
            }
            elseif($args[$j] instanceof Symbol) {
                if($args[$j]->getSymbol() instanceof Variable) {
                    $arg = $instruction->addChild('arg' . ($j + 1));
                    $arg[$j] = $args[$j]->getSymbol()->getVar();
                    $arg->addAttribute('type', 'var');
                }
                else {
                    $arg = $instruction->addChild('arg' . ($j + 1));
                    $arg[$j] = $args[$j]->getSymbol()->getValue();
                    $arg->addAttribute('type', $args[$j]->getSymbol()->getType());
                }
            }
        }
    }
    $dom->loadXML($xml->asXML());
    return $dom->saveXML();
}

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
        if (count($stuff) == 1) {
            $instruction = new Instruction($stuff[0]);
        }
        else {
            $instruction = new Instruction($stuff[0], array_slice($stuff, 1));
        }
        $instructions[] = $instruction;
    }
    return $instructions;
}

function LocateHeader() {
    $headReg = '/^\s*\.ippcode23\s*(?:#.*)?$/i';
    while ($line = fgets(STDIN)) {
        if(IsWholeLineComment($line) || IsWholeLineEmpty($line)) {
            continue;
        }
        if (preg_match($headReg, $line)) {
            $head = trim($line);
            return $head;
        }
        else {
            exit(ErrorCodes::HEADER_ERROR);
        }
    }
}

function StartCheck($argc, $argv) {
    // checks if the number of arguments is correct
    if ($argc > 2) {
        exit(ErrorCodes::HEADER_ERROR);
    }
    // checks if the argument is --help
    if ($argc == 2) {
        if ($argv[1] == '--help') {
            echo "Použití: php parse.php [--help]\n\n";
            echo "Tento skript bude pracovat s těmito parametry:\n\n";
            echo "Volby:\n";
            echo "  --help                 zobrazí tuto nápovědu a ukončí program\n";
            exit(0);
        }
        else {
            exit(ErrorCodes::HEADER_ERROR);
        }
    }

}

function IsWholeLineComment($line) {
    $comment = '/^\s*#.*$/';
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