##########################################
# Nome: Perdo Garcia, Sávio Francisco    #
# Analisardor Sintático                  #
#                                        #
##########################################

from lexical import LexicalAnalyzer
import sys

token_list = LexicalAnalyzer.lexer(sys.argv[1])

line_numb = 1

i = 0

global INPUT_TOKEN

for key, value in token_list[i][0].items():
    INPUT_TOKEN = value
    break

def match(EXPECTED_TOKEN):
    
    global i, token_list, INPUT_TOKEN, line_numb

    try:
        if token_list[i][2] > token_list[i+1][1]:
            line_numb += 1
    except:
        pass

    if EXPECTED_TOKEN == INPUT_TOKEN:
        i += 1
        if (i < len(token_list)):
            for key, value in token_list[i][0].items():
                if (value in LexicalAnalyzer.punctuation.values() or 
                    value in LexicalAnalyzer.operators.values() or 
                    value in LexicalAnalyzer.reserved_words.values()):
                    
                    INPUT_TOKEN = value
                
                else:
                    INPUT_TOKEN = key
                
                break

    else:
        print(f"Sintax error line {line_numb+1} column: {token_list[i][1]}: {list(token_list[i][0].values())[0]}")
        exit(-1)

def prog(EXPECTED_TOKEN):
    fun(EXPECTED_TOKEN)
    fun_seq(EXPECTED_TOKEN)

def fun_seq(EXPECTED_TOKEN):
    
    global INPUT_TOKEN
    
    if ("FUNCTION" in INPUT_TOKEN):
        fun(EXPECTED_TOKEN)
        fun_seq(EXPECTED_TOKEN)
    else:
        return
      
def fun(EXPECTED_TOKEN):
    match("FUNCTION")
    match("Identifier")
    match("L_BRACKET")
    params_list(EXPECTED_TOKEN)
    match("R_BRACKET")
    return_type(EXPECTED_TOKEN)
    block(EXPECTED_TOKEN)

def params_list(EXPECTED_TOKEN):
    
    global INPUT_TOKEN

    if ("Identifier" in INPUT_TOKEN):
        match("Identifier")
        match("COLON")
        type(EXPECTED_TOKEN)
        params_list_aux(EXPECTED_TOKEN)
    
    else:
        return

def params_list_aux(EXPECTED_TOKEN):
    
    global INPUT_TOKEN

    if ("COMMA" in INPUT_TOKEN):
        match("COMMA")
        match("Identifier")
        match("COLON")
        type(EXPECTED_TOKEN)
        params_list_aux(EXPECTED_TOKEN)
    
    else:
        return

def return_type(EXPECTED_TOKEN):

    global INPUT_TOKEN

    if (INPUT_TOKEN == "ARROW"):
        match("ARROW")
        if (INPUT_TOKEN in ["INT", "FLOAT", "CHAR"]):
            type(EXPECTED_TOKEN)
    else:
        return

def block(EXPECTED_TOKEN):
    match("L_BRACE")
    seq(EXPECTED_TOKEN)
    match("R_BRACE")

def seq(EXPECTED_TOKEN):
    
    global INPUT_TOKEN

    if ("LET" in INPUT_TOKEN):
        declaration(EXPECTED_TOKEN)
        seq(EXPECTED_TOKEN)
    
    else:
        if ("Identifier" in INPUT_TOKEN or 
            "if" in INPUT_TOKEN or
            "WHILE" in INPUT_TOKEN or
            "PRINT" in INPUT_TOKEN or
            "PRINT_LINE" in INPUT_TOKEN or
            "RETURN" in INPUT_TOKEN):
            
            comands(EXPECTED_TOKEN)
            seq(EXPECTED_TOKEN)
    return

def declaration(EXPECTED_TOKEN):
    match("LET")
    var_1(EXPECTED_TOKEN)
    match("COLON")
    type(EXPECTED_TOKEN)
    match("P_COMMA")

def var_1(EXPECTED_TOKEN):
    match("Identifier")
    var_2(EXPECTED_TOKEN)

def var_2(EXPECTED_TOKEN):
    
    global INPUT_TOKEN
    
    if ("COMMA" in INPUT_TOKEN):
        match("COMMA")
        match("Identifier")
        var_2(EXPECTED_TOKEN)
    
    return

def type(EXPECTED_TOKEN):

    global INPUT_TOKEN
    
    if ("INT" in INPUT_TOKEN):
        match("INT")
    
    elif ("FLOAT" in INPUT_TOKEN):
        match("FLOAT")
    
    elif ("CHAR" in INPUT_TOKEN):
        match("CHAR")

def comands(EXPECTED_TOKEN):

    global INPUT_TOKEN

    if ("Identifier" in INPUT_TOKEN):
        match("Identifier")
        attr_or_call(EXPECTED_TOKEN)
    
    elif ("if" in INPUT_TOKEN):
        if_command(EXPECTED_TOKEN)
    
    elif ("WHILE" in INPUT_TOKEN):
        match("WHILE")
        expression(EXPECTED_TOKEN)
        block(EXPECTED_TOKEN)
    
    elif ("PRINT" == INPUT_TOKEN):
        match("PRINT")
        match("L_BRACKET")
        match("FORMATTED_STRING")
        match("COMMA")
        args_list(EXPECTED_TOKEN)
        match("R_BRACKET")
        match("P_COMMA")
    
    elif ("PRINT_LINE" == INPUT_TOKEN):
        match("PRINT_LINE")
        match("L_BRACKET")
        match("FORMATTED_STRING")
        match("COMMA")
        args_list(EXPECTED_TOKEN)
        match("R_BRACKET")
        match("P_COMMA")

    elif ("RETURN" in INPUT_TOKEN):
        match("RETURN")
        expression(EXPECTED_TOKEN)
        match("P_COMMA")

def attr_or_call(EXPECTED_TOKEN):

    global INPUT_TOKEN
    
    if ("ATTR" in INPUT_TOKEN):
        match("ATTR")
        expression(EXPECTED_TOKEN)
        match("P_COMMA")
    
    elif ("L_BRACKET" in INPUT_TOKEN):
        match("L_BRACKET")
        args_list(EXPECTED_TOKEN)
        match("R_BRACKET")

def if_command(EXPECTED_TOKEN):
    
    global INPUT_TOKEN

    if ("if" in INPUT_TOKEN):
        match("if")
        expression(EXPECTED_TOKEN)
        block(EXPECTED_TOKEN)
        else_command(EXPECTED_TOKEN)
    
    elif "L_BRACE" in INPUT_TOKEN:
        block(EXPECTED_TOKEN)

def else_command(EXPECTED_TOKEN):
    
    global INPUT_TOKEN

    if ("ELSE" in INPUT_TOKEN):
        match("ELSE")
        if_command(EXPECTED_TOKEN)
    else:
        return

def expression(EXPECTED_TOKEN):
    
    relational_expression(EXPECTED_TOKEN)
    expression_opc(EXPECTED_TOKEN)

def expression_opc(EXPECTED_TOKEN):
    
    global INPUT_TOKEN

    if("COMPARISON" in INPUT_TOKEN or 
        "DIFFERENCE" in INPUT_TOKEN):
        
        iqual_operation(EXPECTED_TOKEN)
        relational_expression(EXPECTED_TOKEN)
        expression_opc(EXPECTED_TOKEN)
    
    else:
        return

def relational_expression(EXPECTED_TOKEN): #expressões relacionais
    sum(EXPECTED_TOKEN)
    relational_expression_oper(EXPECTED_TOKEN)

def relational_expression_oper(EXPECTED_TOKEN): #lida com operadores de comparação em expressões relacionais
    
    global INPUT_TOKEN
    
    if (INPUT_TOKEN in ["GREATER_T", "GREATER_EQUAL_T", "LESS_T", "LESS_EQUAL_T"]):
        relational_operation(EXPECTED_TOKEN)
        sum(EXPECTED_TOKEN)
        relational_expression_oper(EXPECTED_TOKEN)
    else:
        return

def iqual_operation(EXPECTED_TOKEN):

    global INPUT_TOKEN
    
    if ("COMPARISON" in INPUT_TOKEN):
        match("COMPARISON")
    elif ("DIFFERENCE" in INPUT_TOKEN):
        match("DIFFERENCE")

def relational_operation(EXPECTED_TOKEN): #operações relacionais
    
    global INPUT_TOKEN
    
    if ("LESS_T" in INPUT_TOKEN):
        match("LESS_T")
    
    elif ("LESS_EQUAL_T" in INPUT_TOKEN):
        match("LESS_EQUAL_T")
    
    elif ("GREATER_T" in INPUT_TOKEN):
        match("GREATER_T")
    
    elif ("GREATER_EQUAL_T" in INPUT_TOKEN):
        match("GREATER_EQUAL_T")

def sum(EXPECTED_TOKEN): #Adição
    term(EXPECTED_TOKEN)
    sum_opc(EXPECTED_TOKEN)

def sum_opc(EXPECTED_TOKEN):#Operadores de adição em expressões aritméticas
    
    if ("PLUS" in INPUT_TOKEN or
        "MINUS" in INPUT_TOKEN):
        
        sum_operation(EXPECTED_TOKEN)
        term(EXPECTED_TOKEN)
        sum_opc(EXPECTED_TOKEN)
    else:
        return

def sum_operation(EXPECTED_TOKEN):#Verifica qual operador de adição está presente no token atual 

    global INPUT_TOKEN
    
    if ("PLUS" in INPUT_TOKEN):
        match("PLUS")
    elif ("MINUS" in INPUT_TOKEN):
        match("MINUS")

def term(EXPECTED_TOKEN):
    factor(EXPECTED_TOKEN)
    termo_opc(EXPECTED_TOKEN)

def termo_opc(EXPECTED_TOKEN):
    
    global INPUT_TOKEN
    
    if ("MULT" in INPUT_TOKEN or "DIV" in INPUT_TOKEN):
        mul_operation(EXPECTED_TOKEN)
        factor(EXPECTED_TOKEN)
        termo_opc(EXPECTED_TOKEN)
    else:
        return

def mul_operation(EXPECTED_TOKEN):
    global INPUT_TOKEN
    
    if ("MULT" in INPUT_TOKEN):
        match("MULT")
    
    elif ("DIV" in INPUT_TOKEN):
        match("DIV")

def factor(EXPECTED_TOKEN):
    
    global INPUT_TOKEN
    
    if ("Identifier" in INPUT_TOKEN):
        match("Identifier")
        call_function(EXPECTED_TOKEN)
    
    elif ("INTEGER_CONST" in INPUT_TOKEN):
        match("INTEGER_CONST")
    
    elif ("FLOAT_CONST" in INPUT_TOKEN):
        match("FLOAT_CONST")
    
    elif ("CHAR_LITERAL" in INPUT_TOKEN):
        match("CHAR_LITERAL")
    
    elif ("L_BRACKET" in INPUT_TOKEN):
        match("L_BRACKET")
        expression(EXPECTED_TOKEN)
        match("R_BRACKET")

def call_function(EXPECTED_TOKEN):
    
    global INPUT_TOKEN
    
    if ("L_BRACKET" in INPUT_TOKEN):
        match("L_BRACKET")
        args_list(EXPECTED_TOKEN)
        match("R_BRACKET")
    else:
        return

def args_list(EXPECTED_TOKEN):
    
    global INPUT_TOKEN

    if (INPUT_TOKEN in ["Identifier", "INTEGER_CONST", "FLOAT_CONST", "CHAR_LITERAL", "L_BRACKET"]):
        factor(EXPECTED_TOKEN)
        args_list_2(EXPECTED_TOKEN)
    else:
        return

def args_list_2(EXPECTED_TOKEN):
    
    global INPUT_TOKEN
    
    if ("COMMA" in INPUT_TOKEN):
        match("COMMA")
        factor(EXPECTED_TOKEN)
        args_list_2(EXPECTED_TOKEN)
    else:
        return
    
prog("FUNCTION")