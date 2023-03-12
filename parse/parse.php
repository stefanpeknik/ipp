<?php
require_once 'errorCodes.php';
require_once 'instruction.php';

// check if there are correct number of arguments
StartCheck($argc, $argv);
// look for header
LocateHeader();
// parse instructions
$instructions = ParseInstructions();
// generate xml
$xml = GenerateXMLFromInstructions($instructions);
// print xml to stdout
$stdout = fopen('php://stdout', 'w');
fwrite($stdout, $xml);
fclose($stdout);



/**
 * Function for generating xml from instructions
 * @param $instructions array of instructions
 * @return string xml
 */
function GenerateXMLFromInstructions($instructions) {
    $xml = new SimpleXMLElement('<?xml version="1.0" encoding="UTF-8"?><program language="IPPcode23"></program>');
    $dom = new DOMDocument();
    $dom->preserveWhiteSpace = false;
    $dom->formatOutput = true;
    
    // loop through instructions
    for($i = 0; $i < count($instructions); $i++) {
        // add instruction element
        $instruction = $xml->addChild('instruction');
        // add order atrribute
        $instruction->addAttribute('order', $i + 1);
        // add opcode attribute
        $instruction->addAttribute('opcode', $instructions[$i]->getOpcode()->getOpcode());

        // loop through arguments
        $args = $instructions[$i]->getArgs();
        for ($j = 0; $j < count($args); $j++) {
            // check if argument is variable
            if ($args[$j] instanceof Variable) {
                // add argument element
                $arg = $instruction->addChild('arg' . ($j + 1));
                // set argument element value
                $arg[$j] = $args[$j]->getVar();
                // add type attribute
                $arg->addAttribute('type', 'var');
            }
            // check if argument is constant
            elseif ($args[$j] instanceof Label) {
                // add argument element
                $arg = $instruction->addChild('arg' . ($j + 1));
                // set argument element value
                $arg[$j] = $args[$j]->getLabel();
                // add type attribute
                $arg->addAttribute('type', 'label');
            }
            // check if argument is type
            elseif ($args[$j] instanceof Type) {
                // add argument element
                $arg = $instruction->addChild('arg' . ($j + 1));
                // set argument element value
                $arg[$j] = $args[$j]->getType();
                // add type attribute
                $arg->addAttribute('type', 'type');
            }
            // check if argument is symbol
            elseif($args[$j] instanceof Symbol) {
                // check if symbol is variable
                if($args[$j]->getSymbol() instanceof Variable) {
                    // add argument element
                    $arg = $instruction->addChild('arg' . ($j + 1));
                    // set argument element value
                    $arg[$j] = $args[$j]->getSymbol()->getVar();
                    // add type attribute
                    $arg->addAttribute('type', 'var');
                }
                // symbol is constant
                else {
                    // add argument element
                    $arg = $instruction->addChild('arg' . ($j + 1));
                    // set argument element value
                    $arg[$j] = $args[$j]->getSymbol()->getValue();
                    // add type attribute
                    $arg->addAttribute('type', $args[$j]->getSymbol()->getType());
                }
            }
        }
    }
    $dom->loadXML($xml->asXML());
    // return xml
    return $dom->saveXML();
}

/**
 * Function for parsing instructions
 * @return array of instructions
 */
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

/**
 * Function for locating header
 * @return string header
 */
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

/**
 * Function for checking if there are correct number of arguments
 * @param $argc number of arguments
 * @param $argv array of arguments
 */
function StartCheck($argc, $argv) {
    // checks if the number of arguments is correct
    if ($argc > 2) {
        exit(ErrorCodes::HEADER_ERROR);
    }
    // checks if the argument is --help
    if ($argc == 2) {
        if ($argv[1] == '--help') {
            echo "Usage: php parse.php [--help]\n\n";
            echo "This script will work with the following parameters:\n\n";
            echo "Options:\n";
            echo "  --help                 display this help message and exit\n";
            exit(0);
        }
        else {
            exit(ErrorCodes::HEADER_ERROR);
        }
    }

}

/**
 * Function for checking if line is comment
 * @param $line line to check
 * @return bool true if line is comment, false otherwise
 */
function IsWholeLineComment($line) {
    $comment = '/^\s*#.*$/';
    if (preg_match($comment, $line)) {
        return true;
    }
    else {
        return false;
    }
}

/**
 * Function for checking if line is empty
 * @param $line line to check
 * @return bool true if line is empty, false otherwise
 */
function IsWholeLineEmpty($line) {
    $empty = '/^\s*$/';
    if (preg_match($empty, $line)) {
        return true;
    }
    else {
        return false;
    }
}