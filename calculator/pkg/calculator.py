# calculator/pkg/calculator.py

from collections.abc import Callable
import math

class Calculator:
    def __init__(self) -> None:
        self.operators: dict[str, Callable[[float, float], float]] = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "^": lambda a, b: a ** b,
        }
        self.unary_functions: dict[str, Callable[[float], float]] = {
            "log2": math.log2,
        }
        self.postfix_unary_operators: dict[str, Callable[[int], int]] = {
            "!": math.factorial,
        }

        # Precedence for binary operators
        self.precedence: dict[str, int] = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "^": 3,
            # Functions should have higher precedence than binary operators,
            # but their application is driven by parentheses.
        }

    def evaluate(self, expression: str) -> float | None:
        if not expression or expression.isspace():
            return None
        tokens = self._tokenize(expression)
        return self._evaluate_infix(tokens)

    def _tokenize(self, expression: str) -> list[str]:
        import re
        # Tokenize numbers (integers/floats), binary operators, parentheses, 'log2', and '!'
        # This regex ensures `log2(16)` becomes `log2`, `(`, `16`, `)`
        # And `5!` becomes `5`, `!`
        token_pattern = re.compile(r'\d+\.\d+|\d+|\+|\-|\*|\/|\^|\(|\)|log2|\!')
        tokens = [match.group(0) for match in token_pattern.finditer(expression) if match.group(0).strip()]
        return tokens

    def _evaluate_infix(self, tokens: list[str]) -> float:
        values: list[float] = []
        operators: list[str] = []

        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    self._apply_operator(operators, values)
                if not operators or operators[-1] != '(':
                    raise ValueError("mismatched parentheses")
                operators.pop() # Pop the '('

                # After popping '(', check if the operator stack's top is a function.
                if operators and operators[-1] in self.unary_functions:
                    self._apply_operator(operators, values) # Apply the function
            elif token in self.operators: # Binary operators
                while (\
                    operators
                    and operators[-1] != '('
                    and operators[-1] in self.precedence # Ensure operator has precedence defined
                    and self.precedence.get(operators[-1], 0) >= self.precedence.get(token, 0) # Use .get with default 0 for safety
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            elif token in self.unary_functions: # Unary functions like 'log2'
                operators.append(token) # Push function onto operator stack
            elif token in self.postfix_unary_operators: # Postfix unary operators like '!'
                if not values:
                    raise ValueError(f"not enough operands for operator {token}")
                operand = values.pop()
                # Factorial only works for non-negative integers
                if not float(operand).is_integer() or operand < 0:
                    raise ValueError("factorial is only defined for non-negative integers")
                values.append(self.postfix_unary_operators[token](int(operand)))
            else: # Must be a number
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"invalid token: {token}")
            i += 1

        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators: list[str], values: list[float]) -> None:
        if not operators:
            return

        operator = operators.pop()

        if operator in self.unary_functions: # Handle unary functions
            if len(values) < 1:
                raise ValueError(f"not enough operands for function {operator}")
            operand = values.pop()
            values.append(self.unary_functions[operator](operand))
        elif operator in self.operators: # Binary operators
            if len(values) < 2:
                raise ValueError(f"not enough operands for operator {operator}")
            b = values.pop()
            a = values.pop()
            values.append(self.operators[operator](a, b))
        else:
            raise ValueError(f"unknown operator: {operator}")
