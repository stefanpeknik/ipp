<?php

class Type {
    private $type;

    public function __construct($type) {
        if (!self::IsType($type)) {
            exit(ErrorCodes::LEXICAL_OR_SYNTAX_ERROR);
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