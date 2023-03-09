<?php
require_once 'variable.php';
require_once 'constant.php';
require_once 'errorCodes.php';

/**
 * Class for storing symbol
 * Class Symbol
 */
class Symbol {
    /**
     * Contains symbol, either variable or constant
     * @var mixed
     */
    private $symbol;

    /**
     * Constructor for Symbol class
     * @param $symbol symbol
     */
    public function __construct($symbol) {
        // check if symbol is valid
        if (!self::IsSymbol($symbol)) {
            exit(ErrorCodes::LEXICAL_OR_SYNTAX_ERROR);
        }
        // check if symbol is variable and if it is, create new variable
        if (Variable::IsVar($symbol)) {
            $this->symbol = new Variable($symbol);
        }
        // symbol is constant, create new constant
        else {
            $this->symbol = new Constant($symbol);
        }
    }

    /**
     * Checks if given string is symbol
     * @param string $symbol symbol
     * @return bool true if symbol is valid, false otherwise
     */
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

    /**
     * Returns symbol
     * @return mixed symbol, either variable or constant
     */
    public function getSymbol() {
        return $this->symbol;
    }

}