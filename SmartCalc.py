
class SmartCalc:

    def __init__(self):
        self.digits = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
        self.operators = {'+', '-', '*', '/', '^'}
        self.var_storer = {}

    def assignment_check(self, before_eq, after_eq) -> None:
        """
        Checks that the RHS (after_eq) of an assignment to a variable is valid.

        """
        self.invalid_assign = {'=', '*', '/', '(', ')', '^'}
        self.first_char = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '+', '.'}
        self.op_checker = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'}

        # Sanitise Input after the equals sign.
        # After equals sign is a variable reference.
        if (not after_eq or any(x in after_eq for x in self.invalid_assign)) or\
            (after_eq[0].isalpha() and not after_eq.isalpha()):
            print("Invalid assignment")
        elif after_eq.isalpha():
            if after_eq in self.var_storer:
                self.var_storer[before_eq] = self.var_storer[after_eq]
            else:
                print("Unknown variable")
        # After equals sign is an operation.
        elif after_eq[0] in self.first_char:
            if len(after_eq) == 1:
                if after_eq in {'-', '+', '.'}:
                    print("Invalid assignment")
                else:
                    self.var_storer[before_eq] = float(after_eq)
            else:
                if after_eq.count('.') > 1:
                    print("Invalid assignment")
                else:
                    for i, _char in enumerate(after_eq[1:]):
                        if _char not in self.op_checker:
                            print("Invalid assignment")
                            return
                        elif i == len(after_eq[1:]) - 1:
                            self.var_storer[before_eq] = float(after_eq)
            
    @staticmethod
    def is_valid_brackets(user_input: str) -> bool:
        """
        For a given string, checks whether:
        1) There are an equivalent number of open and closed brackets
        2) If they are used in a correct order. e.g.  )( does not make sense.
        """

        if user_input.count('(') != user_input.count(')'):
            return False
        # Checks if brackets are used in proper order
        open_br_stack = [i for i, x in enumerate(user_input) if x == "("]
        closed_br_stack = [i for i, x in enumerate(user_input) if x == ")"]
        for i in range(len(open_br_stack)):
            if open_br_stack[i] > closed_br_stack[i]:
                return False
        return True

    def to_single_operators(self, user_input: str) -> str:
        """
        For a given string, this function:
        1) Removes operators from the end of the string
        2) Converts multiple +'s & -'s into a single operator. e.g. -- -> + & +- -> -.
        3) Removes any whitespace.
        """
        
        # remove operators from the end
        while user_input[-1] in self.operators:
            user_input = user_input[:-1]
        # converts consecutive +'s and -'s to single operator  
        end = len(user_input)
        for x in range(len(user_input) - 1):
            curr = user_input[x]
            next = user_input[x + 1]
            if (curr == '+' and next == '+') or (curr == '-' and next == '-'):
                user_input = user_input[0:x] + ' +' + user_input[x + 2:end]
            elif (curr == '+' and next == '-') or (curr == '-' and next == '+'):
                user_input = user_input[0:x] + ' -' + user_input[x + 2:end]
        return user_input.replace(' ', '')

    def infix_to_postfix(self, infix_str: str) -> str:
        """
        ----------------- Infix to Postfix Conversion Algorithm ---------------
        1. Add operands (numbers and variables) to the result (postfix notation) as they arrive.
        2. If the stack is empty or contains a left parenthesis on top, push the incoming operator on the stack.
        3. If the incoming operator has higher precedence than the top of the stack, push it on the stack.
        4. If the incoming operator has lower or equal precedence than or to the top of the stack,
           pop the stack and add operators to the result until you see an operator that has a smaller precedence or
           a left parenthesis on the top of the stack; then add the incoming operator to the stack.
        5. If the incoming element is a left parenthesis, push it on the stack.
        6. If the incoming element is a right parenthesis, pop the stack and add operators to the result until you see
           a left parenthesis. Discard the pair of parentheses.
        7. At the end of the expression, pop the stack and add all operators to the result.
        """
        postfix = ''
        stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

        # Steps refer to the algorithm
        for i, x in enumerate(infix_str):
            # Step 1
            if x in self.digits or x.isalpha():
                try:
                    if infix_str[i+1] in self.digits or infix_str[i + 1].isalpha():
                        postfix += x
                    else:
                        postfix += x + ' '
                except IndexError:
                    postfix += x + ' '
            elif x in self.operators:
                # if first num is < 0
                if (i == 0 and infix_str[i + 1] in self.digits) or (i == 0 and infix_str[i + 1].isalpha()):
                    postfix += x
                # Step 2
                elif len(stack) == 0 or (len(stack) > 0 and stack[-1] == '('):
                    stack.append(x)
                # Step 3
                elif precedence[x] > precedence[stack[-1]]:
                    stack.append(x)
                # Step 4
                else:
                    while True:
                        postfix += stack.pop() + ' '
                        if len(stack) == 0 or precedence[x] > precedence[stack[-1]]:
                            stack.append(x)
                            break
            # Step 5
            elif x == '(':
                stack.append(x)
            # Step 6
            elif x == ')':
                while stack[-1] != '(':
                    postfix += stack.pop() + ' '
                stack.pop()
        # Step 7
        stk_len = len(stack)
        while stk_len > 0:
            postfix += stack.pop()
            if stk_len != 1:
                postfix += ' '
            stk_len -= 1

        return postfix

    def calculate_result(self, postfix_str: str) -> str:
        """
        # -------- Calculate result from Postfix Notation ----------
        # 1. If the incoming element is a number, push it into the stack (the whole number, not a single digit).
        # 2. If the incoming element is the name of a variable, push its value into the stack.
        # 3. If the incoming element is an operator, then pop twice to get two numbers and
        #      perform the operation; push the result on the stack.
        # 4. When the expression ends, the number on the top of the stack is a final result.
        """
        stack = []
        num_storer = ''

        for i, x in enumerate(postfix_str):
            if x in self.digits or (i == 0 and postfix_str[i] == '-'):
                if postfix_str[i + 1] in self.digits:
                    num_storer += x
                else:
                    num_storer += x
                    stack.append(float(num_storer))
                    num_storer = ''
            # if char a-z/A-Z (variable)
            elif x.isalpha() or (i == 0 and postfix_str[i] == '-'):
                if postfix_str[i + 1].isalpha():
                    num_storer += x
                else:
                    num_storer += x
                    stack.append(float(self.var_storer[num_storer]))
                    num_storer = ''
            # if char is operator
            elif x in self.operators:
                fp = stack.pop()
                sp = stack.pop()
                if x == '+':
                    stack.append(sp + fp)
                elif x == '-':
                    stack.append(sp - fp)
                elif x == '*':
                    stack.append(sp * fp)
                elif x == '/':
                    stack.append(sp / fp)
                elif x == '^':
                    stack.append(sp ** fp)
        return "%g" % stack.pop()

    def main(self):
        while True:
            inp = input().replace(' ', '')
            equals_index = inp.find('=')

            # no input
            if not inp:
                continue
            # forwardslash commands
            elif inp[0] == '/':
                if inp == '/help':
                    print("This is a smart calculator.")
                    print("It supports the following operators: '+', '-', '*', '/', '^' ")
                    print("You can also set variables for later use with the '=' operator")
                    print("Variable names must be strictly alphabetical utf-8")
                    print("It supports the proper order of operations by converting to postfix notation")
                    print("To clear all previously stored variables, type /clear")
                    print("To check all currently stored variables, type /currvars")
                elif inp == '/clear':
                    self.var_storer = {}
                    print('Variable storage has been reset')
                elif inp == '/currvars':
                    for key in self.var_storer:
                        print('%s: %g' % (key, self.var_storer[key]), end='  ')
                elif inp == '/exit':
                    break
                else:
                    print('/help for overview and /exit to stop the program')
            # equals sign in input
            elif equals_index != -1:
                proc_inp = self.to_single_operators(inp)
                self.assignment_check(proc_inp[0:equals_index], proc_inp[equals_index + 1: len(proc_inp)])
            # no equals sign in input
            else:
                # input is a-z/A-Z (retrieve variable)
                if inp.isalpha():
                    try:
                        print('%g' % self.var_storer[inp])
                    except KeyError:
                        print("No such variable exists")
                # input is not a-z/A-Z (process a calculation)
                else:
                    processed_inp = self.to_single_operators(inp)
                    postfix = self.infix_to_postfix(processed_inp)
                    try:
                        result = self.calculate_result(postfix)
                        print(result)
                    except IndexError:
                        print("Invalid Expression")
                    except KeyError:
                        print("No such variable exists")


if __name__ == '__main__':
    calc = SmartCalc()
    calc.main()
