##########################################
# Nome: Perdo Garcia, Sávio Francisco    #
# Analisardor Sintático                  #
##########################################

from lexical import LexicalAnalyzer
import sys

class ASTNode:
    def __init__(self, node_type, children=None, value=None):
        self.node_type = node_type
        self.children = children if children else []
        self.value = value

    def add_child(self, child):
        self.children.append(child)

    def __str__(self, level=0):
        indent = "  " * level
        # Constrói a string de representação do nó atual
        result = f"{indent}Node(type={self.node_type}, value={self.value})\n"
        # Recursivamente chama __str__ para cada filho, aumentando o nível de indentação
        for child in self.children:
            result += child.__str__(level + 1)
        return result    
    


class SymbolTable:
    
    def __init__(self, func_name):
        self.symbols = {}
        self.func_name = func_name

    def add_symbol(self, id:str, tipo:str, pos_par:int):
        if id in self.symbols:
            raise Exception(f"Erro: Identificador {id} já declarado.")
        
        self.symbols[id] = (tipo, pos_par)
    
    def __str__(self) -> str:
        final_string = f"Tabela da função : {self.func_name} \n"
        for key in self.symbols.keys(): 
            final_string += key + ' | ' + str(self.symbols[key]) + '\n'
        
        return final_string


token_list = LexicalAnalyzer.lexer(sys.argv[1])

line_numb = 1

tabela_de_simbolos = {} #Dicionário das tableas de símbolos

pos_param = 0
fn_atual = ""
lista_ids = []

i = 0

global INPUT_TOKEN
global INPUT_VALUE

for key, value in token_list[i][0].items():
    INPUT_TOKEN = value
    
    break

def match(EXPECTED_TOKEN):
    
    global i, token_list, INPUT_TOKEN, line_numb, INPUT_VALUE

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
                    INPUT_VALUE = value
                
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
    
    global INPUT_VALUE, fn_atual
    
    match("FUNCTION")

    #Criara uma nova entrada na trabla de simbolos global
    tabela_de_simbolos[INPUT_VALUE] = SymbolTable(INPUT_VALUE)
    fn_atual = INPUT_VALUE

    #cria o no Function
    func_node = ASTNode("FUNC")

    match("Identifier")
    match("L_BRACKET")
    params_list(EXPECTED_TOKEN)
    match("R_BRACKET")
    return_type(EXPECTED_TOKEN)
    block(EXPECTED_TOKEN, func_node)
    print(func_node)

def params_list(EXPECTED_TOKEN):
    
    global INPUT_TOKEN, INPUT_VALUE, fn_atual, pos_param
    ##Guardar o lexema do Id
    if ("Identifier" in INPUT_TOKEN):
        id = INPUT_VALUE
        match("Identifier")

        match("COLON") 
        tipo = type(EXPECTED_TOKEN)
        tabela_de_simbolos[fn_atual].add_symbol(id,tipo,pos_param)
        pos_param+=1

        ##Variável locar para receber 
        params_list_aux(EXPECTED_TOKEN)
    
    else:
        return

def params_list_aux(EXPECTED_TOKEN):
    
    global INPUT_TOKEN, INPUT_VALUE, fn_atual, pos_param

    if ("COMMA" in INPUT_TOKEN):
        
        match("COMMA")
        id = INPUT_VALUE
        
        match("Identifier")
        match("COLON")
        tipo = type(EXPECTED_TOKEN)
        
        tabela_de_simbolos[fn_atual].add_symbol(id, tipo, pos_param)
        pos_param+=1
        
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

def block(EXPECTED_TOKEN, func_node : ASTNode):
    match("L_BRACE")
    block_node = ASTNode("BLOCK")   #Cria o Node Bloco
    seq(EXPECTED_TOKEN, block_node) #Passa o Node bloco pra seq
    func_node.add_child(block_node) #Coloca como filho de function
    match("R_BRACE")

def seq(EXPECTED_TOKEN, block_node : ASTNode):
    
    global INPUT_TOKEN

    if ("LET" in INPUT_TOKEN):
        declaration(EXPECTED_TOKEN, block_node)
        seq(EXPECTED_TOKEN, block_node) #passa nó bloco
    
    else:
        if ("Identifier" in INPUT_TOKEN or 
            "if" in INPUT_TOKEN or
            "WHILE" in INPUT_TOKEN or
            "PRINT" in INPUT_TOKEN or
            "PRINT_LINE" in INPUT_TOKEN or
            "RETURN" in INPUT_TOKEN):
            
            comands(EXPECTED_TOKEN, block_node) #passa nó bloco e retorna
            seq(EXPECTED_TOKEN, block_node) #passa nó bloco e retorna
    return

def declaration(EXPECTED_TOKEN):
    global lista_ids, tabela_de_simbolos
    match("LET")
    var_1(EXPECTED_TOKEN)
    match("COLON")
    tipo = type(EXPECTED_TOKEN)
    match("P_COMMA")
    for id in lista_ids:
        tabela_de_simbolos[fn_atual].add_symbol(id,tipo,-1)

    lista_ids = []

def var_1(EXPECTED_TOKEN):
    global INPUT_TOKEN, INPUT_VALUE

    lista_ids.append(INPUT_VALUE)

    match("Identifier")
    var_2(EXPECTED_TOKEN)

def var_2(EXPECTED_TOKEN):
    
    global INPUT_TOKEN, INPUT_VALUE
    
    if ("COMMA" in INPUT_TOKEN):
        match("COMMA")
        lista_ids.append(INPUT_VALUE)
        match("Identifier")
        var_2(EXPECTED_TOKEN)
    
    return

#Feito
def type(EXPECTED_TOKEN):

    global INPUT_TOKEN

    if ("INT" in INPUT_TOKEN):
        match("INT")
        return "INT"
    
    elif ("FLOAT" in INPUT_TOKEN):
        match("FLOAT")
        return "FLOAT"
    
    elif ("CHAR" in INPUT_TOKEN):
        match("CHAR")
        return "CHAR"

def comands(EXPECTED_TOKEN, block_node : ASTNode):

    global INPUT_TOKEN, INPUT_VALUE

    if ("Identifier" in INPUT_TOKEN):
        id = ASTNode("ID", value=INPUT_VALUE)
        match("Identifier")
        attr_or_call(EXPECTED_TOKEN, block_node)
    
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

def attr_or_call(EXPECTED_TOKEN, block_node : ASTNode):

    global INPUT_TOKEN
    
    if ("ATTR" in INPUT_TOKEN):
        attr_node = ASTNode("Assingn")
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

for key in tabela_de_simbolos.keys() :

    print(tabela_de_simbolos[key])

##Implementar a tebela
#1)Como ele é estruturada, p/ cada função tem-se uma tabela


##Asa
##Semântico