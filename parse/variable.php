<?php
require_once 'errorCodes.php';

/**
 * Class for storing variable
 * Class Variable
 */
class Variable {
    /**
     * Contains variable in format GF|LF|TF@var
     * @var string
     */
    private $var;

    /**
     * Contains scope (GF|LF|TF) of variable
     * @var string
     */
    private $scope;

    /**
     * Contains name of variable
     * @var string
     */
    private $name;

    /**
     * Constructor for Variable class
     * @param $var variable in format GF|LF|TF@var
     */
    public function __construct($var) {
        if (!self::IsVar($var)) {
            exit(ErrorCodes::LEXICAL_OR_SYNTAX_ERROR);
        }
        $this->var = $var;
        $this->scope = substr($var, 0, 2);
        $this->name = substr($var, 3);
    }

    /**
     * Checks if given string is variable
     * @param string $var variable in format GF|LF|TF@var
     * @return bool true if variable is valid, false otherwise
     */
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

    /**
     * Returns variable in format GF|LF|TF@var
     * @return string variable in format GF|LF|TF@var
     */
    public function getVar() {
        return $this->var;
    }

    /**
     * Returns scope of variable
     * @return string scope (GF|LF|TF) of variable
     */
    public function getScope() {
        return $this->scope;
    }

    /**
     * Returns name of variable
     * @return string name of variable
     */
    public function getName() {
        return $this->name;
    }
}