from operator import add, sub, mul, truediv


class TokenType:
    INTEGER = "INTEGER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    EOF = "EOF"


class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value


class Lexer:
    TOKENS = {
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.MUL,
        "/": TokenType.DIV,
        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
    }

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[0] if text else None

    def advance(self):
        self.pos += 1
        self.current_char = (
            self.text[self.pos]
            if self.pos < len(self.text)
            else None
        )

    def integer(self):
        result = ""

        while (
            self.current_char
            and self.current_char.isdigit()
        ):
            result += self.current_char
            self.advance()

        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
                continue

            if self.current_char.isdigit():
                return Token(
                    TokenType.INTEGER,
                    self.integer(),
                )

            if self.current_char in self.TOKENS:
                char = self.current_char
                self.advance()

                return Token(
                    self.TOKENS[char],
                    char,
                )

            raise ValueError(
                f"Невідомий символ: {self.current_char}"
            )

        return Token(TokenType.EOF, None)


class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Num:
    def __init__(self, token):
        self.value = token.value


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type != token_type:
            raise ValueError(
                "Помилка синтаксичного аналізу"
            )

        self.current_token = (
            self.lexer.get_next_token()
        )

    def factor(self):
        token = self.current_token

        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)

        if token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

        raise ValueError(
            "Очікується число або вираз у дужках"
        )

    def term(self):
        node = self.factor()

        while self.current_token.type in (
            TokenType.MUL,
            TokenType.DIV,
        ):
            token = self.current_token
            self.eat(token.type)

            node = BinOp(
                node,
                token,
                self.factor(),
            )

        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            token = self.current_token
            self.eat(token.type)

            node = BinOp(
                node,
                token,
                self.term(),
            )

        return node


class Interpreter:
    OPERATIONS = {
        TokenType.PLUS: add,
        TokenType.MINUS: sub,
        TokenType.MUL: mul,
        TokenType.DIV: truediv,
    }

    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        return self.OPERATIONS[node.op.type](
            left,
            right,
        )

    def visit(self, node):
        if isinstance(node, Num):
            return node.value

        return self.visit_BinOp(node)

    def interpret(self):
        result = self.visit(self.parser.expr())

        if (
            self.parser.current_token.type
            != TokenType.EOF
        ):
            raise ValueError(
                "Зайві символи у виразі"
            )

        return result


def main():
    while True:
        try:
            text = input(
                'Введіть вираз або для виходу введіть "exit": '
            )

            if text.lower() == "exit":
                break

            result = Interpreter(
                Parser(Lexer(text))
            ).interpret()

            print(f"Результат: {result}")

        except (
            ValueError,
            ZeroDivisionError,
        ) as error:
            print(f"Помилка: {error}")


if __name__ == "__main__":
    main()