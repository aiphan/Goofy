import re
from dataclasses import dataclass
from typing import List, Union, Dict

@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if text else None
        self.line = 1
        self.column = 1
    
    def error(self):
        raise Exception(f'Invalid character {self.current_char} at line {self.line}, column {self.column}')
    
    def advance(self):
        self.pos += 1
        self.column += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            if self.current_char == '\n':
                self.line += 1
                self.column = 0
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def skip_comment(self):
        while self.current_char and self.current_char != '\n':
            self.advance()
    
    def get_number(self):
        result = ''
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        return float(result) if '.' in result else int(result)
    
    def get_identifier(self):
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result
    
    def get_string(self):
        self.advance()  # Skip opening quote
        result = ''
        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()
        if self.current_char == '"':
            self.advance()
        return result
    
    def get_next_token(self) -> Token:
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char == '#' or (self.current_char == 't' and self.text[self.pos:self.pos+3] == 'tea'):
                if self.current_char == 't':
                    self.pos += 3
                    self.column += 3
                self.skip_comment()
                continue
            
            if self.current_char.isdigit():
                return Token('NUMBER', self.get_number(), self.line, self.column)
            
            if self.current_char.isalpha():
                identifier = self.get_identifier()
                
                # Keywords with GenZ slang
                if identifier == 'bruh':
                    return Token('DECLARE', identifier, self.line, self.column)
                elif identifier == 'itsgiving':
                    return Token('PRINT', identifier, self.line, self.column)
                elif identifier == 'twin':
                    return Token('PLUS', identifier, self.line, self.column)
                elif identifier == 'flop':
                    return Token('MINUS', identifier, self.line, self.column)
                elif identifier == 'thicc':
                    return Token('MULTIPLY', identifier, self.line, self.column)
                elif identifier == 'ratio':
                    return Token('DIVIDE', identifier, self.line, self.column)
                elif identifier == 'gyat':
                    return Token('CONCAT', identifier, self.line, self.column)
                elif identifier == 'lethimcook':
                    return Token('IF', identifier, self.line, self.column)
                elif identifier == 'bet':
                    return Token('THEN', identifier, self.line, self.column)
                elif identifier == 'naur':
                    return Token('ELSE', identifier, self.line, self.column)
                elif identifier == 'bigflex':
                    return Token('GREATER', identifier, self.line, self.column)
                else:
                    return Token('IDENTIFIER', identifier, self.line, self.column)
            
            if self.current_char == '"':
                return Token('STRING', self.get_string(), self.line, self.column)
            
            if self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(', self.line, self.column)
            
            if self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')', self.line, self.column)
            
            if self.current_char == '{':
                self.advance()
                return Token('LBRACE', '{', self.line, self.column)
            
            if self.current_char == '}':
                self.advance()
                return Token('RBRACE', '}', self.line, self.column)
            
            if self.current_char == '=':
                self.advance()
                return Token('ASSIGN', '=', self.line, self.column)
            
            self.error()
        
        return Token('EOF', None, self.line, self.column)

class Interpreter:
    def __init__(self):
        self.variables = {}
    
    def interpret(self, text: str):
        lexer = Lexer(text)
        tokens = []
        
        while True:
            token = lexer.get_next_token()
            tokens.append(token)
            if token.type == 'EOF':
                break
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token.type == 'IF':
                i = self.handle_if_statement(tokens, i)
            elif token.type == 'PRINT':
                i = self.handle_print(tokens, i)
            elif token.type == 'DECLARE':
                i = self.handle_declaration(tokens, i)
            else:
                i += 1
    
    def handle_print(self, tokens, i):
        i += 1
        if i < len(tokens) and tokens[i].type == 'LPAREN':
            i += 1
            value = self.evaluate_expression(tokens[i])
            print(value)
            i += 1
            if i < len(tokens) and tokens[i].type == 'RPAREN':
                i += 1
        else:
            value = self.evaluate_expression(tokens[i])
            print(value)
            i += 1
        return i
    
    def handle_declaration(self, tokens, i):
        i += 1
        var_name = tokens[i].value
        i += 1
        i += 1
        first_value = self.evaluate_expression(tokens[i])
        i += 1
        if i < len(tokens) and tokens[i].type in ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'CONCAT']:
            operator = tokens[i].type
            i += 1
            second_value = self.evaluate_expression(tokens[i])
            result = self.apply_operator(first_value, operator, second_value)
            i += 1
        else:
            result = first_value
        self.variables[var_name] = result
        return i
    
    def handle_if_statement(self, tokens, i):
        i += 1  # Skip 'lethimcook'
        condition_left = self.evaluate_expression(tokens[i])
        i += 1
        operator = tokens[i].type
        i += 1
        condition_right = self.evaluate_expression(tokens[i])
        i += 1
        
        condition_met = self.evaluate_condition(condition_left, operator, condition_right)
        
        # Find 'bet' block
        while i < len(tokens) and tokens[i].type != 'THEN':
            i += 1
        i += 1  # Skip 'bet'
        i += 1  # Skip '{'
        
        if condition_met:
            while i < len(tokens) and tokens[i].type != 'RBRACE':
                if tokens[i].type == 'PRINT':
                    i = self.handle_print(tokens, i)
                elif tokens[i].type == 'DECLARE':
                    i = self.handle_declaration(tokens, i)
                else:
                    i += 1
            i += 1
        else:
            # Skip to 'naur' block
            brace_count = 1
            while brace_count > 0:
                if tokens[i].type == 'LBRACE':
                    brace_count += 1
                elif tokens[i].type == 'RBRACE':
                    brace_count -= 1
                i += 1
            
            if i < len(tokens) and tokens[i].type == 'ELSE':
                i += 1  # Skip 'naur'
                i += 1  # Skip '{'
                while i < len(tokens) and tokens[i].type != 'RBRACE':
                    if tokens[i].type == 'PRINT':
                        i = self.handle_print(tokens, i)
                    elif tokens[i].type == 'DECLARE':
                        i = self.handle_declaration(tokens, i)
                    else:
                        i += 1
                i += 1
        return i
    
    def evaluate_condition(self, left, operator, right):
        if operator == 'GREATER':
            return left > right
        return False
    
    def apply_operator(self, left, operator, right):
        if operator == 'PLUS':
            return left + right
        elif operator == 'MINUS':
            return left - right
        elif operator == 'MULTIPLY':
            return left * right
        elif operator == 'DIVIDE':
            return left / right if right != 0 else 0
        elif operator == 'CONCAT':
            return str(left) + str(right)
        return left
    
    def evaluate_expression(self, token):
        if token.type == 'NUMBER':
            return token.value
        elif token.type == 'STRING':
            return token.value
        elif token.type == 'IDENTIFIER':
            return self.variables.get(token.value, 0)
        return 0

def main():
    interpreter = Interpreter()
    
    # List of test files
    test_files = ['math.txt', 'concat.txt', 'conditional.txt']
    
    for test_file in test_files:
        try:
            with open(test_file, 'r') as file:
                program = file.read()
            
            # Print a header for each test
            print(f"\n=== Running Goofy Program from {test_file} ===\n")
            
            # Run the interpreter and print output
            interpreter.interpret(program)
            
            # Print completion message for the test
            print(f"\n=== Program from {test_file} Complete ===\n")
        
        except FileNotFoundError:
            print(f"Error: {test_file} not found. Please create this file first!")
        except Exception as e:
            print(f"Error running program from {test_file}: {str(e)}")
        
        # Add a larger space and separator between test outputs
        print("\n" + "="*40 + "\n")  # Clear separation between tests

if __name__ == "__main__":
    main()

