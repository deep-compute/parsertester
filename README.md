# Parser Tester

Helps in iteratively developing string parsing functions.

Often there is a need to develop string parsers using regular expression and
other rule basde methods. The usual problem with this approach is that it is
brittle and changes made to the parser to address some cases causes regressions
in other cases.

The Parser Tester is useful make the process less painful. Below is a brief
example on how to use this.

strings.txt: Dummy file containing strings that we need to parse (one per line)
```
Hello
SDSDD
```

dummy_parser.py: A dummy parser that simple lower cases the input string
(Look inside `parsertester` directory for this file)

Running Parser Tester:


```bash
parsertester strings.txt strings.db dummy_parser.Parser
```
