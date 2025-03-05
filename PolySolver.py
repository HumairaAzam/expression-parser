import re
import numpy as np
from sympy import sympify, collect
import sympy as sp
import PolySolver as ps
class PolySolver:
    """A class for solving polynomial equations and finding roots."""      
    def polynomial_degree(self,poly_str):
        """
        Find the degree of a polynomial.

        Parameters:
            poly_str (str): String representation of the polynomial.

        Returns:
            int or str: Degree of the polynomial or an error message if the polynomial is not valid.
        """
        # Reqular expression to extract terms from polynomial string
        term_pattern = re.compile(r'([+-]?\s*\d*\s*x(\^\d+)?)') 
        # get the list of individual that matches
        terms = re.findall(term_pattern, poly_str)
        if not terms:
            return "Not a valid polynomial."
        # Finding the highest power from the array of terms
        degree = 0
        # Looping through all the terms of polynomial
        for term in terms:
            matched_power = re.search(r'\^(\d+)?', term[0]) # Extracting the group of digits after the caret symbol
            # Check if matched power has an integer value else return 1 because degree of x is 1 
            if matched_power:
                power = int(matched_power.group(1)) 
            else:
                power = 1
            degree = max(degree, power) # saving the highest power in degree variable
        return degree        
    def compute_derivative(self,coefficients):
        """
        Compute the derivative of a polynomial.

        Parameters:
            coefficients (list): Coefficients of the polynomial.

        Returns:
            list: Coefficients of the derivative polynomial.
        """
        # Compute the derivative of the polynomial
        #derivative_coefficients = [i * coef for i, coef in enumerate(coefficients, start=1)][1:]
        coefficients = coefficients[::-1]
        if not coefficients:
            return [0]

        # Calculate the derivative
        derivative_coefficients = [i * coefficients[i] for i in range(1, len(coefficients))]
        derivative_coefficients = derivative_coefficients[::-1]
        return derivative_coefficients  
    def find_linear_roots(self,coefficients):
        """
        Find the roots of a linear equation.

        Parameters:
            coefficients (list): Coefficients of the linear equation.

        Returns:
            list: List of roots.
        """
        # Ensure that the coefficients list has at least two elements
        coefficients = self.remove_leading_zeros(coefficients)
        if len(coefficients) < 2:
            raise ValueError("Insufficient coefficients for a linear equation")
        a = coefficients[0]
        b = coefficients[1]
        # For a linear equation (ax + b = 0)
        if a != 0 and b != 0:
            root_linear = -b / a
            return [root_linear]
        elif a == 0 and b == 0:
        # Invalid coefficients (both a and b are zero)
            return []
    def find_quadratic_roots(self,coefficients):
        """
        Find the roots of a quadratic equation.

        Parameters:
            coefficients (list): Coefficients of the quadratic equation.

        Returns:
            list: List of roots.
        """
        # Ensure that the coefficients list has at least two elements
        if len(coefficients) < 3:
            raise ValueError("Insufficient coefficients for a linear equation")
        coefficients = self.remove_leading_zeros(coefficients)
        a = coefficients[0]
        b = coefficients[1]
        c = coefficients[2]
    # For a quadratic equation (ax^2 + bx + c = 0)
        if a != 0:
            discriminant = b**2 - 4*a*c

        if discriminant > 0:
            root1 = (-b + (discriminant)**0.5) / (2*a)
            root2 = (-b - (discriminant)**0.5) / (2*a)
            return [root1, root2]
        elif discriminant == 0:
            root_real = -b / (2*a)
            return [root_real]
        else:
            # Complex roots
            root_real_part = -b / (2*a)
            root_imag_part = (abs(discriminant))**0.5 / (2*a)
            root1 = complex(root_real_part, root_imag_part)
            root2 = complex(root_real_part, -root_imag_part)
            return [root1, root2]
    def extract_coefficients(self,expression_str, variable='x'):
        """
        Extract coefficients from a polynomial expression.

        Parameters:
            expression_str (str): String representation of the polynomial expression.
            variable (str): Variable to collect coefficients for (default is 'x').

        Returns:
            list: Coefficients of the polynomial.
        """
        # Parse the expression
        expression = sympify(expression_str)
        # Collect terms based on the variable
        collected_expression = collect(expression, variable)
        # Extract coefficients from the collected expression
        coefficients = [collected_expression.coeff(variable, degree) for degree in range(3, -1, -1)]
        
        return coefficients
    def find_roots(self,expression_str):
        """
        Find the roots of a polynomial expression.

        Parameters:
            expression_str (str): String representation of the polynomial expression.

        Returns:
            list: List of roots.
        """
        coefficient = self.extract_coefficients(expression_str)
        degree = self.polynomial_degree(expression_str)
        if degree  == 1:
            roots = self.find_linear_roots(coefficient)
        elif degree == 2: 
            roots = self.find_quadratic_roots(coefficient)
        elif degree >= 3: 
            roots = np.roots(coefficient);
        return roots
    def remove_leading_zeros(self,arr):
        """
        Remove leading zeros from a list.

        Parameters:
            arr (list): Input list.

        Returns:
            list: List with leading zeros removed.
        """
        # Find the index of the first non-zero element
        first_non_zero_index = next((i for i, x in enumerate(arr) if x != 0), len(arr))
        # Remove leading zeros
        result = arr[first_non_zero_index:]
        return result
    def polynomial_degree(self,poly_str):   
        """
        Find the degree of a polynomial.

        Parameters:
            poly_str (str): String representation of the polynomial.

        Returns:
            int or str: Degree of the polynomial or an error message if the polynomial is not valid.
        """
        # Reqular expression to extract terms from polynomial string
        term_pattern = re.compile(r'([+-]?\s*\d*\s*x(\^\d+)?)') 

        # get the list of individual that matches
        terms = re.findall(term_pattern, poly_str)

        if not terms:
            return "Not a valid polynomial."

        # Finding the highest power from the array of terms
        degree = 0
        # Looping through all the terms of polynomial
        for term in terms:
            matched_power = re.search(r'\^(\d+)?', term[0]) # Extracting the group of digits after the caret symbol
            # Check if matched power has an integer value else return 1 because degree of x is 1 
            if matched_power:
                power = int(matched_power.group(1))
                
            else:
                power = 1
            degree = max(degree, power) # saving the highest power in degree variable
        return degree    
    def coffExp(self,coefficients, variable='x'):
        """
        Create a polynomial expression from an array of coefficients.

        Parameters:
            coefficients (list): List of coefficients.
            variable (str): Variable symbol (default is 'x').

        Returns:
            str: Polynomial expression.
        """
        degree = len(coefficients) - 1
        expression = ''

        for i, coef in enumerate(coefficients):
            if coef != 0:
                term = f"{coef}{'*' + variable if i < degree else ''}"
                if degree - i > 1:
                    term += f"^{degree - i}"
                expression += term + ' + '

        return expression.rstrip(' + ')
    def calcExpDerivative(self,exp):
        """
        Calculate the derivative from the expression.

        Parameters:
            polynomial Expression.

        Returns:
            resultant polynomial expression.
        """
        coff = self.extract_coefficients(exp) # extract the cofficient of expression
        coff = self.remove_leading_zeros(coff) # remove the leading 0 from the expressions
        result = self.compute_derivative(coff) # find the derivatve of expression
        return self.coffExp(result) # return the expression from the derivative response
    def compute_jacobian_matrix(self,x,y,f,g):
        """
        Calculate the jacobian matrix for the functions matrix

        Parameters:
        x = varible for calculation
        y = variable for calculation
        f : function of x
        g : function of y

        Returns:
            jacobian matrix
        """
        
        # Compute partial derivatives
        df_dx = sp.diff(f, x)
        df_dy = sp.diff(f, y)
        dg_dx = sp.diff(g, x)
        dg_dy = sp.diff(g, y)

        # Construct the Jacobian matrix
        J = sp.Matrix([[df_dx, df_dy], [dg_dx, dg_dy]])

        return J
