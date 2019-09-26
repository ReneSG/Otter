grammar otter;

/* START TOKENS */

// Keywords
CLASS: 'Class';
INHERITS: 'inherits';
LET: 'let';
DEF: 'def';
RETURN: 'return';
LIST: 'list';
READ: 'read';
WRITE: 'write';
IF: 'if';
UNLESS: 'unless';
ELSEIF: 'elseif';
ELSE: 'else';
PRIVATE: 'private';
PUBLIC: 'public';
WHILE: 'while';
BY: 'by';
FOR: 'for';
UNTIL: 'until';
INT: 'int';
FLOAT: 'float';
STRING: 'string';
BOOLEAN: 'boolean';
AT: '@';

// Operators
AND: 'and';
OR: 'or';
NOT: 'not';
LESS: '<';
GREATHER: '>';
LESS_EQUAL: '<=';
GREATHER_EQUAL: '>=';
EQUAL: '==';
NOT_EQUAL: '!=';
ASSIGN: '=';
ADD: '+';
MULT: '*';
SUBS: '-';
DIV: '/';

// Separators
OPEN_PAR: '(';
CLOSE_PAR: ')';
OPEN_CURLY: '{';
CLOSE_CURLY: '}';
OPEN_SQUARE: '[';
CLOSE_SQUARE: ']';
SEMICOLON: ';';
COLON: ':';
COMMA: ',';
DOT: '.';

// Primitives data types
BOOLEAN_PRIMITIVE: 'truthy' | 'falsy';
FLOAT_PRIMITIVE: [0-9]+ . [0-9]+?;
INT_PRIMITIVE: [0-9]+;
STRING_PRIMITIVE: '".*"';
ID: [A-Za-z]([A-Za-z0-9])*;

/* END TOKENS */

/* START GRAMMAR */

classAttributes: accessModifiers LET ID COLON otterType SEMICOLON;

assigment: LET ID COLON otterType ASSIGN constant SEMICOLON | listAssigment;

methodCall: ID DOT ID OPEN_PAR arguments? CLOSE_PAR SEMICOLON;

methodDeclaration: accessModifiers DEF ID OPEN_PAR arguments? CLOSE_PAR COLON otterType block;

block: OPEN_CURLY statements CLOSE_CURLY;

statements: conditional | whileLoop | forLoop | assigment;

conditional: IF OPEN_PAR expression CLOSE_PAR block (ELSEIF block)* (ELSE block)?;

unless: UNLESS OPEN_PAR expression CLOSE_PAR block;

whileLoop: WHILE OPEN_PAR expression CLOSE_PAR block;

forLoop: FOR OPEN_PAR ID UNTIL ID (GREATHER | GREATHER_EQUAL | LESS | LESS_EQUAL | EQUAL) term BY term;

classDeclaration: CLASS ID (INHERITS ID)? classBlock;

classBlock: classAttributes | methodDeclaration | classConstructor;

classConstructor: accessModifiers ID OPEN_PAR arguments CLOSE_PAR block;

writeIO: WRITE OPEN_PAR (STRING_PRIMITIVE | ID) CLOSE_PAR SEMICOLON;

readIO: READ OPEN_PAR CLOSE_PAR SEMICOLON;

listAssigment: LET ID COLON LIST LESS otterType GREATHER ASSIGN OPEN_SQUARE listElements? CLOSE_SQUARE SEMICOLON;

listElements: term (COMMA term)*;

expression: NOT expr | expr;

expr: term (GREATHER | GREATHER_EQUAL | LESS | LESS_EQUAL | EQUAL) term ((AND | OR) expr)* | term;

term: ID | constant | arithmeticExpr | AT ID;

arithmeticExpr: (ID | constant) (ADD | SUBS | MULT | DIV) term;

arguments: argument (COMMA argument)*;

argument: ID COLON otterType;

accessModifiers: PUBLIC | PRIVATE;

otterType: INT | FLOAT | STRING | BOOLEAN;

constant: BOOLEAN_PRIMITIVE | FLOAT_PRIMITIVE | INT_PRIMITIVE | STRING_PRIMITIVE | ID;

/* END GRAMMAR */

// Whitespace and comments
COMMENT: '/*' .*? '*/' -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
WS: [ \t\r\n\u000C]+ -> skip;
