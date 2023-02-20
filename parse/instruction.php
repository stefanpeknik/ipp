<?php
require_once 'opCode.php';
require_once 'variable.php';
require_once 'symbol.php';
require_once 'label.php';
require_once 'type.php';
require_once 'errorCodes.php';


class Instruction {
    private $opcode;
    private $args;

    public function __construct($opcode, $args = array()) {
        if (OpCode::IsOpCode($opcode)) {
            $this->opcode = new OpCode($opcode);
        }
        else {
            exit(ErrorCodes::OPCODE_ERROR);
        }

        if (count($args) != count($this->opcode->getArgs())) {
            exit(ErrorCodes::LEXICAL_OR_SYNTAX_ERROR);
        }
        elseif(count($this->opcode->getArgs()) == 0) {
            $this->args = array();
        }
        else {
            for($i = 0; $i < count($args); $i++) {
                if ($this->opcode->getArgs()[$i] == ArgType::VAR) {
                    if (Variable::IsVar($args[$i])) {
                        $this->args[] = new Variable($args[$i]);
                    }
                    else {
                        exit(ErrorCodes::LEXICAL_OR_SYNTAX_ERROR);
                    }
                }
                elseif ($this->opcode->getArgs()[$i] == ArgType::SYMB) {
                    if (Symbol::IsSymbol($args[$i])) {
                        $this->args[] = new Symbol($args[$i]);
                    }
                    else {
                        exit(ErrorCodes::LEXICAL_OR_SYNTAX_ERROR);
                    }
                }
                elseif ($this->opcode->getArgs()[$i] == ArgType::LABEL) {
                    if (Label::IsLabel($args[$i])) {
                        $this->args[] = new Label($args[$i]);
                    }
                    else {
                        exit(ErrorCodes::LEXICAL_OR_SYNTAX_ERROR);
                    }
                }
                elseif ($this->opcode->getArgs()[$i] == ArgType::TYPE) {
                    if (Type::IsType($args[$i])) {
                        $this->args[] = new Type($args[$i]);
                    }
                    else {
                        exit(ErrorCodes::LEXICAL_OR_SYNTAX_ERROR);
                    }
                }
            }
        }
    }

    public function getOpcode() {
        return $this->opcode;
    }

    public function getArgs() {
        return $this->args;
    }
}