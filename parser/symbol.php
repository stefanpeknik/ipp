<?php

class Symbol {
    private $symbol;

    public function __construct($symbol) {
        if (!self::IsSymbol($symbol)) {
            exit(23);
        }
        if (Variable::IsVar($symbol)) {
            $this->symbol = new Variable($symbol);
        }
        else {
            $this->symbol = new Constant($symbol);
        }
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

}