from lexical import LexicalAnalyzer
import sys

class Parser:
    def __init__(self, file):
        self.token_list = LexicalAnalyzer.lexer(file)
        self.line_numb = 1
        self.i = 0

        for key, value in self.token_list[self.i][0].items():
            self.INPUT_TOKEN = value
            break

    def match(self, EXPECTED_TOKEN):
        try:
            if self.token_list[self.i][2] > self.token_list[self.i+1][1]:
                self.line_numb += 1
        except:
            pass

        if EXPECTED_TOKEN == self.INPUT_TOKEN:
            self.i += 1

            if (self.i < len(self.token_list)):
                for key, value in self.token_list[self.i][0].items():
                    if (value in LexicalAnalyzer.punctuation.values() or 
                        value in LexicalAnalyzer.operators.values() or 
                        value in LexicalAnalyzer.reserved_words.values()):
                        
                        self.INPUT_TOKEN = value
                    
                    else:
                        self.INPUT_TOKEN = key
                    
                    break

        else:
            print(f"Sintax error line {self.line_numb+1} column: {self.token_list[self.i][1]}: {list(self.token_list[self.i][0].values())[0]}")
            exit(-1)

    def prog(self,EXPECTED_TOKEN):
        self.fun(EXPECTED_TOKEN)
        self.fun_seq(EXPECTED_TOKEN)
    
    def fun_seq(self,EXPECTED_TOKEN):

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
        
        if("Identifier" in self.INPUT_TOKEN):
            self.match("Identifier")
            self.match("COLON")
            self.type(EXPECTED_TOKEN)
            self.params_list_aux(EXPECTED_TOKEN)
        else:
            return
    
    def params_list_aux(self, EXPECTED_TOKEN):
        
        if("COMMA" in self.INPUT_TOKEN):
            self.match("COMMA")
            self.match("Identifier")
            self.match("COLON")
            self.type(EXPECTED_TOKEN)
            self.params_list_aux(EXPECTED_TOKEN)
        else:
            return
    def return_type(self, EXPECTED_TOKEN):
            
        if (self.INPUT_TOKEN == "ARROW"):
            self.match("ARROW")
            if (self.INPUT_TOKEN in ["INT", "FLOAT", "CHAR"]):
                self.type(EXPECTED_TOKEN)
        else:
            return
    
    def block(self, EXPECTED_TOKEN):
        self.match("L_BRACE")
        self.seq(EXPECTED_TOKEN)
        self.match("R_BRACE")
    
    def seq(self, EXPECTED_TOKEN):
        if("LET" in self.INPUT_TOKEN):
            self.declaration(EXPECTED_TOKEN)
            self.seq(EXPECTED_TOKEN)
        else:
            if ("Identifier" in self.INPUT_TOKEN or
                "if" in self.INPUT_TOKEN or
                "WHILE" in self.INPUT_TOKEN or
                "PRINT" in self.INPUT_TOKEN or
                "RETURN" in self.INPUT_TOKEN):

                self.commands(EXPECTED_TOKEN)
                self.seq(EXPECTED_TOKEN)
        return
    
# Usage:
parser = Parser(sys.argv[1])
parser.prog("FUNCTION")
