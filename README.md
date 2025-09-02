# Merriment

Merriment is a 2D stack-based programming language, inspired by Befunge and similar languages. Merriment asks the question: what if you could define new commands using the language itself? To that end, Merriment has 2 features not present in most fungeoids: code is written in multiple codeboxes which can call each other with single-character commands, and there is a velocity stack which can be used to manipulate the velocity of the IP.

## Usage
`python3 Merriment.py program` (file name is `program.merry`)

## Codeboxes
Here is an example of a codebox:
```
#######
# foo #
#v====#
#>123@#
#######
```
The name of this codebox is `foo`. (Leading and trailing spaces in the name are ignored.) The IP (Instruction Pointer) starts from the `v` in the line below the name and continues downward. (Note that the `v` can be anywhere in the line of equals signs, not just the left.) As you might expect, the `>` command redirects the instruction pointer toward the right. Then, 1, 2, and 3 are pushed onto the stack. Finally, the IP hits the `@` symbol, which returns control to whatever codebox called `foo`.

How do you call a codebox? Using the first character in its name. So, to call `foo`, use the `f` command. Suppose we have this codebox in the same file:
```
########
#      #
#v=====#
#>f++o@#
########
```
This codebox has an empty name, making it the "main codebox". When the program is run, this codebox will be called. First, it calls `foo`, which pushes 1, 2, and 3. Then these values are added together, resulting in 6. The `o` command prints ASCII character 6 (ACK), and finally the `@` command causes the program to terminate.

## Data Stack and Velocity Stack
There are two stacks that are used to hold data. Both can hold arbitrarily sized integers. One of them is the *data stack*, as seen in the previous example. The other is the *velocity stack*. When a codebox is called, the velocity of the instruction pointer is pushed to the velocity stack: first the x component, then the y component. After returning from the call, the components are popped again in the reverse order, possibly changing the IP's velocity. (Note that if the velocity stack is left untouched, the velocity remains the same after the call.)

Notably, even the arrows (`<>^v`) are defined in this way, rather than being base commands implemented directly into the interpreter.

The velocity stack can also be used as an extra place to store data. You can see it being used that way in some of the codeboxes in the standard library.

## Imports
To import another file, you need an import statement on its own line like this: `{file}` This will look for a file called `file.merry` in the same folder as the interpreter and import all of its codeboxes.

In general, `{stdlib}` is recommended, because it imports `{arrows}` and also contains a few useful commands.

## Comments
Anything outside of a codebox that is not an import statement will be considered a comment and ignored. Comments can also be written inside codeboxes, as long as you ensure the IP never reaches them.

## Commands
### Base commands
|Command|Function|
|--|--|
|0-9|Push value to the data stack|
|↊|Push 10|
|↋|Push 11|
|+|Pop a, pop b, push a+b|
|-|Pop a, pop b, push b-a|
|*|Pop a, pop b, push a*b|
|,|Pop a, pop b, push floor(b/a) (Errors on division by 0)|
|`|Is positive: pop value, then push 1 if it's positive, or 0 otherwise|
|:|Duplicate|
|.|Pop|
|~|Swap|
|{|Move value from velocity stack to data stack|
|}|Move value from data stack to velocity stack|
|@|Return|
|"|Toggle string mode|
|i|Input character (-1 on EOF)|
|o|Output character|
|!|Debug: Print message containing current codebox, position, velocity, and contents of both stacks|
### Commands in {stdlib} + {arrows}
|Command|Function|
|--|--|
|>|Right: Set velocity to 1,0|
|<|Left: Set velocity to -1,0|
|v|Down: Set velocity to 0,1|
|^|Up: Set velocity to 0,-1|
|%|Modulo: Pop a, pop b, push b%a|
|(|Less Than: Pop a, pop b, then push 1 if b<a or 0 otherwise|
|)|Greater Than: Pop a, pop b, then push 1 if b>a or 0 otherwise|
|=|Equals: Pop a, pop b, then push 1 if b=a or 0 otherwise|
|_|Horizontal If: Pop value, then go right if it's positive, or left if it's non-positive.|
|\||Vertical If: Pop value, then go down if it's positive, or up if it's non-positive.|
|b|boost: Pop value and multiply IP velocity by it.|
|p|print: Print a string from the stack terminated by a non-positive value.|
|r|rot: a b c -> b c a|
|g|get: Pop n, then push the nth item from the top of the stack (0-indexed). If n is negative, get the 0th item.|
|s|set: Pop n, pop x, then set the nth item from the top of the stack to x (0-indexed). If n is negative, set the 0th item.|
|?|Signpost: Pop value, then change velocity depending on its sign: If it's positive, rotate 90 degrees clockwise. If it's 0, leave velocity unchanged. If it's negative, rotate 90 degrees counter-clockwise.|
|n|num->str: Pop number, then push its string representation, terminated by 0.|
### Other modules
* {number}: More math functions
* {shmove}: More IP movement options