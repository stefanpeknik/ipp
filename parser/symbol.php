<?php

class Symbol {
    private $symbol;
    private $isVar;
    private $isConst;

    public function __construct($symbol) {
        if (!self::IsSymbol($symbol)) {
            exit(23);
        }
        if (Variable::IsVar($symbol)) {
            $this->isVar = true;
        }
        else {
            $this->isVar = false;
            $this->isConst = true;
        }
        $this->symbol = $symbol;
    }

    public static function IsSymbol($symbol) {
        if(Variable::IsVar($symbol)) {
            return true;
        }
        elseif(Constant::IsConst($symbol)) {
            return true;
        }
        else {
            return false;
        }
    }

    public function getSymbol() {
        return $this->symbol;
    }

    public function isVar() {
        return $this->isVar;
    }

    public function isConst() {
        return $this->isConst;
    }
}