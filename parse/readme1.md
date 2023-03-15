# Implementation documentation for the 1st task for the IPP 2022/2023

Name and surname: Štefan Pekník
Login: xpekni01


## Usage

Parses IPPcode23 code into an XML.

```php8.1 parse.php [--help]```

Input is read from STDIN.


## Program structure

`parse.php` is the main body of the program, containing start argument parsing, parsing of IPPcode23 code and generating XML.
The process is: 
- validate start arguments, 
- find header ".IPPcode23", parse code into a structure, 
- generate an XML from the structure and write it on STDOUT.

### Parsing of the start arguments

The program has to start either with no arguments, or with a single flag `--help` which makes the program print a help info and end.

### How the code is parsed
 
The program loops and reads each line, ignoring blank lines and comments. Each line is then split by a whitespace and  and given to a constructor of a instruction in a way that the first string is the instruction operation code and the rest are arguments. The given arguments for a construction are validated and if a operation code is found in a private array of operation codes, the program proceeds to validate whether all the given arguments for such operation are of a correct type (var/symb/const/label/type) and whether the numbers of arguments matches the required number by the instuction. Parsing of the arguments is done mostly using regular expressions.


### XML generation

The XML is generated using SimpleXML extension, formatted using DOM extension and printed on STDOUT.