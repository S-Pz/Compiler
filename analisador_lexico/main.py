import re
import sys 
import json

#=================================================== TOKENS ========================================================
class LexicalAnalyzer:
    reserved_words = {
        'fn'        : 'FUNCTION',
        'main'      : 'MAIN',
        'let'       : 'LET',
        'int'       : 'INT',
        'float'     : 'FLOAT',
        'char'      : 'CHAR',
        'if'        : 'if',
        'else'      : 'ELSE',
        'while'     : 'WHILE',
        'print'     : 'PRINT',
        'println'   : 'PRINT_LINE',
        'return'    : 'RETURN',
    }
    
    operators = {
        '=='        : 'COMPARISON',
        '!='        : 'DIFFERENCE',
        '<='        : 'LESS_EQUAL_T',
        '<'         : 'LESS_T',
        '>='        : 'GREATER_EQUAL_T',
        '>'         : 'GREATER_T',
        '+'         : 'PLUS',
        '->'        : 'ARROW',
        '-'         : 'MINUS',
        '*'         : 'MULT',
        '/'         : 'DIV',
        '='         : 'ATTR',
    }

    punctuation =  {
       
        ':'         : 'COLON',
        '('         : 'L_BRACKET',
        ')'         : 'R_BRACKET',
        '{'         : 'L_BRACE',
        '}'         : 'R_BRACE',
        '['         : 'L_COL',
        ']'         : 'R_COL',
        ','         : 'COMMA',
        ';'         : 'P_COMMA',
    }
    
    id_pattern = re.compile(r'[a-zA-Z]([a-zA-Z]|[0-9]|_)*')
    char_literal_pattern = re.compile(r"'.*?'")
    formated_string_pattern = re.compile(r'"([^"\\]|\\.)*"')
    integer_const_pattern = re.compile(r'[0-9]+')
    float_const_pattern = re.compile(r'[0-9]+\.[0-9]+')
    
    
#=========================================== ANALISADOR LEXICO =============================================================
    @staticmethod
    def lexer(filename):
        line_number = 0 # Numero da linha
        tokens = [] # Lista de Tokens
        
        with open(filename, 'r') as f :
            for line in f :
                line_number += 1 
                position = 0 # Posição atual dentro da linha 
                while position < len(line):
                    match = None
                    for pattern, token_type in [

                        (LexicalAnalyzer.id_pattern, 'ID'),
                        (LexicalAnalyzer.char_literal_pattern, 'CHAR_LITERAL'),
                        (LexicalAnalyzer.formated_string_pattern, 'FORMATTED_STRING'),
                        (LexicalAnalyzer.float_const_pattern, 'FLOAT_CONST'),
                        (LexicalAnalyzer.integer_const_pattern, 'INTEGER_CONST'),
                    ]:
                        match = pattern.match(line, position)
                        if match:
                            
                            value = match.group()
                            
                            if token_type == 'ID' :  #Checa se um  ID é uma palavra reservada
                                
                                if value in LexicalAnalyzer.reserved_words:
                                    tokens.append(({'ReservedWords' : LexicalAnalyzer.reserved_words[value]}, line_number))
                                else : 
                                    tokens.append(({'Identifier' : value}, line_number))
                            else :
                                tokens.append(({token_type : value}, line_number))
                            
                            position = match.end()
                            
                            break
                    else:
                        for operator, token_type in LexicalAnalyzer.operators.items():
                           
                            if line.startswith(operator, position):
                                tokens.append(({'Operators': LexicalAnalyzer.operators[operator]}, line_number))
                                position += len(operator)
                                break
                        else:
                            for punctuation_mark, token_type in LexicalAnalyzer.punctuation.items():
                                if line.startswith(punctuation_mark, position):
                                    
                                    tokens.append(({'Punctuation' : LexicalAnalyzer.punctuation[punctuation_mark]} , line_number))
                                    position += len(punctuation_mark)
                                    
                                    break
                            else:
                                if line[position] == ' ' or line[position] == '\n':
                                    pass
                                else:
                    
                                    raise ValueError(f"Erro léxico na Linha: {line_number} Posição: {position}")
                                position += 1  # Ignorar caracteres desconhecido
            return tokens

#Para executar o programa rode no terminal: python main.py nomedoarquivo.p
if __name__ == "__main__":
    tokens = LexicalAnalyzer.lexer(sys.argv[1])

    #Obtém o nome do arquivo de entrada e splita
    file_name = sys.argv[1].split('.')
    
    for token in tokens:
        print(token)

    #Geração do arquivo Json
    with open(file_name[0]+".json","w", encoding="utf-8") as json_file:
        json.dump(tokens, json_file, ensure_ascii = False, indent = 2)   

