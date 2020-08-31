# Smart Calculator

## Overview
Smart Calculator converts an input string to a calculation with the correct order of operations intact i.e. BIDMAS. This does not provide much new use to python, especially because of the existance of eval(), but it does provide the fundamental theory of some of the work that a calculator does.

It is common practice to write and read equations in infix notation, i.e. __5+5__. However, as the number of operators and operands piles up, it becomes especially hard to program something that fully incorporates BIDMAS. A good example of this is __2 + 3 * 4__. By BIDMAS, this is __2 + 12 = 14__ . But a classical problem in infix notation would be that the program would calculate the addition first, giving us the false answer of __5 * 4 = 20__ .

## Algorithms Used

__Infix to Postfix Conversion Algorithm__ 
1. Add operands (numbers and variables) to the result (postfix notation) as they arrive.
2. If the stack is empty or contains a left parenthesis on top, push the incoming operator on the stack.
3. If the incoming operator has higher precedence than the top of the stack, push it on the stack.
4. If the incoming operator has lower or equal precedence than or to the top of the stack, pop the stack and add operators to the result until you see an operator that has a smaller precedence or a left parenthesis on the top of the stack; then add the incoming operator to the stack.
5. If the incoming element is a left parenthesis, push it on the stack.
6. If the incoming element is a right parenthesis, pop the stack and add operators to the result until you see a left parenthesis. Discard the pair of parentheses.
7. At the end of the expression, pop the stack and add all operators to the result.

__Calculate result from Postfix Notation__
1. If the incoming element is a number, push it into the stack (the whole number, not a single digit!).
2. If the incoming element is the name of a variable, push its value into the stack.
3. If the incoming element is an operator, then pop twice to get two numbers and perform the operation; push the result on the stack.
4. When the expression ends, the number on the top of the stack is a final result.

## Function Overview

**All functions below use strings as input**

**before_eq** - variable before equals sign         
**after_eq** - variable or float/int after equals sign (strictly no calculations here)  
This function checks that everything before and after the equals sign is correct, i.e. no invalid characters. It will also set the variable to the variable dictionary.
```python
def assignment_check(before_eq, after_eq):
    pass
```

If input has brackets, it checks that they are ordered correctly and each opening bracket has a corresponding closing bracket.  
```python
def is_valid_brackets(user_input):
    pass 
```

If input has multiple consecutive + or -, it converts to correct operator. e.g. **- 5 - - + 10 ----> - 5 + 10**  
```python
def to_single_operators(user_input):
    pass
```

This function uses the the infix to postfix algorithm above to convert an infix form calculation to a postfix form.
```python
def infix_to_postfix(infix_str):
    pass
```

This function calculates a result from postfix notation.
```python
def calculate_result(postfix_str):
    pass
```
