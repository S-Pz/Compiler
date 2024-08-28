##########################################
# Nome: Perdo Garcia, Sávio Francisco    #
# Analisador Sintático                  #
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
    block_node = block(EXPECTED_TOKEN, func_node)
    func_node.add_child(block_node)
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

def block(EXPECTED_TOKEN):
    match("L_BRACE")
    block_node = ASTNode("BLOCK")   #Cria o Node Bloco
    seq(EXPECTED_TOKEN, block_node) #Passa o Node bloco pra seq
    match("R_BRACE")
    return block_node

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
            
            no = comands(EXPECTED_TOKEN)
            block_node.add_child(no)
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

def comands(EXPECTED_TOKEN):

    global INPUT_TOKEN, INPUT_VALUE

    if ("Identifier" in INPUT_TOKEN):
        id_node = ASTNode("ID", value=INPUT_VALUE)
        match("Identifier")
        return attr_or_call(EXPECTED_TOKEN, id_node)
    
    elif ("if" in INPUT_TOKEN):
        if_command(EXPECTED_TOKEN)
    
    elif ("WHILE" in INPUT_TOKEN):
        match("WHILE")
        no_expr = expression(EXPECTED_TOKEN)
        no_bloco = block(EXPECTED_TOKEN)
        return ASTNode('While', children=[no_expr, no_bloco])
    
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

def attr_or_call(EXPECTED_TOKEN, id_node : ASTNode):

    global INPUT_TOKEN
    
    if ("ATTR" in INPUT_TOKEN):
        attr_node = ASTNode("Assingn")
        match("ATTR")
        expression(EXPECTED_TOKEN)
        match("P_COMMA")
        return attr_node

    elif ("L_BRACKET" in INPUT_TOKEN):
        match("L_BRACKET")
        args_list(EXPECTED_TOKEN)
        match("R_BRACKET")
        return None
        #TODO
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
    
    no_esq = relational_expression(EXPECTED_TOKEN)
    return expression_opc(EXPECTED_TOKEN, no_esq)

def expression_opc(EXPECTED_TOKEN, no_esq):
    
    global INPUT_TOKEN, INPUT_VALUE

    if("COMPARISON" in INPUT_TOKEN or "DIFFERENCE" in INPUT_TOKEN):
        
        op = INPUT_VALUE
        iqual_operation(EXPECTED_TOKEN)
        
        no_dir = relational_expression(EXPECTED_TOKEN)
        no = ASTNode("RelOp", value=op)
        no.add_child(no_esq)
        no.add_child(no_dir)
        
        return expression_opc(EXPECTED_TOKEN, no)
    
    else:
        return no_esq

def relational_expression(EXPECTED_TOKEN): #expressões relacionais
    no_esq = sum(EXPECTED_TOKEN)
    return relational_expression_oper(EXPECTED_TOKEN, no_esq)

def relational_expression_oper(EXPECTED_TOKEN, no_esq : ASTNode): #lida com operadores de comparação em expressões relacionais
    
    global INPUT_TOKEN, INPUT_VALUE
    
    if (INPUT_TOKEN in ["GREATER_T", "GREATER_EQUAL_T", "LESS_T", "LESS_EQUAL_T"]):
        op = INPUT_VALUE
        relational_operation(EXPECTED_TOKEN)        
        no_dir : ASTNode = sum(EXPECTED_TOKEN)
        no = ASTNode("RelOp", value=op)
        no.add_child(no_esq)
        no.add_child(no_dir)
        return  relational_expression_oper(EXPECTED_TOKEN,no)
    else:
        return no_esq

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
    no_esq = term(EXPECTED_TOKEN)
    return sum_opc(EXPECTED_TOKEN, no_esq)

def sum_opc(EXPECTED_TOKEN, no_esq : ASTNode):#Operadores de adição em expressões aritméticas
    global INPUT_TOKEN, INPUT_VALUE

    if ("PLUS" in INPUT_TOKEN or
        "MINUS" in INPUT_TOKEN):
        op = INPUT_VALUE
        sum_operation(EXPECTED_TOKEN)
        no_dir = term(EXPECTED_TOKEN)

        no = ASTNode("Aritop", value=op)
        no.add_child(no_esq)
        no.add_child(no_dir)
        return sum_opc(EXPECTED_TOKEN, no)
    
    else:
        return no_esq

def sum_operation(EXPECTED_TOKEN):#Verifica qual operador de adição está presente no token atual 

    global INPUT_TOKEN
    
    if ("PLUS" in INPUT_TOKEN):
        match("PLUS")
    elif ("MINUS" in INPUT_TOKEN):
        match("MINUS")

def term(EXPECTED_TOKEN):
    no_esq = factor(EXPECTED_TOKEN)
    return termo_opc(EXPECTED_TOKEN, no_esq)

def termo_opc(EXPECTED_TOKEN, no_esq : ASTNode):
    
    global INPUT_TOKEN, INPUT_VALUE
    
    if ("MULT" in INPUT_TOKEN or "DIV" in INPUT_TOKEN):
        op = INPUT_VALUE
        mul_operation(EXPECTED_TOKEN)
        no_dir = factor(EXPECTED_TOKEN )
        no_arith = ASTNode("Arith_NODE", value=op)
        no_arith.add_child(no_esq)
        no_arith.add_child(no_dir)
        return termo_opc(EXPECTED_TOKEN, no_arith)
    else:
        return no_esq

def mul_operation(EXPECTED_TOKEN):
    global INPUT_TOKEN
    
    if ("MULT" in INPUT_TOKEN):
        match("MULT")
    
    elif ("DIV" in INPUT_TOKEN):
        match("DIV")

def factor(EXPECTED_TOKEN):
    
    global INPUT_TOKEN, INPUT_VALUE
    
    if ("Identifier" in INPUT_TOKEN):
        node = ASTNode("ID_NODE", value=INPUT_VALUE)
        match("Identifier")
        node_call : ASTNode = call_function(EXPECTED_TOKEN)
        
        if node_call is None:
            return node
        else :
            return node_call

    elif ("INTEGER_CONST" in INPUT_TOKEN):
        no = ASTNode("INT_CONST", value=INPUT_VALUE)
        match("INTEGER_CONST")
        return no
    
    elif ("FLOAT_CONST" in INPUT_TOKEN):
        no = ASTNode("FLOAT_CONST", value=INPUT_VALUE)
        match("FLOAT_CONST")
        return no
    
    elif ("CHAR_LITERAL" in INPUT_TOKEN):
        no = ASTNode("CHAR_LITERAL", value=INPUT_VALUE)
        match("CHAR_LITERAL")
        return no
    
    elif ("L_BRACKET" in INPUT_TOKEN):
        match("L_BRACKET")
        no = expression(EXPECTED_TOKEN)
        match("R_BRACKET")
        return no
    
def call_function(EXPECTED_TOKEN):
    
    global INPUT_TOKEN
    
    if ("L_BRACKET" in INPUT_TOKEN):
        call_node = ASTNode("CALL_NODE")
        match("L_BRACKET")
        args_list(EXPECTED_TOKEN, call_node)
        match("R_BRACKET")
        return call_node
    else:
        return None

def args_list(EXPECTED_TOKEN, call_node : ASTNode):
    
    global INPUT_TOKEN

    if (INPUT_TOKEN in ["Identifier", "INTEGER_CONST", "FLOAT_CONST", "CHAR_LITERAL", "L_BRACKET"]):
        factor_node : ASTNode = factor(EXPECTED_TOKEN)
        call_node.add_child(factor_node)
        args_list_2(EXPECTED_TOKEN, call_node)
    else:
        return

def args_list_2(EXPECTED_TOKEN, call_node : ASTNode):
    
    global INPUT_TOKEN
    
    if ("COMMA" in INPUT_TOKEN):
        match("COMMA")
        factor_node : ASTNode = factor(EXPECTED_TOKEN)
        call_node.add_child(factor_node)
        args_list_2(EXPECTED_TOKEN, call_node)
    else:
        return
    
prog("FUNCTION")

for key in tabela_de_simbolos.keys() :

    print(tabela_de_simbolos[key])

##Implementar a tebela
#1)Como ele é estruturada, p/ cada função tem-se uma tabela


##Asa
##Semântico