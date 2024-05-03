from lexical import LexicalAnalyzer
import sys

class SyntaxAnalyzer:
    def __init__(self, input_file):
        self.token_list = LexicalAnalyzer.lexer(input_file)
        self.line_numb = 1
        self.i = 0
        self.INPUT_TOKEN = None
    
    def get_next_token(self):
        if self.i < len(self.token_list):
            for key, value in self.token_list[self.i][0].items():
                if (value in LexicalAnalyzer.punctuation.values() or 
                    value in LexicalAnalyzer.operators.values() or 
                    value in LexicalAnalyzer.reserved_words.values()):
                    
                    self.INPUT_TOKEN = value
                
                else:
                    self.INPUT_TOKEN = key
                
                break
            self.i += 1
            
    def match(self, EXPECTED_TOKEN):
        try:
            if self.token_list[self.i][2] > self.token_list[self.i+1][1]:
                self.line_numb += 1
        except:
            pass

        if EXPECTED_TOKEN == self.INPUT_TOKEN:
            self.get_next_token()

        else:
            print(f"Sintax error line {self.line_numb+1} column: {self.token_list[self.i][1]}: {list(self.token_list[self.i][0].values())[0]}")
            exit(-1)

    def prog(self, EXPECTED_TOKEN):
        self.get_next_token()
        self.fun(EXPECTED_TOKEN)
        self.fun_seq(EXPECTED_TOKEN)

    def fun_seq(self, EXPECTED_TOKEN):
        if ("FUNCTION" in self.INPUT_TOKEN):
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

    def params_list(self, EXPECTED_TOKEN):
        self.get_next_token()
        
        if("Identifier" in self.INPUT_TOKEN):
            self.match("Identifier")
            self.match("COLON")
            self.type(EXPECTED_TOKEN)
            self.params_list_aux(EXPECTED_TOKEN)
        else:
            return
        
    

if __name__ == "__main__":
    syntax_analyzer = SyntaxAnalyzer(sys.argv[1])
    syntax_analyzer.prog("FUNCTION")