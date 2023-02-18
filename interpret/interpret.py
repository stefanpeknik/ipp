import argparse
import sys
import xml.etree.ElementTree as ET

# Chybové návratové kódy
ERR_MISSING_PARAM = 10
ERR_FILE_OPEN = 11
ERR_FILE_WRITE = 12
ERR_INVALID_XML_FORMAT = 31
ERR_INVALID_XML_STRUCTURE = 32
ERR_INTERNAL = 99

def parse_arguments():
    parser = argparse.ArgumentParser(description="Tento skript bude pracovat s těmito parametry:", add_help=False)
    parser.add_argument("--help", action="help", help="zobrazí tuto nápovědu a ukončí program")
    parser.add_argument("--source", dest="source_file", metavar="file", help="vstupní soubor s XML reprezentací zdrojového kódu")
    parser.add_argument("--input", dest="input_file", metavar="file", help="soubor se vstupy pro samotnou interpretaci zadaného zdrojového kódu")
    args = parser.parse_args()
    
    if args.source_file is None and args.input_file is None:
        print("Musí být zadán alespoň jeden z parametrů --source nebo --input.")
        sys.exit(ERR_MISSING_PARAM)
    
    if args.source_file is not None and args.input_file is not None:
        print("Nelze použít oba parametry --source a --input současně.")
        sys.exit(ERR_MISSING_PARAM)
    
    return args

def parse_xml_file(filename):
    try:
        tree = ET.parse(filename)
    except ET.ParseError:
        print(f"Error: File '{filename}' is not well-formed XML.", file=sys.stderr)
        sys.exit(ERR_XML_FORMAT)
    root = tree.getroot()
    for child in root:
        if child.tag != 'instruction':
            print(f"Error: Unexpected element '{child.tag}' found in XML file.", file=sys.stderr)
            sys.exit(ERR_XML_STRUCTURE)
        
    return root

def main():
    args = parse_arguments()
    if args.source:
        source_root = parse_xml_file(args.source)
    else:
        print("Error: Missing parameter '--source'.", file=sys.stderr)
        sys.exit(1)
    if args.input:
        input_root = parse_xml_file(args.input)
    else:
        input_root = ET.Element('inputs')
    # TODO: implement code execution
    print("Source code and inputs parsed successfully.")

if __name__ == '__main__':
    main()
