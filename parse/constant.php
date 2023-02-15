<?php

class Constant {
    private $const;
    private $type;
    private $value;

    public function __construct($const) {
        if (!self::IsConst($const)) {
            exit(ErrorCodes::LEXICAL_OR_SYNTAX_ERROR);
        }
        $this->const = $const;
        $this->type = substr($const, 0, strpos($const, '@'));
        $this->value = substr($const, strpos($const, '@') + 1);
    }

    public static function IsConst($const) {
        $int = '/^int@[+-]?(0x[0-9a-fA-F]+|0[0-7]*|[1-9][0-9]*)$/';
        $bool = '/^bool@(true|false)$/';
        $string = '/^string@((?![\s#"\\\\]).|\\\\[0-9]{3})*$/';
        $nil = '/^nil@nil$/';

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
