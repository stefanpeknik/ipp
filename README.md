# ipp - projects

Specification of the project can be found in [here](ipp23spec.pdf).

Generic idea of the project is to create fully functioning interpreter of IPPcode23 language. It achieves so in two parts:
- [parse](parse/) - parses given code written in IPPcode23 language into XML while validating its syntax (more info [here](parse/readme1.md)),
- [interpret](interpret/) - takes the created XML and interpretates it (more info [here](interpret/readme2.md)).


## Final results

| Category | Percentage Evaluation |
|----------|-----------------------|
| Lexical Analysis (Error detection) | 93% |
| Syntactic Analysis (Error detection) | 100% |
| Semantic Analysis (Error detection) | 100% |
| Runtime Errors (Detection) | 100% |
| Instruction Interpretation | 100% |
| Interpretation of Non-Trivial Programs | 100% |
| Command Line Options | 100% |
| FLOAT Extension | 0% |
| STACK Extension | 0% |
| STATI Extension | 0% |
| Overall score without extensions | 99% |
