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
GREATER: '>';
LESS_EQUAL: '<=';
GREATER_EQUAL: '>=';
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
STRING_PRIMITIVE: '"' .*? '"';
VOID: 'void';
ID: [A-Za-z]([A-Za-z0-9])*;

// Whitespace and comments
COMMENT: '/*' .*? '*/' -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
WS: [ \t\r\n\u000C]+ -> skip;

/* END TOKENS */

/* START GRAMMAR */

program: (classDeclaration | declaration)*;

classDeclaration:
    CLASS ID (INHERITS ID)? OPEN_CURLY classBlock CLOSE_CURLY;

classBlock: (
        classAttributes
        | methodDeclaration
        | classConstructor
    )*;

classAttributes:
    accessModifiers LET ID COLON otterType SEMICOLON;

classConstructor:
    accessModifiers ID OPEN_PAR arguments? CLOSE_PAR block;

declaration:
    LET ID COLON otterType ASSIGN term SEMICOLON
    | listAssigment;

assignment: (AT)? ID ASSIGN term SEMICOLON;

methodCall: ID DOT ID OPEN_PAR parameters? CLOSE_PAR;

constructorCall: ID OPEN_PAR parameters? CLOSE_PAR;

methodDeclaration:
    accessModifiers DEF ID OPEN_PAR arguments? CLOSE_PAR COLON (
        otterType
        | VOID
    ) block;

block: OPEN_CURLY statements* CLOSE_CURLY;

statements:
    conditional
    | whileLoop
    | forLoop
    | declaration
    | assignment
    | unless
    | returnStatement;

conditional:
    IF OPEN_PAR expression CLOSE_PAR block (
        ELSEIF OPEN_PAR expression CLOSE_PAR block
    )* (ELSE block)?;

unless: UNLESS OPEN_PAR expression CLOSE_PAR block;

whileLoop: WHILE OPEN_PAR expression CLOSE_PAR block;

forLoop:
    FOR OPEN_PAR ID UNTIL ID (
        GREATER
        | GREATER_EQUAL
        | LESS
        | LESS_EQUAL
        | EQUAL
    ) term BY term CLOSE_PAR block;

returnStatement: RETURN term SEMICOLON;

writeIO:
    WRITE OPEN_PAR (STRING_PRIMITIVE | ID) CLOSE_PAR SEMICOLON;

readIO: READ OPEN_PAR CLOSE_PAR SEMICOLON;

listAssigment:
    LET ID COLON LIST LESS otterType GREATER ASSIGN OPEN_SQUARE listElements? CLOSE_SQUARE SEMICOLON
        ;

listElements: term (COMMA term)*;

expression: NOT? relationalExpr;

relationalExpr: comparisonExpr ((AND | OR) relationalExpr)?;

comparisonExpr: expr ((GREATER | GREATER_EQUAL | LESS | LESS_EQUAL | EQUAL) expr)?;

expr: termino ((ADD | SUBS) expr)?;

termino: factor ((MULT | DIV) termino)?;

factor: (ID | constant | AT ID) | OPEN_PAR relationalExpr CLOSE_PAR;

term: ID | constant | arithmeticExpr | AT ID | methodCall | constructorCall;

arithmeticExpr: (ID | constant | AT ID) (ADD | SUBS | MULT | DIV) term;

arguments: argument (COMMA argument)*;

argument: ID COLON otterType;

parameters: term (COMMA term)*;

accessModifiers: PUBLIC | PRIVATE;

otterType: INT | FLOAT | STRING | BOOLEAN | ID;

constant:
    BOOLEAN_PRIMITIVE
    | FLOAT_PRIMITIVE
    | INT_PRIMITIVE
    | STRING_PRIMITIVE
    | ID;

/* END GRAMMAR */
