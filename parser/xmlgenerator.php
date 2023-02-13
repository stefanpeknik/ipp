<?php

class XMLGenerator {
    private $xml;
    private $indent;
    private $indentStep;

    public function __construct() {
        $this->xml = new DOMDocument('1.0', 'UTF-8');
        $this->indent = 0;
        $this->indentStep = 2;
    }

    public function generate($root) {
        $this->xml->appendChild($this->generateNode($root));
        return $this->xml->saveXML();
    }

    private function generateNode($node) {
        $xmlNode = $this->xml->createElement($node->getName());
        $this->indent += $this->indentStep;
        foreach ($node->getAttributes() as $key => $value) {
            $xmlNode->setAttribute($key, $value);
        }
        foreach ($node->getChildren() as $child) {
            $xmlNode->appendChild($this->generateNode($child));
        }
        $this->indent -= $this->indentStep;
        return $xmlNode;
    }
}