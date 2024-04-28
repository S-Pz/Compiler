
# Trabalho feito por: Leonardo Silva Vieira
#                     Marco Antonio de Abreu Barbosa
#                     Renan Aguiar Chagas

# Parte 1 -- Analisador lexico
import re
# from enum import Enum
from sys import argv

import os, sys

token_start = 0
token_flag = 0
num_linha = 1

ws = re.compile(r"[ \n\t]*")

num_linha_flag = 0

def ignore_space(string: str, inicial: int):
    foo = ws.match(string, inicial)
    if "\n" in foo[0]:
        global token_flag, num_linha_flag
        token_flag = len(foo[0]) - 1
        num_linha_flag = 1
    return len(foo[0])


tokens = {"ReservedWords": re.compile(r"fn|let|int|float|char|if|else|while|println|print|return", ),
          # retirou Main para tirar dúvida
          "Identifier": re.compile(r"[a-zA-Z][a-zA-Z0-9_]*"),
          "Punctuation": re.compile(r"\(|\)|->|:|,|\{|\}|\.|;"),
          "Operators": re.compile(r"==|=|!=|>|>=|<|<=|\+|\-|\*|\/"),
          "CharLiteral": re.compile(r"'[^']'"),
          "FloatConst": re.compile(r"[0-9]([0-9])*.[0-9]([0-9])*"),
          "IntConst": re.compile(r"[0-9]([0-9])*"),
          "FormattedString": re.compile(r"\"\{}\""),
          "Errors": re.compile(r"[^a-zA-Z0-9_]"),
          }

punctuation = {
    "(": "LParen",
    ")": "RParen",
    "->": "Arrow",
    ":": "Colon",
    ",": "Comma",
    "{": "LBrace",
    "}": "RBrace",
    ".": "Period",
    ";": "PComma"
}

operators = {
    "==": "Equal",
    "=": "Assign",
    "!=": "NotEqual",
    ">": "GreaterThan",
    ">=": "GreaterThanEqual",
    "<": "LessThan",
    "<=": "LessThanEqual",
    "+": "Plus",
    "-": "Minus",
    "*": "Multiplication",
    "/": "Division",
}

reserved = {
    "fn": "Function",
    # "main": "Main",
    "let": "Let",
    "int": "Int",
    "float": "Float",
    "char": "Char",
    "if": "If",
    "else": "Else",
    "while": "While",
    "println": "PrintLn",
    "print": "Print",
    "return": "Return",
}

token_list = []

with open(argv[1], 'r') as f:
    string_source = f.read()

while True:
    for name, token in tokens.items():
        token_flag = token_flag + ignore_space(string_source, token_start)
        token_start += ignore_space(string_source, token_start)

        if num_linha_flag == 1:
            num_linha_flag = 0
            num_linha += 1

        match = token.match(string_source, token_start)
        if not match:
            continue

        aux = match[0]
        if name == "Punctuation":
            aux = punctuation[match[0]]
        if name == "Operators":
            aux = operators[match[0]]
        if name == "ReservedWords":
            aux = reserved[match[0]]
        if name == "Errors":
            print(f"\033[1;31mErro léxico na posição {token_flag} da linha {num_linha}: {aux}.\033[m")
            exit(-1)
        token_list.append([{name: aux}, token_flag, token_flag + len(match[0])])

        token_flag = token_flag + len(match[0])
        token_start = token_start + len(match[0])
        break

    if token_start >= len(string_source) - 1:
        break

num_linha = 1

# Parte 2 -- Analisador sintatico
i = 0
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
                if value in punctuation.values() or value in operators.values() or value in reserved.values():
                    TOKEN_ENTRADA = value
                else:
                    TOKEN_ENTRADA = key
                break

    else:
        print(f"\033[1;31mErro sintático na posição {token_list[i][1]} da linha {num_linha}: {list(token_list[i][0].values())[0]}")
        exit(-1)


def Programa(TOKEN_ESPERADO):
    Funcao(TOKEN_ESPERADO)
    FuncaoSeq(TOKEN_ESPERADO)


def FuncaoSeq(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "Function" in TOKEN_ENTRADA:
        Funcao(TOKEN_ESPERADO)
        FuncaoSeq(TOKEN_ESPERADO)
    else:
        return


def Funcao(TOKEN_ESPERADO):
    combina("Function")
    combina("Identifier")
    combina("LParen")
    ListaParams(TOKEN_ESPERADO)
    combina("RParen")
    TipoRetornoFuncao(TOKEN_ESPERADO)
    Bloco(TOKEN_ESPERADO)


def ListaParams(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "Identifier" in TOKEN_ENTRADA:
        combina("Identifier")
        combina("Colon")
        Type(TOKEN_ESPERADO)
        ListaParams2(TOKEN_ESPERADO)
    else:
        return


def ListaParams2(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "Comma" in TOKEN_ENTRADA:
        combina("Comma")
        combina("Identifier")
        combina("Colon")
        Type(TOKEN_ESPERADO)
        ListaParams2(TOKEN_ESPERADO)
    else:
        return


def TipoRetornoFuncao(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if TOKEN_ENTRADA == "Arrow":
        combina("Arrow")
        if TOKEN_ENTRADA in ["Int", "Float", "Char"]:
            Type(TOKEN_ESPERADO)
    else:
        return


def Bloco(TOKEN_ESPERADO):
    combina("LBrace")
    Sequencia(TOKEN_ESPERADO)
    combina("RBrace")


def Sequencia(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "Let" in TOKEN_ENTRADA:
        Declaracao(TOKEN_ESPERADO)
        Sequencia(TOKEN_ESPERADO)
    elif "Identifier" in TOKEN_ENTRADA or "If" in TOKEN_ENTRADA or "While" in TOKEN_ENTRADA or "Print" in TOKEN_ENTRADA or "PrintLn" in TOKEN_ENTRADA or "Return" in TOKEN_ENTRADA:
        Comando(TOKEN_ESPERADO)
        Sequencia(TOKEN_ESPERADO)
    return


def Declaracao(TOKEN_ESPERADO):
    combina("Let")
    VarList(TOKEN_ESPERADO)
    combina("Colon")
    Type(TOKEN_ESPERADO)
    combina("PComma")


def VarList(TOKEN_ESPERADO):
    combina("Identifier")
    VarList2(TOKEN_ESPERADO)


def VarList2(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "Comma" in TOKEN_ENTRADA:
        combina("Comma")
        combina("Identifier")
        VarList2(TOKEN_ESPERADO)
    return


def Type(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "Int" in TOKEN_ENTRADA:
        combina("Int")
    elif "Float" in TOKEN_ENTRADA:
        combina("Float")
    elif "Char" in TOKEN_ENTRADA:
        combina("Char")


def Comando(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "Identifier" in TOKEN_ENTRADA:
        combina("Identifier")
        AtribuicaoOuChamada(TOKEN_ESPERADO)
    elif "If" in TOKEN_ENTRADA:
        ComandoIf(TOKEN_ESPERADO)
    elif "While" in TOKEN_ENTRADA:
        combina("While")
        Expr(TOKEN_ESPERADO)
        Bloco(TOKEN_ESPERADO)
    elif "Print" == TOKEN_ENTRADA:
        combina("Print")
        combina("LParen")
        combina("FormattedString")
        combina("Comma")
        ListaArgs(TOKEN_ESPERADO)
        combina("RParen")
        combina("PComma")
    elif "PrintLn" == TOKEN_ENTRADA:
        combina("PrintLn")
        combina("LParen")
        combina("FormattedString")
        combina("Comma")
        ListaArgs(TOKEN_ESPERADO)
        combina("RParen")
        combina("PComma")

    elif "Return" in TOKEN_ENTRADA:
        combina("Return")
        Expr(TOKEN_ESPERADO)
        combina("PComma")


def AtribuicaoOuChamada(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "Assign" in TOKEN_ENTRADA:
        combina("Assign")
        Expr(TOKEN_ESPERADO)
        combina("PComma")
    elif "LParen" in TOKEN_ENTRADA:
        combina("LParen")
        ListaArgs(TOKEN_ESPERADO)
        combina("RParen")


def ComandoIf(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "If" in TOKEN_ENTRADA:
        combina("If")
        Expr(TOKEN_ESPERADO)
        Bloco(TOKEN_ESPERADO)
        ComandoSenao(TOKEN_ESPERADO)
    elif "LBrace" in TOKEN_ENTRADA:
        Bloco(TOKEN_ESPERADO)


def ComandoSenao(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "Else" in TOKEN_ENTRADA:
        combina("Else")
        ComandoIf(TOKEN_ESPERADO)
    else:
        return


def Expr(TOKEN_ESPERADO):
    Rel(TOKEN_ESPERADO)
    ExprOpc(TOKEN_ESPERADO)


def ExprOpc(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "Equal" in TOKEN_ENTRADA or "NotEqual" in TOKEN_ENTRADA:
        OpIgual(TOKEN_ESPERADO)
        Rel(TOKEN_ESPERADO)
        ExprOpc(TOKEN_ESPERADO)
    else:
        return


def OpIgual(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "Equal" in TOKEN_ENTRADA:
        combina("Equal")
    elif "NotEqual" in TOKEN_ENTRADA:
        combina("NotEqual")


def Rel(TOKEN_ESPERADO):
    Adicao(TOKEN_ESPERADO)
    RelOpc(TOKEN_ESPERADO)


def RelOpc(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if TOKEN_ENTRADA in ["GreaterThan", "GreaterThanEqual", "LessThan", "LessThanEqual"]:
        OpRel(TOKEN_ESPERADO)
        Adicao(TOKEN_ESPERADO)
        RelOpc(TOKEN_ESPERADO)
    else:
        return


def OpRel(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "LessThan" in TOKEN_ENTRADA:
        combina("LessThan")
    elif "LessThanEqual" in TOKEN_ENTRADA:
        combina("LessThanEqual")
    elif "GreaterThan" in TOKEN_ENTRADA:
        combina("GreaterThan")
    elif "GreaterThanEqual" in TOKEN_ENTRADA:
        combina("GreaterThanEqual")


def Adicao(TOKEN_ESPERADO):
    Termo(TOKEN_ESPERADO)
    AdicaoOpc(TOKEN_ESPERADO)


def AdicaoOpc(TOKEN_ESPERADO):
    if "Plus" in TOKEN_ENTRADA or "Minus" in TOKEN_ENTRADA:
        OpAdicao(TOKEN_ESPERADO)
        Termo(TOKEN_ESPERADO)
        AdicaoOpc(TOKEN_ESPERADO)
    else:
        return


def OpAdicao(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "Plus" in TOKEN_ENTRADA:
        combina("Plus")
    elif "Minus" in TOKEN_ENTRADA:
        combina("Minus")


def Termo(TOKEN_ESPERADO):
    Fator(TOKEN_ESPERADO)
    TermoOpc(TOKEN_ESPERADO)


def TermoOpc(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "Multiplication" in TOKEN_ENTRADA or "Division" in TOKEN_ENTRADA:
        OpMult(TOKEN_ESPERADO)
        Fator(TOKEN_ESPERADO)
        TermoOpc(TOKEN_ESPERADO)
    else:
        return


def OpMult(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "Multiplication" in TOKEN_ENTRADA:
        combina("Multiplication")
    elif "Division" in TOKEN_ENTRADA:
        combina("Division")


def Fator(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "Identifier" in TOKEN_ENTRADA:
        combina("Identifier")
        ChamadaFuncao(TOKEN_ESPERADO)
    elif "IntConst" in TOKEN_ENTRADA:
        combina("IntConst")
    elif "FloatConst" in TOKEN_ENTRADA:
        combina("FloatConst")
    elif "CharLiteral" in TOKEN_ENTRADA:
        combina("CharLiteral")
    elif "LParen" in TOKEN_ENTRADA:
        combina("LParen")
        Expr(TOKEN_ESPERADO)
        combina("RParen")


def ChamadaFuncao(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "LParen" in TOKEN_ENTRADA:
        combina("LParen")
        ListaArgs(TOKEN_ESPERADO)
        combina("RParen")
    else:
        return


def ListaArgs(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if TOKEN_ENTRADA in ["Identifier", "IntConst", "FloatConst", "CharLiteral", "LParen"]:
        Fator(TOKEN_ESPERADO)
        ListaArgs2(TOKEN_ESPERADO)
    else:
        return


def ListaArgs2(TOKEN_ESPERADO):
    global TOKEN_ENTRADA
    if "Comma" in TOKEN_ENTRADA:
        combina("Comma")
        Fator(TOKEN_ESPERADO)
        ListaArgs2(TOKEN_ESPERADO)
    else:
        return

Programa("Function")