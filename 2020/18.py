import re
from pathlib import Path


# Part 1

def tokenize(expression: str) -> list[str]:
    token_pattern = re.compile(r'^\s*(\d+|[+\-*/()])')
    tokens = []
    while expression:
        match = token_pattern.match(expression)
        next_token = match.group(1)
        expression = expression.removeprefix(match.group(0))
        tokens.append(next_token)
    return tokens


def convert_to_postfix(tokens: list[str], high_precedence: str = '*/') -> list[str]:
    # Shunting yard algorithm (without operator precedence)
    queue = []
    stack = []
    for token in tokens:
        if token.isnumeric():
            queue.append(token)
        elif token in '+-*/':
            # Keep left-to-right precedence by emptying the operators from the queue
            while stack and stack[-1] in high_precedence:
                queue.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while (top := stack.pop()) != '(':
                queue.append(top)
    while stack:
        queue.append(stack.pop())
    return queue


def evaluate_postfix(tokens: list[str]) -> int:
    stack = []
    for token in tokens:
        if token.isnumeric():
            stack.append(token)
        else:
            arg1, arg2 = int(stack.pop()), int(stack.pop())
            if token == '+':
                stack.append(arg2 + arg1)
            elif token == '-':
                stack.append(arg2 - arg1)
            elif token == "*":
                stack.append(arg2 * arg1)
            elif token == "/":
                stack.append(arg2 // arg1)
    return stack.pop()


input_path = Path("input") / "18.txt"
with input_path.open() as f:
    expressions = [line.strip() for line in f]

print(sum(evaluate_postfix(convert_to_postfix(tokenize(expression), '+-*/')) for expression in expressions))


# Part 2
print(sum(evaluate_postfix(convert_to_postfix(tokenize(expression), '+-')) for expression in expressions))
