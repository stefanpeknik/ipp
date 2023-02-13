<?php

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