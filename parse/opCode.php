<?php
require_once 'errorCodes.php';

/**
 * Class for storing argument types
 * Class ArgType
 */
class ArgType {
    /**
     * Argument is variable
     * @var int
     */
    const VAR = 0;
    /**
     * Argument is symbol
     * @var int
     */
    const SYMB = 1;
    /**
     * Argument is label
     * @var int
     */
    const LABEL = 2;
    /**
     * Argument is type
     * @var int
     */
    const TYPE = 3;
}

/**
 * Class for storing opcodes
 * Class OpCode
 */
class OpCode {

    /**
     * Contains array of opcodes
     * @var array
     */
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

    /**
     * contains opcode of instruction
     * @var string
     */
    private $opCode;

    /**
     * contains array of argument types
     * @var array
     */
    private $args;

    /**
     * Constructor for OpCode class
     * @param $opCode opcode of instruction
     */
    public function __construct($opCode) {
        // check if given opcode is valid
        if (!self::IsOpCode($opCode)) {
            exit(ErrorCodes::OPCODE_ERROR);
        }
        $this->opCode = strtoupper($opCode);

        // set array of argument types
        switch($this->opCode) {
            case 'MOVE':
                $this->args = array(ArgType::VAR, ArgType::SYMB);
                break;
            case 'CREATEFRAME':
                $this->args = array();
                break;
            case 'PUSHFRAME':
                $this->args = array();
                break;
            case 'POPFRAME':
                $this->args = array();
                break;
            case 'DEFVAR':
                $this->args = array(ArgType::VAR);
                break;
            case 'CALL':
                $this->args = array(ArgType::LABEL);
                break;
            case 'RETURN':
                $this->args = array();
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
                $this->args = array();
                break;
        }
    }

    /**
     * Checks if given opcode is valid
     * @param $opCode opcode to check
     * @return bool true if opcode is valid, false otherwise
     */
    public static function IsOpCode($opCode) {
        if (in_array(strtoupper($opCode), self::$OpCodes)) {
            return true;
        }
        else {
            return false;
        }
    }

    /**
     * Returns opcode of instruction
     * @return string opcode of instruction
     */
    public function getOpCode() {
        return $this->opCode;
    }

    /**
     * Returns array of argument types of instruction
     * @return array array of argument types
     */
    public function getArgs() {
        return $this->args;
    }
}