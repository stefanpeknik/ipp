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
        // TODO
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
