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

program: (classDeclaration | declaration)* {Compiler.debug_quads()};

classDeclaration:
    CLASS class_id = ID (INHERITS inherit_id = ID)? {Compiler.add_class($class_id.text, $inherit_id.text)
        } OPEN_CURLY classBlock CLOSE_CURLY {Compiler.end_class_scope()};

classBlock: (
        classAttributes
        | methodDeclaration
        | classConstructor
    )*;

classAttributes:
    access_modifier=accessModifiers LET var_name=ID COLON var_type=otterType SEMICOLON {Compiler.add_instance_variable($var_name.text, $var_type.text, $access_modifier.text)
        };

classConstructor:
    access_modifier=accessModifiers const_name=ID {Compiler.add_constructor($const_name.text, $access_modifier.text)} OPEN_PAR arguments? CLOSE_PAR block;

declaration:
    LET var_name=ID COLON var_type=otterType ASSIGN value=term {Compiler.add_variable($var_name.text, $var_type.text, $value.text)} SEMICOLON
    | listAssigment;

assignment: <assoc=right> (AT)? reference ASSIGN {Compiler.push_op($ASSIGN.text)} expression {Compiler.gen_quad_assign()} SEMICOLON;

methodCall: ID DOT ID OPEN_PAR parameters? CLOSE_PAR;

constructorCall: ID OPEN_PAR parameters? CLOSE_PAR;

methodDeclaration:
    access_modifier=accessModifiers DEF method_name=ID {Compiler.add_method($method_name.text, $access_modifier.text)
        } OPEN_PAR arguments? CLOSE_PAR COLON return_type=returnType {Compiler.add_return_type($return_type.text)
        } block {Compiler.end_method_scope()};

block: OPEN_CURLY statements* CLOSE_CURLY;

statements:
    conditional
    | whileLoop
    | forLoop
    | declaration
    | assignment
    | unless
    | returnStatement
    | readIO
    | writeIO;

conditional:
    IF OPEN_PAR expression CLOSE_PAR {Compiler.start_condition_quad()} block (
        ELSEIF {Compiler.gen_goto_quad()} OPEN_PAR expression CLOSE_PAR {Compiler.start_condition_quad()} block
    )* (ELSE {Compiler.gen_goto_quad()} block)? {Compiler.end_condition_quad()};

unless: UNLESS OPEN_PAR expression CLOSE_PAR {Compiler.start_condition_quad(True)} block {Compiler.end_condition_quad()};

whileLoop: WHILE OPEN_PAR {Compiler.push_instruction_address()} expression CLOSE_PAR {Compiler.start_for_quad()} block {Compiler.end_while_quad()};

forLoop:
    FOR OPEN_PAR ID UNTIL {Compiler.push_instruction_address()} expression {Compiler.start_condition_quad()} BY expr CLOSE_PAR {Compiler.push_instruction_address()} block {Compiler.end_for_quad()};

returnStatement: RETURN term {Compiler.return_quad()} SEMICOLON;

writeIO:
    WRITE OPEN_PAR (STRING_PRIMITIVE | ID) {Compiler.write_quad()} CLOSE_PAR SEMICOLON;

readIO: READ OPEN_PAR CLOSE_PAR {Compiler.read_quad()} SEMICOLON;

listAssigment:
    LET ID COLON LIST LESS otterType GREATER ASSIGN OPEN_SQUARE listElements? CLOSE_SQUARE SEMICOLON
        ;

listElements: term (COMMA term)*;

expression: (NOT {Compiler.push_op($NOT.text)})? relationalExpr {Compiler.maybe_gen_not_quad()};

relationalExpr:comparisonExpr {Compiler.check_pending_and_or()} (op=(AND | OR) {Compiler.push_op($op.text)} relationalExpr {Compiler.check_pending_and_or()})?;

comparisonExpr: expr {Compiler.check_pending_rel_op()} (op=(GREATER | GREATER_EQUAL | LESS | LESS_EQUAL | EQUAL) {Compiler.push_op($op.text)} expr {Compiler.check_pending_rel_op()})?;

expr: termino {Compiler.check_pending_sum_sub()} (op=(ADD | SUBS) {Compiler.push_op($op.text)} expr {Compiler.check_pending_sum_sub()})?;

termino: factor {Compiler.check_pending_div_prod()} (op=(MULT | DIV) {Compiler.push_op($op.text)} termino {Compiler.check_pending_div_prod()})?;

factor: (constant | reference) | OPEN_PAR {Compiler.open_par()} relationalExpr CLOSE_PAR {Compiler.close_par()};

term: constant | reference | expression | methodCall | constructorCall;

arguments: argument (COMMA argument)*;

argument: arg_name=ID COLON arg_type=otterType {Compiler.add_method_argument($arg_name.text, $arg_type.text)};

parameters: term (COMMA term)*;

accessModifiers: PUBLIC | PRIVATE;

otterType: INT | FLOAT | STRING | BOOLEAN | ID;

returnType: otterType | VOID;

constant:
    BOOLEAN_PRIMITIVE {Compiler.push_constant('bool', $BOOLEAN_PRIMITIVE.text)}
    | FLOAT_PRIMITIVE {Compiler.push_constant('float', $FLOAT_PRIMITIVE.text)}
    | INT_PRIMITIVE {Compiler.push_constant('int', $INT_PRIMITIVE.text)}
    | STRING_PRIMITIVE {Compiler.push_constant('string', $STRING_PRIMITIVE.text)};

reference:
  ID {Compiler.push_constant('id', $ID.text)}
  | AT ID {Compiler.push_constant('@id', $ID.text)}
  | listReference;

listReference:
  ID {Compiler.push_constant('id', $ID.text)} (OPEN_SQUARE (constant | reference) {Compiler.resolve_dimension_access()} CLOSE_SQUARE)* {Compiler.complete_dimension_access()};

/* END GRAMMAR */
