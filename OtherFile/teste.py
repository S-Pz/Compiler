from lexical import LexicalAnalyzer
import sys

class Parser:
    def __init__(self, input_file):
        self.token_list = LexicalAnalyzer.lexer(input_file)
        self.line_numb = 1
        self.i = 0
        self.INPUT_TOKEN = self.token_list[0][0].get("Identifier", "")

    def match(self, EXPECTED_TOKEN):
        try:
            if self.token_list[self.i][2] > self.token_list[self.i+1][1]:
                self.line_numb += 1
        except IndexError:
            pass

        if EXPECTED_TOKEN == self.INPUT_TOKEN:
            self.i += 1
            if self.i < len(self.token_list):
                self.INPUT_TOKEN = next(iter(self.token_list[self.i][0].values()), "")
        else:
            print(f"Sintax error line {self.line_numb+1} column: {self.token_list[self.i][1]}: {list(self.token_list[self.i][0].values())[0]}")
            exit(-1)

    def prog(self, EXPECTED_TOKEN):
        self.fun(EXPECTED_TOKEN)
        self.fun_seq(EXPECTED_TOKEN)

    def fun_seq(self, EXPECTED_TOKEN):
        if "FUNCTION" in self.INPUT_TOKEN:
            self.fun(EXPECTED_TOKEN)
            self.fun_seq(EXPECTED_TOKEN)
        else:
            return

    def fun(self, EXPECTED_TOKEN):
        self.match("FUNCTION")
        self.match("Identifier")
        self.match("L_BRACKET")
        self.params_list(EXPECTED_TOKEN)
        self.match("R_BRACKET")
        self.return_type(EXPECTED_TOKEN)
        self.block(EXPECTED_TOKEN)

    # Other methods follow...

def main():
    if len(sys.argv) != 2:
        print("Usage: python your_script.py input_file")
        sys.exit(1)
    
    parser = Parser(sys.argv[1])
    parser.