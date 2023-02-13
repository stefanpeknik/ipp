<?php

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