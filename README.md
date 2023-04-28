# ipp - projects

Specification of the project can be found in [here](ipp23spec.pdf).

Generic idea of the project is to create fully functioning interpreter of IPPcode23 language. It achieves so in two parts:
- [parse](parse/) - parses given code written in IPPcode23 language into XML while validating its syntax (more info [here](parse/readme1.md)),
- [interpret](interpret/) - takes the created XML and interpretates it (more info [here](interpret/readme2.md)).
