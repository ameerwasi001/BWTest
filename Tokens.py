from string import ascii_letters

LETTERS = ascii_letters
DIGITS = "0123456789"

#Tokems
TT_NUMBER = "NUMBER"
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_RPAREN = "RPAREN"
TT_LPAREN = "LPAREN"
TT_EE = "EE"
TT_NE = "NE"
TT_GT = "GT"
TT_LT = "LT"
TT_GTE = "GTE"
TT_LTE = "LTE"
TT_EOF = "EOF"
TT_NOT = "NOT"
TT_AND = "AND"
TT_OR = "OR"
TT_STRING = "STRING"
TT_EQUALS = "EQUALS"
TT_SARROW = "SARROW"
TT_DARROW = "DARROW"
TT_COMMA = "COMMA"
TT_NEWLINE = "NEWLINE"

KEYWORDS = [
"IF",
"THEN",
"ELSEIF",
"ELSE",
"while",
"end",
"run",
"every",
"time",
"in",
"times",
"restart",
"stop",
"try",
"except"
]

class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
        if pos_end:
            self.pos_end = pos_end

    def matches(self, name, value):
        return ((self.type == name) and (self.value == value))

    def __repr__(self):
        if self.value: return f'[{self.type}:{self.value}]'
        return self.type
