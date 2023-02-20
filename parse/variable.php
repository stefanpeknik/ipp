<?php
require_once 'errorCodes.php';

class Variable {
    private $var;
    private $scope;
    private $name;

    public function __construct($var) {
        if (!self::IsVar($var)) {
            exit(ErrorCodes::LEXICAL_OR_SYNTAX_ERROR);
        }
        $this->var = $var;
        $this->scope = substr($var, 0, 2);
        $this->name = substr($var, 3);
    }

    public static function IsVar($var) {
        # regex to check if the variable is in format GF|LF|TF@var
        $reg = '/^(LF|TF|GF)@[a-zA-Z_$&%*!?-][a-zA-Z0-9_$&%*!?-]*$/';
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