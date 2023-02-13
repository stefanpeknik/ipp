<?php


class Constant {
    private $const;
    private $type;
    private $value;

    public function __construct($const) {
        if (!self::IsConst($const)) {
            exit(23);
        }
        $this->const = $const;
        $this->type = substr($const, 0, strpos($const, '@'));
        $this->value = substr($const, strpos($const, '@') + 1);
    }

    public static function IsConst($const) {
        # regex to check if the constant is in format int@int
        $int = "/int@[+-]?\d+/";
        # regex to check if the constant is in format bool@(true|false)
        $bool = "/bool@(true|false)/";
        # regex to check if the constant is in format string@string
        $string = "/string@(([^#\\@]+|\\[0-9]{3})*)/";
        # regex to check if the constant is in format nil@nil
        $nil = "/nil@nil/";

        if (preg_match($int, $const)) {
            return true;
        }
        elseif (preg_match($bool, $const)) {
            return true;
        }
        elseif (preg_match($string, $const)) {
            return true;
        }
        elseif (preg_match($nil, $const)) {
            return true;
        }
        else {
            return false;
        }
    }

    public function getConst() {
        return $this->const;
    }

    public function getType() {
        return $this->type;
    }

    public function getValue() {
        return $this->value;
    }
}

class Instruction {
    private $opcode;
    private $args;

    public function __construct($opcode, $args) {
        if (OpCode::IsOpCode($opcode)) {
            $this->opcode = new OpCode($opcode);
        }
        else {
            exit(22);
        }

        if (count($args) != count($this->opcode->getArgs())) {
            exit(23);
        }

        for($i = 0; $i < count($args); $i++) {
            if ($this->opcode->getArgs()[$i] == ArgType::VAR) {
                if (Variable::IsVar($args[$i])) {
                    $this->args[] = new Variable($args[$i]);
                }
                else {
                    exit(23);
                }
            }
            elseif ($this->opcode->getArgs()[$i] == ArgType::SYMB) {
                if (Symbol::IsSymbol($args[$i])) {
                    $this->args[] = new Symbol($args[$i]);
                }
                else {
                    exit(23);
                }
            }
            elseif ($this->opcode->getArgs()[$i] == ArgType::LABEL) {
                if (Label::IsLabel($args[$i])) {
                    $this->args[] = new Label($args[$i]);
                }
                else {
                    exit(23);
                }
            }
            elseif ($this->opcode->getArgs()[$i] == ArgType::TYPE) {
                if (Type::IsType($args[$i])) {
                    $this->args[] = new Type($args[$i]);
                }
                else {
                    exit(23);
                }
            }
        }

    }

    public function getOpcode() {
        return $this->opcode;
    }

    public function getArgs() {
        return $this->args;
    }
}
class Label {
    private $label;

    public function __construct($label) {
        if (!self::IsLabel($label)) {
            exit(23);
        }
        $this->label = $label;
    }

    public static function IsLabel($label) {
        # regex to check if the label is in format label
        $reg = "/[a-zA-Z_\$&%*!?-][a-zA-Z0-9_\$&%*!?-]*/";
        if (preg_match($reg, $label)) {
            return true;
        }
        else {
            return false;
        }
    }

    public function getLabel() {
        return $this->label;
    }
}
StartCheck($argc, $argv);

LocateHeader();

$instructions = ParseInstructions();


$xml = new SimpleXMLElement('<?xml version="1.0" encoding="UTF-8"?><program language="IPPcode23"></program>');

// TODO
for($i = 0; $i < count($instructions); $i++) {
    $instruction = $xml->addChild('instruction');
    $instruction->addAttribute('order', $i + 1);
    $instruction->addAttribute('opcode', $instructions[$i]->getOpcode()->getOpcode());
    $args = $instructions[$i]->getArgs();
    for($j = 0; $j < count($args); $j++) {
        $arg = $instruction->addChild('arg' . ($j + 1), $args[$j]->getArg());
        $arg->addAttribute('type', $args[$j]->getType());
    }
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
class ArgType {
    const NONE = 0;
    const VAR = 1;
    const SYMB = 2;
    const LABEL = 3;
    const TYPE = 4;
}

class OpCode {
    private static $OpCodes = array (
        'MOVE',
        'CREATEFRAME',
        'PUSHFRAME',
        'POPFRAME',
        'DEFVAR',
        'CALL',
        'RETURN',
        'PUSHS',
        'POPS',
        'ADD',
        'SUB',
        'MUL',
        'IDIV',
        'LT',
        'GT',
        'EQ',
        'AND',
        'OR',
        'NOT',
        'INT2CHAR',
        'STRI2INT',
        'READ',
        'WRITE',
        'CONCAT',
        'STRLEN',
        'GETCHAR',
        'SETCHAR',
        'TYPE',
        'LABEL',
        'JUMP',
        'JUMPIFEQ',
        'JUMPIFNEQ',
        'EXIT',
        'DPRINT',
        'BREAK'
    );

    private $opCode;
    private $args;

    public function __construct($opCode) {
        if (!self::IsOpCode($opCode)) {
            exit(22);
        }
        $this->opCode = $opCode;

        switch($this->opCode) {
            case 'MOVE':
                $this->args = array(ArgType::VAR, ArgType::SYMB);
                break;
            case 'CREATEFRAME':
                $this->args = array(ArgType::NONE);
                break;
            case 'PUSHFRAME':
                $this->args = array(ArgType::NONE);
                break;
            case 'POPFRAME':
                $this->args = array(ArgType::NONE);
                break;
            case 'DEFVAR':
                $this->args = array(ArgType::VAR);
                break;
            case 'CALL':
                $this->args = array(ArgType::LABEL);
                break;
            case 'RETURN':
                $this->args = array(ArgType::NONE);
                break;
            case 'PUSHS':
                $this->args = array(ArgType::SYMB);
                break;
            case 'POPS':
                $this->args = array(ArgType::VAR);
                break;
            case 'ADD':
                $this->args = array(ArgType::VAR, ArgType::SYMB, ArgType::SYMB);
                break;
            case 'SUB':
                $this->args = array(ArgType::VAR, ArgType::SYMB, ArgType::SYMB);
                break;
            case 'MUL':
                $this->args = array(ArgType::VAR, ArgType::SYMB, ArgType::SYMB);
                break;
            case 'IDIV':
                $this->args = array(ArgType::VAR, ArgType::SYMB, ArgType::SYMB);
                break;
            case 'LT':
                $this->args = array(ArgType::VAR, ArgType::SYMB, ArgType::SYMB);
                break;
            case 'GT':
                $this->args = array(ArgType::VAR, ArgType::SYMB, ArgType::SYMB);
                break;
            case 'EQ':
                $this->args = array(ArgType::VAR, ArgType::SYMB, ArgType::SYMB);
                break;
            case 'AND':
                $this->args = array(ArgType::VAR, ArgType::SYMB, ArgType::SYMB);
                break;
            case 'OR':
                $this->args = array(ArgType::VAR, ArgType::SYMB, ArgType::SYMB);
                break;
            case 'NOT':
                $this->args = array(ArgType::VAR, ArgType::SYMB);
                break;
            case 'INT2CHAR':
                $this->args = array(ArgType::VAR, ArgType::SYMB);
                break;
            case 'STRI2INT':
                $this->args = array(ArgType::VAR, ArgType::SYMB, ArgType::SYMB);
                break;
            case 'READ':
                $this->args = array(ArgType::VAR, ArgType::TYPE);
                break;
            case 'WRITE':
                $this->args = array(ArgType::SYMB);
                break;
            case 'CONCAT':
                $this->args = array(ArgType::VAR, ArgType::SYMB, ArgType::SYMB);
                break;
            case 'STRLEN':
                $this->args = array(ArgType::VAR, ArgType::SYMB);
                break;
            case 'GETCHAR':
                $this->args = array(ArgType::VAR, ArgType::SYMB, ArgType::SYMB);
                break;
            case 'SETCHAR':
                $this->args = array(ArgType::VAR, ArgType::SYMB, ArgType::SYMB);
                break;
            case 'TYPE':
                $this->args = array(ArgType::VAR, ArgType::SYMB);
                break;
            case 'LABEL':
                $this->args = array(ArgType::LABEL);
                break;
            case 'JUMP':
                $this->args = array(ArgType::LABEL);
                break;
            case 'JUMPIFEQ':
                $this->args = array(ArgType::LABEL, ArgType::SYMB, ArgType::SYMB);
                break;
            case 'JUMPIFNEQ':
                $this->args = array(ArgType::LABEL, ArgType::SYMB, ArgType::SYMB);
                break;
            case 'EXIT':
                $this->args = array(ArgType::SYMB);
                break;
            case 'DPRINT':
                $this->args = array(ArgType::SYMB);
                break;
            case 'BREAK':
                $this->args = array(ArgType::NONE);
                break;
        }
    }

    public static function IsOpCode($opCode) {
        if (in_array(strtoupper($opCode), self::$OpCodes)) {
            return true;
        }
        else {
            return false;
        }
    }

    public function getOpCode() {
        return $this->opCode;
    }

    public function getArgs() {
        return $this->args;
    }
}
class Symbol {
    private $symbol;

    public function __construct($symbol) {
        if (!self::IsSymbol($symbol)) {
            exit(23);
        }
        if (Variable::IsVar($symbol)) {
            $this->symbol = new Variable($symbol);
        }
        else {
            $this->symbol = new Constant($symbol);
        }
    }

    public static function IsSymbol($symbol) {
        if(Variable::IsVar($symbol)) {
            return true;
        }
        elseif(Constant::IsConst($symbol)) {
            return true;
        }
        else {
            return false;
        }
    }

    public function getSymbol() {
        return $this->symbol;
    }

}
class Type {
    private $type;

    public function __construct($type) {
        if (!self::IsType($type)) {
            exit(23);
        }
        $this->type = $type;
    }

    public static function IsType($type) {
        if ($type == "int" || $type == "bool" || $type == "string" || $type == "nil") {
            return true;
        }
        else {
            return false;
        }
    }

    public function getType() {
        return $this->type;
    }
}
class Variable {
    private $var;
    private $scope;
    private $name;

    public function __construct($var) {
        if (!self::IsVar($var)) {
            exit(23);
        }
        $this->var = $var;
        $this->scope = substr($var, 0, 2);
        $this->name = substr($var, 3);
    }

    public static function IsVar($var) {
        # regex to check if the variable is in format GF|LF|TF@var
        $reg = "/^(LF|TF|GF)@[a-zA-Z_\$&%*!?-][a-zA-Z0-9_\$&%*!?-]*$/";
        if (preg_match($reg, $var)) {
            return true;
        }
        else {
            return false;
        }
    }

    public function getVar() {
        return $this->var;
    }

    public function getScope() {
        return $this->scope;
    }

    public function getName() {
        return $this->name;
    }
}
class XMLGenerator {
    private $xml;
    private $indent;
    private $indentStep;

    public function __construct() {
        $this->xml = new DOMDocument('1.0', 'UTF-8');
        $this->indent = 0;
        $this->indentStep = 2;
    }

    public function generate($root) {
        $this->xml->appendChild($this->generateNode($root));
        return $this->xml->saveXML();
    }

    private function generateNode($node) {
        $xmlNode = $this->xml->createElement($node->getName());
        $this->indent += $this->indentStep;
        foreach ($node->getAttributes() as $key => $value) {
            $xmlNode->setAttribute($key, $value);
        }
        foreach ($node->getChildren() as $child) {
            $xmlNode->appendChild($this->generateNode($child));
        }
        $this->indent -= $this->indentStep;
        return $xmlNode;
    }
}