# CF_and_CS_grammars_comparsion

Comparsion of context-free and context-sensitive grammars for development and creation the new programming languages

## Usage

You can find the examples of programmes in **examples** directory. In order to execute script you should choose mode (CF or CS: context free an context sensitive respectively) of execution as a first argument and path to the executable file as the second one. Example is below:

```sh
git clone https://github.com/mmkuznecov/CF_and_CS_grammars_comparsion
cd CF_and_CS_grammars_comparsion/src
python3 main.py -m CF -f ../bubble_sort.rlang
```

## Features

Language currently supporting:

* Math (+ - * / %), logical and bitwise operations

* Variables of different types (int, float, string, list, dict)

* If statements

* While and for loops

* Functions

The info will be updated along with adding the new functionality.

## Language syntax

Firstly, all statements end with colon

Comment section starts with double slash:

```java
// comment example
```

Output section provided with **print** keyword:

```java
print("Hello world!")
```

Variables are defined with the **let** keyword:

```java
let a: int;
let b = 10;
```

You can assign value along with variable declaration as you can see above.

Language provides working with math, logical and bitwise operations:

```java
let a = 10 * 2 + 3; // value of a is 23 because there is a precedence of operations
let b = true or false; // value of b is true
let c = 1 & 0; // value of c is 0
```

Next main constructions will be described with the examples:

**If** statement example:

```java
let a = 10;
if a > 5{
    print("var is greater than 5");
}
else {
    print("var is less than 5"); 
}

// first statement will be printed
```

**For** loop example:

```java
let break = false; // just a var
let i: int;

for i = 0; i < 10 and !break; ++i {
  if i % 2 == 0 or i < 2 {
    print(i);
  }
  if i > 4 
    break = true;
}

// following programm will print numbers 0 1 2 4
```

**While** loop example:

```java
let i = 1;

while i <= 10{
    print(i);
    i+=1;
}

// programm will print numbers from 1 to 10
```

**Function** example:

```java
let x = 2;
let y = 3;

fn add_numbers (a: int, b: int){
    return a + b;
}

print(add_numbers(x,y));

// 5 will be printed
```

Also language supports function composition. You can find the example of recursion in *factorial_recursion.rlang* file in **examples** directory.

In order to check all keywords and constructions, you can look at the code of lexer and parser at **src** directory.