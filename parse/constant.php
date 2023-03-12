<?php

/**
 * Class for storing constant
 * Class Constant
 */
class Constant {
    
    /**
     * Contains constant in format type@value
     * @var string
     */
    private $const;

    /**
     * Contains type of constant
     * @var string
     */
    private $type;

    /**
     * Contains value of constant
     * @var string
     */
    private $value;

    /**
     * Creates new constant
     * @param string $const constant in format type@value
     */
    public function __construct($const) {
        // check if constant is valid
        if (!self::IsConst($const)) {
            exit(ErrorCodes::LEXICAL_OR_SYNTAX_ERROR);
        }
        $this->const = $const;
        $this->type = substr($const, 0, strpos($const, '@'));
        $this->value = substr($const, strpos($const, '@') + 1);
    }

    /**
     * Checks if given string is constant
     * @param string $const constant in format type@value
     * @return bool true if constant is valid, false otherwise
     */
    public static function IsConst($const) {
        // set up regexes for each type of constant
        $decimal = '[1-9][0-9]*(_[0-9]+)*|0';
        $hexadecimal = '0[xX][0-9a-fA-F]+(_[0-9a-fA-F]+)*';
        $octal = '0[oO]?[0-7]+(_[0-7]+)*';
        $int = "/^int@[+-]?(($decimal)|($hexadecimal)|($octal))$/";
        $bool = '/^bool@(true|false)$/';
        $string = '/^string@((?![\s#"\\\\]).|\\\\[0-9]{3})*$/';
        $nil = '/^nil@nil$/';

        // check if constant matches any of the regexes
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

    /**
     * Returns constant in format type@value
     * @return string constant in format type@value
     */
    public function getConst() {
        return $this->const;
    }

    /**
     * Returns type of constant
     * @return string type of constant
     */
    public function getType() {
        return $this->type;
    }

    /**
     * Returns value of constant
     * @return string value of constant
     */
    public function getValue() {
        return $this->value;
    }
}
