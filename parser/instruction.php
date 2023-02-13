<?php

class Instruction {
    private $opcode;
    private $args;

    public function __construct($opcode, $args) {
        if (OpCode::IsOpCode($opcode)) {
            $this->opcode = new OpCode($opcode);
        }
        else {
            exit(22);
        }

        if (count($args) != count($this->opcode->getArgs())) {
            exit(23);
        }

        for($i = 0; $i < count($args); $i++) {
            if ($this->opcode->getArgs()[$i] == ArgType::VAR) {
                if (Variable::IsVar($args[$i])) {
                    $this->args[] = new Variable($args[$i]);
                }
                else {
                    exit(23);
                }
            }
            elseif ($this->opcode->getArgs()[$i] == ArgType::SYMB) {
                if (Symbol::IsSymbol($args[$i])) {
                    $this->args[] = new Symbol($args[$i]);
                }
                else {
                    exit(23);
                }
            }
            elseif ($this->opcode->getArgs()[$i] == ArgType::LABEL) {
                if (Label::IsLabel($args[$i])) {
                    $this->args[] = new Label($args[$i]);
                }
                else {
                    exit(23);
                }
            }
            elseif ($this->opcode->getArgs()[$i] == ArgType::TYPE) {
                if (Type::IsType($args[$i])) {
                    $this->args[] = new Type($args[$i]);
                }
                else {
                    exit(23);
                }
            }
            elseif ($this->opcode->getArgs()[$i] == ArgType::NONE) {
                if ($args[$i] == null) {
                    $this->args[] = null;
                }
                else {
                    exit(23);
                }
            }
        }

    }

}