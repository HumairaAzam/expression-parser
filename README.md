# Expression-Parser

The expression parser evaluate and process arthematic
and polynomial expressions. The parser take the arthematic expression, matries and
polynomial as string and solve them accordingly to create the valuable output.
The Expression parser is built on python. The python library Numpy is used to
leverage mathematical operations. NumPy’s efficient mathematical operations, including
arithmetic functions like addition, subtraction, multiplication, division, and exponentiation,
are leveraged within the parser. Additionally, NumPy provides essential trigonometric
functions such as ‘sin‘, ‘cos‘, ‘tan‘, and ‘sqrt‘. It is also used in matrix evaluation.
The Shunting Yard algorithm used to convert infix expressions into postfix notation,
ensuring accurate evaluation of arithmetic operations while respecting the order of operations.
The regular expression method helps in identification of operands, operators, and functions
also helps in validating the characters in expression.
The integration of arithmetic operations enables seamless handling of basic mathematical
expressions, ensuring correct evaluation and computation of results. For example, expressions
like "2 + 3 * sin(0)" are parsed and evaluated accurately, maintaining precedence and
yielding correct outcomes.
More over the expression parser also supports the polynomial operations like finding
the roots of polynomial, computing derivative of polynomial or solving the expressions
with the polynomial.

## Components

### ExParser Class

The `ExParser` class facilitates expression evaluation, solution, and basic arithmetic operations.

### PolySolver Class

The `PolySolver` class specializes in solving intricate polynomial problems, such as derivative computation and advanced operations.

### Python Notebook

The accompanying Python notebook (`Polynomial_Expressions.ipynb`) serves as an interactive environment for implementing and testing the functionalities offered by the `ExParser` and `PolySolver` classes.

## Usage

Explore the provided Python notebook (`Polynomial_Expressions.ipynb`) to interactively experiment with and understand the capabilities of the `ExParser` and `PolySolver` classes.

Example usage:
```python
# Import the classes from the module
from polynomial_solver import ExParser, PolySolver

# Create instances of ExParser and PolySolver
parser = ExParser()
solver = PolySolver()

# Evaluate and solve expressions using ExParser methods
result = parser.evaluate_expression('3 * x + 2', x=5)
print("Result:", result)

# Solve polynomial problems using PolySolver methods
derivative = solver.compute_derivative('x**2 + 5*x + 3', var='x')
print("Derivative:", derivative)

## Requirements

- [Python 3.x](https://www.python.org/downloads/): Make sure you have Python 3.x installed on your system.
- [Jupyter Notebook](https://jupyter.org/install): Install Jupyter Notebook to run the provided Python notebook (`Polynomial_Expressions.ipynb`).

Make sure to install the required software before running the project. You can click on the links above to download and install Python 3.x and Jupyter Notebook from their official websites.

