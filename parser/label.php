<?php

class Label {
    private $label;

    public function __construct($label) {
        if (!self::IsLabel($label)) {
            exit(23);
        }
        $this->label = $label;
    }

    public static function IsLabel($label) {
        # regex to check if the label is in format label
        $reg = "/[a-zA-Z_\$&%*!?-][a-zA-Z0-9_\$&%*!?-]*/";
        if (preg_match($reg, $label)) {
            return true;
        }
        else {
            return false;
        }
    }

    public function getLabel() {
        return $this->label;
    }
}