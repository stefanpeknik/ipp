<?php
require_once 'opCode.php';
require_once 'variable.php';
require_once 'symbol.php';
require_once 'label.php';
require_once 'type.php';
require_once 'errorCodes.php';

/**
 * Class for storing instruction
 * Class Instruction
 */
class Instruction {

    /**
     * contains opcode of instruction
     * @var OpCode
     */
    private $opcode;

    /**
     * contains array of arguments of instruction
     * @var array
     */
    private $args;

    /**
     * Constructor for Instruction class
     * @param $opcode opcode of instruction
     * @param $args array of arguments of instruction
     */
    public function __construct($opcode, $args = array()) {
        // check if given opcode is valid
        if (!OpCode::IsOpCode($opcode)) {
            exit(ErrorCodes::OPCODE_ERROR);
        }
        $this->opcode = new OpCode($opcode);

        // check if number of arguments is valid
        if (count($args) != count($this->opcode->getArgs())) {
            exit(ErrorCodes::LEXICAL_OR_SYNTAX_ERROR);
        }
        // if there are no arguments, set args to empty array
        elseif(count($this->opcode->getArgs()) == 0) {
            $this->args = array();
        }
        // if there are arguments, check if they are valid
        else {
            // check if each argument is valid
            for($i = 0; $i < count($args); $i++) {
                // check if argument is variable and if it is, create new variable
                if ($this->opcode->getArgs()[$i] == ArgType::VAR) {
                    if (Variable::IsVar($args[$i])) {
                        $this->args[] = new Variable($args[$i]);
                    }
                    else {
                        exit(ErrorCodes::LEXICAL_OR_SYNTAX_ERROR);
                    }
                }
                // check if argument is constant and if it is, create new constant
                elseif ($this->opcode->getArgs()[$i] == ArgType::SYMB) {
                    if (Symbol::IsSymbol($args[$i])) {
                        $this->args[] = new Symbol($args[$i]);
                    }
                    else {
                        exit(ErrorCodes::LEXICAL_OR_SYNTAX_ERROR);
                    }
                }
                // check if argument is label and if it is, create new label
                elseif ($this->opcode->getArgs()[$i] == ArgType::LABEL) {
                    if (Label::IsLabel($args[$i])) {
                        $this->args[] = new Label($args[$i]);
                    }
                    else {
                        exit(ErrorCodes::LEXICAL_OR_SYNTAX_ERROR);
                    }
                }
                // check if argument is type and if it is, create new type
                elseif ($this->opcode->getArgs()[$i] == ArgType::TYPE) {
                    if (Type::IsType($args[$i])) {
                        $this->args[] = new Type($args[$i]);
                    }
                    else {
                        exit(ErrorCodes::LEXICAL_OR_SYNTAX_ERROR);
                    }
                }
                // if argument is not variable, constant, label or type, exit
                else {
                    exit(ErrorCodes::LEXICAL_OR_SYNTAX_ERROR);
                }
            }
        }
    }

    /**
     * returns opcode of instruction
     * @return OpCode opcode of instruction
     */
    public function getOpcode() {
        return $this->opcode;
    }

    /**
     * returns array of arguments of instruction
     * @return array array of arguments of instruction
     */
    public function getArgs() {
        return $this->args;
    }
}