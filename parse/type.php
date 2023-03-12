<?php

/**
 * Class for storing type
 * Class Type
 */
class Type {
    /**
     * Contains type in format type
     * @var string
     */
    private $type;

    /**
     * Creates new type
     * @param string $type type in format type
     */
    public function __construct($type) {
        // check if type is valid
        if (!self::IsType($type)) {
            exit(ErrorCodes::LEXICAL_OR_SYNTAX_ERROR);
        }
        $this->type = $type;
    }

    /**
     * Checks if given string is type
     * @param string $type type in format type
     * @return bool true if type is valid, false otherwise
     */
    public static function IsType($type) {
        if ($type == "int" || $type == "bool" || $type == "string" || $type == "nil") {
            return true;
        }
        else {
            return false;
        }
    }

    /**
     * Returns type in format type
     * @return string type in format type
     */
    public function getType() {
        return $this->type;
    }
}