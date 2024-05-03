import re, sys, json

class LexicalAnalyzer:
    reserved_words = {
        'fn'        : 'FUNCTION',
        #'main'      : 'MAIN',
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
                                    tokens.append(({'ReservedWords' : LexicalAnalyzer.reserved_words[value]}, position , match.end()))
                                else : 
                                    tokens.append(({'Identifier' : value}, position , match.end()))
                            else :
                                tokens.append(({token_type : value}, position , match.end()))
                            
                            position = match.end()
                            
                            break
                    else:
                        for operator, token_type in LexicalAnalyzer.operators.items():
                           
                            if line.startswith(operator, position):
                                tokens.append(({'Operators': LexicalAnalyzer.operators[operator]}, position , position + len(operator)))
                                position += len(operator)
                                break
                        else:
                            for punctuation_mark, token_type in LexicalAnalyzer.punctuation.items():
                                if line.startswith(punctuation_mark, position):
                                    
                                    tokens.append(({'Punctuation' : LexicalAnalyzer.punctuation[punctuation_mark]} , position, position + len(punctuation_mark)))
                                    position += len(punctuation_mark)
                                    
                                    break
                            else:
                                if line[position] == ' ' or line[position] == '\n':
                                    pass
                                else:
                    
                                    raise ValueError(f"Lexical error: line {line_number} column: {position}")
                                position += 1  # Ignorar caracteres desconhecido
            return tokens


token_list  = LexicalAnalyzer.lexer(sys.argv[1])

num_linha = 1

i = 0
print(token_list[0][2])
print(token_list[1][1])


global TOKEN_ENTRADA
for key, value in token_list[i][0].items():
    TOKEN_ENTRADA = value
    break


def combina(TOKEN_ESPERADO):
    global i, token_list, TOKEN_ENTRADA, num_linha

    try:

        if token_list[i][2] > token_list[i+1][1]:
            num_linha += 1
    except:
        pass

    if TOKEN_ESPERADO == TOKEN_ENTRADA:
        i += 1
        if i < len(token_list):
            for key, value in token_list[i][0].items():
                if value in LexicalAnalyzer.punctuation.values() or value in LexicalAnalyzer.operators.values() or value in LexicalAnalyzer.reserved_words.values():
                    TOKEN_ENTRADA = value
                else:
                    TOKEN_ENTRADA = key
                break

    else:
        print(f"\033[1;31mErro sintático na posição {token_list[i][1]} da linha {num_linha+1}: {list(token_list[i][0].values())[0]}")
        exit(-1)


def Programa(TOKEN_ESPERADO):
    Funcao(TOKEN_ESPERADO)
    FuncaoSeq(TOKEN_ESPERADO)


def FuncaoSeq(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "FUNCTION" in TOKEN_ENTRADA:
        Funcao(TOKEN_ESPERADO)
        FuncaoSeq(TOKEN_ESPERADO)
    else:
        return


def Funcao(TOKEN_ESPERADO):
    combina("FUNCTION")
    combina("Identifier")
    combina("L_BRACKET")
    ListaParams(TOKEN_ESPERADO)
    combina("R_BRACKET")
    TipoRetornoFuncao(TOKEN_ESPERADO)
    Bloco(TOKEN_ESPERADO)


def ListaParams(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "Identifier" in TOKEN_ENTRADA:
        combina("Identifier")
        combina("COLON")
        Type(TOKEN_ESPERADO)
        ListaParams2(TOKEN_ESPERADO)
    else:
        return


def ListaParams2(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "COMMA" in TOKEN_ENTRADA:
        combina("COMMA")
        combina("Identifier")
        combina("COLON")
        Type(TOKEN_ESPERADO)
        ListaParams2(TOKEN_ESPERADO)
    else:
        return


def TipoRetornoFuncao(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if TOKEN_ENTRADA == "ARROW":
        combina("ARROW")
        if TOKEN_ENTRADA in ["INT", "FLOAT", "CHAR"]:
            Type(TOKEN_ESPERADO)
    else:
        return


def Bloco(TOKEN_ESPERADO):
    combina("L_BRACE")
    Sequencia(TOKEN_ESPERADO)
    combina("R_BRACE")


def Sequencia(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "LET" in TOKEN_ENTRADA:
        Declaracao(TOKEN_ESPERADO)
        Sequencia(TOKEN_ESPERADO)
    elif "Identifier" in TOKEN_ENTRADA or "if" in TOKEN_ENTRADA or "WHILE" in TOKEN_ENTRADA or "PRINT" in TOKEN_ENTRADA or "PRINT_LINE" in TOKEN_ENTRADA or "RETURN" in TOKEN_ENTRADA:
        Comando(TOKEN_ESPERADO)
        Sequencia(TOKEN_ESPERADO)
    return


def Declaracao(TOKEN_ESPERADO):
    combina("LET")
    VarList(TOKEN_ESPERADO)
    combina("COLON")
    Type(TOKEN_ESPERADO)
    combina("P_COMMA")


def VarList(TOKEN_ESPERADO):
    combina("Identifier")
    VarList2(TOKEN_ESPERADO)


def VarList2(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "COMMA" in TOKEN_ENTRADA:
        combina("COMMA")
        combina("Identifier")
        VarList2(TOKEN_ESPERADO)
    return


def Type(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "INT" in TOKEN_ENTRADA:
        combina("INT")
    elif "FLOAT" in TOKEN_ENTRADA:
        combina("FLOAT")
    elif "CHAR" in TOKEN_ENTRADA:
        combina("CHAR")


def Comando(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "Identifier" in TOKEN_ENTRADA:
        combina("Identifier")
        AtribuicaoOuChamada(TOKEN_ESPERADO)
    elif "if" in TOKEN_ENTRADA:
        ComandoIf(TOKEN_ESPERADO)
    elif "WHILE" in TOKEN_ENTRADA:
        combina("WHILE")
        Expr(TOKEN_ESPERADO)
        Bloco(TOKEN_ESPERADO)
    elif "PRINT" == TOKEN_ENTRADA:
        combina("PRINT")
        combina("L_BRACKET")
        combina("FORMATTED_STRING")
        combina("COMMA")
        ListaArgs(TOKEN_ESPERADO)
        combina("R_BRACKET")
        combina("P_COMMA")
    elif "PRINT_LINE" == TOKEN_ENTRADA:
        combina("PRINT_LINE")
        combina("L_BRACKET")
        combina("FORMATTED_STRING")
        combina("COMMA")
        ListaArgs(TOKEN_ESPERADO)
        combina("R_BRACKET")
        combina("P_COMMA")

    elif "RETURN" in TOKEN_ENTRADA:
        combina("RETURN")
        Expr(TOKEN_ESPERADO)
        combina("P_COMMA")


def AtribuicaoOuChamada(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "ATTR" in TOKEN_ENTRADA:
        combina("ATTR")
        Expr(TOKEN_ESPERADO)
        combina("P_COMMA")
    elif "L_BRACKET" in TOKEN_ENTRADA:
        combina("L_BRACKET")
        ListaArgs(TOKEN_ESPERADO)
        combina("R_BRACKET")


def ComandoIf(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "if" in TOKEN_ENTRADA:
        combina("if")
        Expr(TOKEN_ESPERADO)
        Bloco(TOKEN_ESPERADO)
        ComandoSenao(TOKEN_ESPERADO)
    elif "L_BRACE" in TOKEN_ENTRADA:
        Bloco(TOKEN_ESPERADO)


def ComandoSenao(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "ELSE" in TOKEN_ENTRADA:
        combina("ELSE")
        ComandoIf(TOKEN_ESPERADO)
    else:
        return


def Expr(TOKEN_ESPERADO):
    Rel(TOKEN_ESPERADO)
    ExprOpc(TOKEN_ESPERADO)


def ExprOpc(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "COMPARISON" in TOKEN_ENTRADA or "DIFFERENCE" in TOKEN_ENTRADA:
        OpIgual(TOKEN_ESPERADO)
        Rel(TOKEN_ESPERADO)
        ExprOpc(TOKEN_ESPERADO)
    else:
        return


def OpIgual(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "COMPARISON" in TOKEN_ENTRADA:
        combina("COMPARISON")
    elif "DIFFERENCE" in TOKEN_ENTRADA:
        combina("DIFFERENCE")


def Rel(TOKEN_ESPERADO):
    Adicao(TOKEN_ESPERADO)
    RelOpc(TOKEN_ESPERADO)


def RelOpc(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if TOKEN_ENTRADA in ["GREATER_T", "GREATER_EQUAL_T", "LESS_T", "LESS_EQUAL_T"]:
        OpRel(TOKEN_ESPERADO)
        Adicao(TOKEN_ESPERADO)
        RelOpc(TOKEN_ESPERADO)
    else:
        return


def OpRel(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "LESS_T" in TOKEN_ENTRADA:
        combina("LESS_T")
    elif "LESS_EQUAL_T" in TOKEN_ENTRADA:
        combina("LESS_EQUAL_T")
    elif "GREATER_T" in TOKEN_ENTRADA:
        combina("GREATER_T")
    elif "GREATER_EQUAL_T" in TOKEN_ENTRADA:
        combina("GREATER_EQUAL_T")


def Adicao(TOKEN_ESPERADO):
    Termo(TOKEN_ESPERADO)
    AdicaoOpc(TOKEN_ESPERADO)


def AdicaoOpc(TOKEN_ESPERADO):
    if "PLUS" in TOKEN_ENTRADA or "MINUS" in TOKEN_ENTRADA:
        OpAdicao(TOKEN_ESPERADO)
        Termo(TOKEN_ESPERADO)
        AdicaoOpc(TOKEN_ESPERADO)
    else:
        return


def OpAdicao(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "PLUS" in TOKEN_ENTRADA:
        combina("PLUS")
    elif "MINUS" in TOKEN_ENTRADA:
        combina("MINUS")


def Termo(TOKEN_ESPERADO):
    Fator(TOKEN_ESPERADO)
    TermoOpc(TOKEN_ESPERADO)


def TermoOpc(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "MULT" in TOKEN_ENTRADA or "DIV" in TOKEN_ENTRADA:
        OpMult(TOKEN_ESPERADO)
        Fator(TOKEN_ESPERADO)
        TermoOpc(TOKEN_ESPERADO)
    else:
        return


def OpMult(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "MULT" in TOKEN_ENTRADA:
        combina("MULT")
    elif "DIV" in TOKEN_ENTRADA:
        combina("DIV")


def Fator(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "Identifier" in TOKEN_ENTRADA:
        combina("Identifier")
        ChamadaFuncao(TOKEN_ESPERADO)
    elif "INTEGER_CONST" in TOKEN_ENTRADA:
        combina("INTEGER_CONST")
    elif "FLOAT_CONST" in TOKEN_ENTRADA:
        combina("FLOAT_CONST")
    elif "CHAR_LITERAL" in TOKEN_ENTRADA:
        combina("CHAR_LITERAL")
    elif "L_BRACKET" in TOKEN_ENTRADA:
        combina("L_BRACKET")
        Expr(TOKEN_ESPERADO)
        combina("R_BRACKET")


def ChamadaFuncao(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "L_BRACKET" in TOKEN_ENTRADA:
        combina("L_BRACKET")
        ListaArgs(TOKEN_ESPERADO)
        combina("R_BRACKET")
    else:
        return


def ListaArgs(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if TOKEN_ENTRADA in ["Identifier", "INTEGER_CONST", "FLOAT_CONST", "CHAR_LITERAL", "L_BRACKET"]:
        Fator(TOKEN_ESPERADO)
        ListaArgs2(TOKEN_ESPERADO)
    else:
        return


def ListaArgs2(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "COMMA" in TOKEN_ENTRADA:
        combina("COMMA")
        Fator(TOKEN_ESPERADO)
        ListaArgs2(TOKEN_ESPERADO)
    else:
        return




Programa("FUNCTION")