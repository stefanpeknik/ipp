<?php


function my_is_int($input) {
    if ($input[0] == '-') {
        return ctype_digit(substr($input, 1));
    }
    return ctype_digit($input);
}

class Constant {
    private $type;
    private $const;

    private $Types = array (
        'int',
        'bool',
        'string',
        'nil'
    );

    public function __construct($type, $const) {
        if (!in_array($type, $this->Types)) {
            exit(69);
        }
        $this->type = $type;
        
        // switch($this->type) {
        //     case 'int':
        //         if (!my_is_int($const)) {
        //             exit(69);
        //         }
        //         break;
        //     case 'bool':
        //         if (!is_bool($const)) {
        //             exit(69);
        //         }
        //         break;
        //     case 'string':
        //         if (!is_string($const)) {
        //             exit(69);
        //         }
        //         break;
        //     case 'nil':
        //         if (!is_null($const)) {
        //             exit(69);
        //         }
        //         break;
        // }
        $this->const = $const;
    }

    public function getType() {
        return $this->type;
    }
    public function getConst() {
        return $this->const;
    }
}

// checks if the number of arguments is correct
if ($argc > 2) {
    exit(10);
}
// checks if the argument is --help
if ($argc == 2) {
    if ($argv[1] == '--help') {
        echo("print help");
    }
    else {
        exit(10);
    }    
}

$const = new Constant('int', '123');
echo $const->getType();
echo $const->getConst();
