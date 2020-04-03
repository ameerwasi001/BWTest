from Tokens import *
from Errors import *

#Position
class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1
        if current_char == '\n':
            self.ln += 1
            self.col = 0
        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#Lexer
class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, self.fn, self.text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_number(self):
        number_str = ""
        pos_start = self.pos.copy()
        dot_count = 0
        while (self.current_char != None) and (self.current_char in DIGITS+"."):
            if self.current_char == ".": dot_count+=1
            if dot_count == 2: break
            number_str += self.current_char
            self.advance()
        return Token(TT_NUMBER, number_str, pos_start, self.pos)

    def make_identifier(self):
        id_str = ""
        pos_start = self.pos.copy()
        while (self.current_char != None) and (self.current_char in LETTERS+"_"+DIGITS):
            id_str += self.current_char
            self.advance()
        return Token(TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER, id_str, pos_start, self.pos)

    def equals_or_ee_or_darrow(self):
        pos_start = self.pos.copy()
        tok_type = TT_EQUALS
        self.advance()
        if self.current_char == "=":
            tok_type = TT_EE
            self.advance()
        elif self.current_char == ">":
            tok_type = TT_DARROW
            self.advance()
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos.copy())

    def greater_or_ge(self):
        pos_start = self.pos.copy()
        tok_type = TT_GT
        self.advance()
        if self.current_char == "=":
            tok_type = TT_GTE
            self.advance()
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos.copy())

    def lesser_or_le(self):
        pos_start = self.pos.copy()
        tok_type = TT_LT
        self.advance()
        if self.current_char == "=":
            tok_type = TT_LTE
            self.advance()
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos.copy())

    def not_or_ne(self):
        pos_start = self.pos.copy()
        tok_type = TT_NOT
        self.advance()
        if self.current_char == "=":
            tok_type = TT_NE
            self.advance()
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos.copy())

    def make_string(self):
        string = ""
        escape_character = False
        escape_characters = {
            't': '\t',
            'n': '\n'
        }
        pos_start = self.pos.copy()
        self.advance()
        while self.current_char != '"' or escape_character:
            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)
                escape_character = False
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string += self.current_char
            self.advance()
        self.advance()
        return Token(TT_STRING, string, pos_start=pos_start, pos_end=self.pos.copy())

    def single_arrow_or_minus(self):
        tok_type = TT_MINUS
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '>':
            tok_type = TT_SARROW
            self.advance()
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos.copy())

    def skip_comment(self):
        self.advance()
        while not self.current_char == '\n':
            self.advance()
        self.advance()
        return

    def generate_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in '\t ':
                self.advance()
            elif self.current_char in '$':
                self.skip_comment()
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(self.single_arrow_or_minus())
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == '=':
                tokens.append(self.equals_or_ee_or_darrow())
            elif self.current_char == '>':
                tokens.append(self.greater_or_ge())
            elif self.current_char == '<':
                tokens.append(self.lesser_or_le())
            elif self.current_char == '!':
                tokens.append(self.not_or_ne())
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA, pos_start=self.pos))
                self.advance()
            elif self.current_char == '|':
                tokens.append(Token(TT_OR, pos_start=self.pos))
                self.advance()
            elif self.current_char == '&':
                tokens.append(Token(TT_AND, pos_start=self.pos))
                self.advance()
            elif self.current_char in ';\n':
                tokens.append(Token(TT_NEWLINE, pos_start=self.pos))
                self.advance()
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharacterError(pos_start, self.pos, f"'{char}'")
        tokens.append(Token(TT_EOF, pos_start = self.pos))
        return tokens, None
