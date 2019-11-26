# Otter Language

## Developers

- René García Sáenz
- Joao Gabriel Moura Almeida

## Requirements

- Python 3.7.2
- Antlr4

## Development
To compile the grammar use the following command:

```bash
$ ntlr4 -Dlanguage=Python3 grammar/otter.g4
```

To run a Otter program run (The grammar has to be compiled at least once to be able to run the following command):

```bash
$ python3 Otter.py <file-name>
```

## Usage

To run an Otter program do (This will recompile the grammar and run the input file):
```bash
$ ./otter <file-name>
```

# Reference manual

### Class declaration
In the Otter programming language everything has to be on a class. By default Otter will detect the Main class and the main function within that class and run that function at the start of the program.

To declare a class use the `Class` keyword followed by the class name, as shown in the following example

```
Class Main {
    public Main() {
        write("Hello world!");
    }
}
```

### Class attributes
As in almost every Object Oriented Programming language, Otter allows you to have attributes within a class declaration. To declare a class attribute use the `public` or `private` keyword to determine the access modifiers of the attribute followed by the `let` keyword and the type of the attribute. The following block of code shows an example of it.

```
Class Main {
  public let foo: int;
  private let bar: string;
}
```

Otter programming language uses a special character to indicate the reference of a class attribute. Preprend `@` character to the attribute to reference it.
```
Class Main {
  public let foo: int;
  private let bar: string;

  public main() {
    @foo = 10;
    @bar = "Hello World!";
  }
}
```

### Variables

In order to declare a variable within a function scope use the `let` keyword followed by the variable name and the variable type.

Given that Otter is a typed programming language, once a variable is declared it cannot change its type.

```
Class Main {
  public main() {
    let foo: string = "Hello World!";
    let bar: int = 100;
  }
}
```


#### Class instantiation

In order to instantiate a class the `new` keyword should be used followed by the name of the class.

```
Class Foo {
  public let bar: string;

  public Foo(bar: string) {
    @bar = bar;
  }
}

Class Main {
  public Main() {
    let fooInstance: Foo = new Foo("Hello World!");
  }
}
```

By default Otter programming language will look for a method with a name that matches the class name, and will call it as the constructor. Additionally it is possible to not have classes without a constructor but with attributes, these classes cannot be instantiated.

### Member functions

Member functions have to be declared within a class by using the `public` or `private` access modifiers followed by the `def` keyword, the name of the function and the return type. In case that a function does not return a value use the `void` keyword as the return type.


```
Class Foo {
  public def publicBar(): string {
    return "This is a public function!";
  }

  private def privateBar(): string {
    return "This is a private function!";
  }
}
```

#### Returns in function

In order to return a value in a function use the `return` keyword followed by any valid expression

```
Class Foo {
  public def bar(): float {
    return 3.14159
  }
  .
  .
  .
}
```

#### Parameters in a function

Parameters within a function can be defined by following the parameter name by its type. The following block shows an example of it.

```
Class Foo {
  public let a: int;
  public let b: string;
  public let c: float;

  public def bar(a: int, b: string, c: float) {
    @a = a;
    @b = b;
    @c = c;
  }
}
```

### Multidimensional variables

Variables with multiples dimensions can be declared using `[<int_constant>]`. For example to declare an array of int use `let a: int[10]`, additionally variables can have infinite dimensions. For example to declare a matrix use `let b: int[10][5]`. Once a dimensional variable is declared its type and size cannot be changed.

All the elements in multidimensional variables are indexed from zero up to n - 1. To access a value from a dimension variable do
```
  a[6] = 900;
```

Aditionally Otter also supports creating multidimensional variables with
custom types. The following example illustrates this scenario.
```
Class Foo{
  public let bar: string;
  public Foo() {
    @bar = "Hello";
  }

  public printBar() {
    write(@bar);
  }
}

Class Main {
  public Main() {
    let fooArray: Foo[10];

    let i: int = 0;
    for(i until i < 10 by 1) {
      fooArray[i] = new Foo();
    }

    i = 0;
    for(i until i < 10 by 1) {
      fooArray[i].printFoo();
    }
  }
}
```

### Multidimensional variables as parameters

In order to pass a multidimensional variable as a parameter in a function use the following syntax.

```
Class Main {
  public def foo(array: int[10], matrix: int[10][5]) {

  }

  public Main() {
    let a: int[10];
    let b: int[10][5];

    self.foo(a, b);
  }
}
```

When passing a multidimensional variable as a parameter to a function its dimensions, sizes and types must match. Keep in mind that a new copy of the variable is created for each method call when passing the multidimensional variable as parameter.

### Conditionals

Otter language defines two different ways to perform conditions. Keep in mind that Otter uses `truthy` and `falsy` to represent boolean primitives.

```
let condition: bool = truthy;

if (condition) {
    write("The condition evaluated to true.")
}

unless (condition) {
  write("The condition evaluated to false.")
}
```

Aditionally else statement can be included in if statements.

```
let condition: bool = falsy;

if (condition) {
  write("The condition evaluated to true.")
}
else {
  write("The condition evaluated to false.")
}
```

Finally elseif clause can be use to have multiple conditions in the same
if statement.

```
let i: int = 10;

if (i == 10) {
    write("i is equal to 10");
}
elseif(i > 10) {
    write("i is greater than 10");
}
else {
    write("Oops. It seems that no condition was fulfilled :( .");
}
```

### Loops

#### For loop

For loops can be defined using the following syntax.

```
let i: int = 0
for(i until i < 5 by 1) {
  write(i);
}
```

Aditionally more complex expressions can be used to increment the
iterator.

```
let i: int = 0
let f: int = 10;
for(i until i < 500 by f * 10 - 20) {
  write(i);
}
```

#### While loop

While loops can be declared using the following syntax.

```
let i: int = 0;

while(i < 100){
    write(i);
    i = i + 1;
}
```

### Input and Output

#### read

Reading from the console is possible using `read` keyword, keep in mind
that eveything will be read as string.

```
let input: string = "Hi";
input = read();
```

#### write

Write function prints the provided expression to console.

```
write("Wooh, I am being printed on the console.");
```

### Inheritance

Since Otter is a Object Oriented Programming language it supports single
inheritance. This means that all method and attributes declared in the
super class will be available on the child class. To use inheritance use
`inherits` keyword followed by the name of the parent class.


```

Class Animal {
  public let sound: string;
  public let name: string;
}

Class Dog inherits Animal {
  public let breed: string;

  public Dog(name: string) {
    @sound = "woof";
    @name = name;
    @breed = "unknown";
  }

  public def getInfo(): void {
    write(@sound);
    write(@name);
    write(@breed);
  }
}

Class Yorkshire inherits Dog {
  public Yorkshire(name: string) {
    @sound = "woof woof";
    @name = name;
    @breed = "yorkshire";
  }
}

Class Main {
  public Main() {
    let dog: Dog = new Dog("my dog");
    let yorkie: Yorkshire = new Yorkshire("yorkshire");

    dog.getInfo();
    write("-------");
    yorkie.getInfo();
  }
}

```
