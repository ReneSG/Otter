grammar otter;

@parser::header {
from compilation.compiler import Compiler
}

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

program: {self.otterComp = Compiler()} (classDeclaration | declaration)*;

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
    LET ID COLON otterType ASSIGN expression SEMICOLON
    | listAssigment;

assignment: <assoc=right> (AT)? ID ASSIGN {self.otterComp.push_op($ASSIGN.text)} expression {self.otterComp.gen_quad_assign()} SEMICOLON;

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
    IF OPEN_PAR expression CLOSE_PAR {self.otterComp.start_condition_quad()} block (
        ELSEIF {self.otterComp.gen_goto_quad()} OPEN_PAR expression CLOSE_PAR {self.otterComp.start_condition_quad()} block
    )* (ELSE {self.otterComp.gen_goto_quad()} block)? {self.otterComp.end_condition_quad()};

unless: UNLESS OPEN_PAR expression CLOSE_PAR {self.otterComp.start_condition_quad(True)} block {self.otterComp.end_condition_quad()};

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

expression: (NOT {self.otterComp.push_op($NOT.text)})? relationalExpr {self.otterComp.maybe_gen_not_quad()};

relationalExpr:comparisonExpr {self.otterComp.check_pending_and_or()} (op=(AND | OR) {self.otterComp.push_op($op.text)} relationalExpr {self.otterComp.check_pending_and_or()})?;

comparisonExpr: expr (op=(GREATER | GREATER_EQUAL | LESS | LESS_EQUAL | EQUAL) {self.otterComp.push_op($op.text)} expr {self.otterComp.check_pending_rel_op()})?;

expr: termino (op=(ADD | SUBS) {self.otterComp.push_op($op.text)} expr {self.otterComp.check_pending_sum_sub()})?;

termino: factor (op=(MULT | DIV) {self.otterComp.push_op($op.text)} termino {self.otterComp.check_pending_div_prod()})?;

factor: (ID | constant | AT ID) | OPEN_PAR {self.otterComp.open_par()} relationalExpr CLOSE_PAR {self.otterComp.close_par()};

term: ID | constant | expression | AT ID | methodCall | constructorCall;

arguments: argument (COMMA argument)*;

argument: ID COLON otterType;

parameters: term (COMMA term)*;

accessModifiers: PUBLIC | PRIVATE;

otterType: INT | FLOAT | STRING | BOOLEAN | ID;

constant:
    BOOLEAN_PRIMITIVE {self.otterComp.push_constant('bool', $BOOLEAN_PRIMITIVE.text)}
    | FLOAT_PRIMITIVE {self.otterComp.push_constant('float', $FLOAT_PRIMITIVE.text)}
    | INT_PRIMITIVE {self.otterComp.push_constant('int', $INT_PRIMITIVE.text)}
    | STRING_PRIMITIVE {self.otterComp.push_constant('string', $STRING_PRIMITIVE.text)}
    | ID;

/* END GRAMMAR */
