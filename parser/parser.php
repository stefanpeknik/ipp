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
            elseif ($this->opcode->getArgs()[$i] == ArgType::NONE) {
                if ($args[$i] == null) {
                    $this->args[] = null;
                }
                else {
                    exit(23);
                }
            }
        }

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
enum ArgType {
    const NONE = 0;
    const VAR = 1;
    const SYMB = 2;
    const LABEL = 3;
    const TYPE = 4;
}

class OpCode {
    private $OpCodes = array (
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
                $this->args = array(Arg::VAR, Arg::SYMB);
                break;
            case 'CREATEFRAME':
                $this->args = array(Arg::NONE);
                break;
            case 'PUSHFRAME':
                $this->args = array(Arg::NONE);
                break;
            case 'POPFRAME':
                $this->args = array(Arg::NONE);
                break;
            case 'DEFVAR':
                $this->args = array(Arg::VAR);
                break;
            case 'CALL':
                $this->args = array(Arg::LABEL);
                break;
            case 'RETURN':
                $this->args = array(Arg::NONE);
                break;
            case 'PUSHS':
                $this->args = array(Arg::SYMB);
                break;
            case 'POPS':
                $this->args = array(Arg::VAR);
                break;
            case 'ADD':
                $this->args = array(Arg::VAR, Arg::SYMB, Arg::SYMB);
                break;
            case 'SUB':
                $this->args = array(Arg::VAR, Arg::SYMB, Arg::SYMB);
                break;
            case 'MUL':
                $this->args = array(Arg::VAR, Arg::SYMB, Arg::SYMB);
                break;
            case 'IDIV':
                $this->args = array(Arg::VAR, Arg::SYMB, Arg::SYMB);
                break;
            case 'LT':
                $this->args = array(Arg::VAR, Arg::SYMB, Arg::SYMB);
                break;
            case 'GT':
                $this->args = array(Arg::VAR, Arg::SYMB, Arg::SYMB);
                break;
            case 'EQ':
                $this->args = array(Arg::VAR, Arg::SYMB, Arg::SYMB);
                break;
            case 'AND':
                $this->args = array(Arg::VAR, Arg::SYMB, Arg::SYMB);
                break;
            case 'OR':
                $this->args = array(Arg::VAR, Arg::SYMB, Arg::SYMB);
                break;
            case 'NOT':
                $this->args = array(Arg::VAR, Arg::SYMB);
                break;
            case 'INT2CHAR':
                $this->args = array(Arg::VAR, Arg::SYMB);
                break;
            case 'STRI2INT':
                $this->args = array(Arg::VAR, Arg::SYMB, Arg::SYMB);
                break;
            case 'READ':
                $this->args = array(Arg::VAR, Arg::TYPE);
                break;
            case 'WRITE':
                $this->args = array(Arg::SYMB);
                break;
            case 'CONCAT':
                $this->args = array(Arg::VAR, Arg::SYMB, Arg::SYMB);
                break;
            case 'STRLEN':
                $this->args = array(Arg::VAR, Arg::SYMB);
                break;
            case 'GETCHAR':
                $this->args = array(Arg::VAR, Arg::SYMB, Arg::SYMB);
                break;
            case 'SETCHAR':
                $this->args = array(Arg::VAR, Arg::SYMB, Arg::SYMB);
                break;
            case 'TYPE':
                $this->args = array(Arg::VAR, Arg::SYMB);
                break;
            case 'LABEL':
                $this->args = array(Arg::LABEL);
                break;
            case 'JUMP':
                $this->args = array(Arg::LABEL);
                break;
            case 'JUMPIFEQ':
                $this->args = array(Arg::LABEL, Arg::SYMB, Arg::SYMB);
                break;
            case 'JUMPIFNEQ':
                $this->args = array(Arg::LABEL, Arg::SYMB, Arg::SYMB);
                break;
            case 'EXIT':
                $this->args = array(Arg::SYMB);
                break;
            case 'DPRINT':
                $this->args = array(Arg::SYMB);
                break;
            case 'BREAK':
                $this->args = array(Arg::NONE);
                break;
        }
    }

    public static function IsOpCode($opCode) {
        if (in_array(strtoupper($opCode), $this->OpCodes)) {
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
    private $isVar;
    private $isConst;

    public function __construct($symbol) {
        if (!self::IsSymbol($symbol)) {
            exit(23);
        }
        if (Variable::IsVar($symbol)) {
            $this->isVar = true;
        }
        else {
            $this->isVar = false;
            $this->isConst = true;
        }
        $this->symbol = $symbol;
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

    public function isVar() {
        return $this->isVar;
    }

    public function isConst() {
        return $this->isConst;
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