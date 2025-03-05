import re
import numpy as np
class ExParser:
    """A class for parsing and evaluating mathematical expressions."""

    def __init__(self):
        """Initialize the ExParser object with a dictionary of operators and their priorities."""
        self.operators = {
            '+': (1, lambda x, y: x + y),
            '-': (1, lambda x, y: x - y),
            '*': (2, lambda x, y: x * y),
            '/': (2, lambda x, y: x / y),
            '^': (3, lambda x, y: x ** y),
            'sin': (4, np.sin),
            'cos': (4, np.cos),
            'tan': (4, np.tan),
            'sqrt': (4, np.sqrt),
        }
    
    def makeTokens(self, expression, poly_value):
        """
        Method to make tokens (operators or operands) from the string.

        Parameters:
            expression (str): String of mathematical expression.
            poly_value (float): Value of the polynomial.

        Returns:
            list: Array of tokens.
        """        
        tokens = []
        current_token = ''
        matrix_pattern = re.compile(r'[A-Z][A-Z0-9]*')  # Matrix identifier pattern (capital letters)
        trig_functions = {'sin', 'cos', 'tan', 'sqrt'}  # Set of trigonometric functions
        # Looping through each charater of string for making tokens
        for char in expression:
            # identification and grouping of character to make intger, polynomial or decimal number
            if char.isdigit() or char == '.':
                current_token += char
            elif char.isalpha():
                current_token += char
            else:
                if current_token:
                    if self.is_float(current_token):
                        tokens.append(float(current_token))
                    elif matrix_pattern.match(current_token): 
                        # Recognize matrix identifier and store as a string
                        tokens.append(current_token)
                    elif current_token.lower() in trig_functions:
                        tokens.append(current_token.lower())  # Convert trig functions to lowercase
                    else:
                        tokens.append(poly_value if current_token == 'x' else 0)  # setting polynomial with its value
                    current_token = ''
                if char.strip():
                    tokens.append(char)
        # Adding token in the token array.
        if current_token:
            if current_token.isnumeric():
                tokens.append(float(current_token))
            elif matrix_pattern.match(current_token):
                tokens.append(current_token)
            elif current_token.lower() in trig_functions:
                tokens.append(current_token.lower())  # Convert trig functions to lowercase
            else:
                tokens.append(poly_value if current_token == 'x' else 0) # setting polynomial with its value

        return tokens
    
    def parseExpression(self, expression, matrix_values,poly_value = 0):
        """
        Method to convert infix expression to postfix expression and evaluate the result.

        Parameters:
            expression (str): String of mathematical expression.
            matrix_values (dict): Dictionary of matrices.
            poly_value (float): Value of the polynomial.

        Returns:
            float: Result of the expression.
        """
        output_queue = []
        matrix_pattern = re.compile(r'[A-Z][A-Z0-9]*')
        operator_stack = []
        tokens = self.makeTokens(expression, poly_value) # making tokens from the expression
         # looping through all the tokens to convert infix expression to postfix expression using shunting yard algorithm
        for token in tokens:
            if isinstance(token, float) or isinstance(token, int):
                output_queue.append(token)
            elif matrix_pattern.match(token):
                output_queue.append(matrix_values[token])
            elif token in self.operators:
                while (
                    operator_stack
                    and operator_stack[-1] in self.operators
                    and self.operators[operator_stack[-1]][0] >= self.operators[token][0]
                ):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                operator_stack.pop()
            #elif token in {'sin', 'cos', 'tan'}:  # Added trigonometric functions handling
             #   operator_stack.append(token)
        while operator_stack:
            output_queue.append(operator_stack.pop()) #
        return self.evaluatePostfixExp(output_queue) # evaluating postfix expression
    def evaluatePostfixExp(self, postfix_tokens):
        """
        Method to solve the postfix expression and return the calculated result.

        Parameters:
            postfix_tokens (list): List of postfix tokens.

        Returns:
            float: Calculated result.
        """
        operand_stack = []
        # looping through all the postfix tokens
        for token in postfix_tokens:
             # identifing token if it is an operand
            if isinstance(token, float) or isinstance(token, int) or isinstance(token,np.ndarray):
                operand_stack.append(token) # adding it in operand stack
            elif token in self.operators: # identifing if the token is operator
                if token in {'sin', 'cos', 'tan', 'sqrt'}:
                    op1 = operand_stack.pop()
                    result = self.operators[token][1](op1)
                else:
                    #poping operends for calculation.
                    op2 = operand_stack.pop() 
                    op1 = operand_stack.pop()
                    # if operend is array token is * take dot product
                    if ((isinstance(op1,np.ndarray) or isinstance(op2,np.ndarray)) and token == '*'):
                        result = np.dot(op1,op2)
                    else:     
                        # calculating operend and adding it back in stack
                        result = self.operators[token][1](op1, op2) 
                operand_stack.append(result)
        return operand_stack[0]
    def is_float(self,string):
        """
        Check if the given string is a float.

        Parameters:
            string (str): Input string.

        Returns:
            bool: True if the string is a float, False otherwise.
        """
        # Removing decimal point and then Validate the value by parsable into numeric.
        if string.replace(".", "").isnumeric():
            return True
        else:
            return False
    def is_root_of_CP(self,matrix):
        """
        Check if the given string is a root of its characterstics polynomial.

        Parameters:
            A numpy matrix.

        Returns:
            bool: True if the matrix is a root of its polynomial, False otherwise.
        """
        # Computing thec characteristic Polynomial
        characteristic_poly = np.poly(matrix)

        # Computing the roots of the polynomial
        polyRoots = np.roots(characteristic_poly)

        # puting root values in in matrix
        for root in polyRoots:
            # computing  the determinant matrix
            modified_matrix = matrix - root * np.identity(matrix.shape[0])
            # Check if the determinant is zero (matrix is singular)
            det = np.linalg.det(modified_matrix)
            if np.isclose(det, 0):
                return True

        # If none of the matrices are singular, return False
        return False