<?php

/**
 * Class for storing label
 * Class Label
 */
class Label {

    /**
     * Contains label in format label
     * @var string
     */
    private $label;

    /**
     * Creates new label
     * @param string $label label in format label
     */
    public function __construct($label) {
        // check if label is valid
        if (!self::IsLabel($label)) {
            exit(ErrorCodes::LEXICAL_OR_SYNTAX_ERROR);
        }
        $this->label = $label;
    }

    /**
     * Checks if given string is label
     * @param string $label label in format label
     * @return bool true if label is valid, false otherwise
     */
    public static function IsLabel($label) {
        // set up regex for label
        $reg = '/^[a-zA-Z_$&%*!?-][a-zA-Z0-9_$&%*!?-]*$/';
        // check if label matches regex
        if (preg_match($reg, $label)) {
            return true;
        }
        else {
            return false;
        }
    }

    /**
     * Returns label in format label
     * @return string label in format label
     */
    public function getLabel() {
        return $this->label;
    }
}