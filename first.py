__author__ = "Harsh"

import re


def read_grammar(file_name):

    fp = open(file_name, 'r')

    grammar_productions_list = []

    for eachLine in fp:
        grammar_productions_list.append(eachLine.strip())

    return grammar_productions_list


def read_grammar_asDict(filename):
    grammar_list = read_grammar(filename)
    grammar = {}
    for eachElement in grammar_list:
        eachElement = eachElement.replace(" ", "")
        production = eachElement.split("->")
        if production[0] in grammar:
            grammar[production[0]].append(production[1])
        else:
            grammar[production[0]] = [production[1]]

    return grammar


def find_first(grammar):
  
    first = {}

    non_terminals_list = grammar.keys()


    for non_terminal in non_terminals_list:
   
        first_list = get_first_list(non_terminal, grammar, first)
        first[non_terminal] = first_list

    for symbol in first:
        first_list = list(set(first[symbol]))
        first[symbol] = first_list

    checkForeps(grammar, first)

    return first



def get_first_list(non_terminal, grammar, first):


    first_list = []

    for production in grammar[non_terminal]:
        m = re.search("[A-Z]+",
                      production)  
  
        if m:
            if m.start() > 0:

                first_list.append(
                    production[0])  
            elif m.start() == 0:
           
                temp = first_of_next_symbol(production, first,
                                            grammar)  

                if temp:
        

                    first_list = first_list + temp  


        else:
            if production != "e":
                first_list.append(production[0])  
    if "e" in grammar[non_terminal]:
        if "e" not in first_list:
            first_list.append("e")

    return first_list


def first_of_next_symbol(production, first, grammar):
   
    first_list = []

    for symbol in production:
        if symbol in first:
            first_list = first_list + first[symbol]

        else:
            if symbol.isupper():
                first_list = first_list + get_first_list(symbol, grammar, first)
            else:
                return first_list

        if len(production) > 1:

            if "e" in grammar[symbol]:

                for i in range(first_list.count("e")):
                    first_list.remove("e")

                if production.index(symbol) + 1 < len(production) and production[production.index(symbol) + 1:][
                    0].isupper():
                    temp = get_first_list(production[production.index(symbol) + 1:][0], grammar, first)

                    first_list = first_list + temp

                    if "e" in temp:
                        continue
                    else:
                        return first_list
                elif production.index(symbol) + 1 < len(production) and production[production.index(symbol) + 1:][
                    0].islower():
                    first_list.append(production[production.index(symbol) + 1:][0])
                    return first_list
            else:
                return first_list
    return first_list


def checkForeps(grammar, first):
    for non_terminal in grammar.keys():
        for eachProduction in grammar[non_terminal]:
            m = re.match("[A-Z]+", eachProduction)
            if m:
                if m.end() == len(eachProduction):
                    eps_present = True
                    for symbol in eachProduction:
                        if 'e' not in first[symbol]:
                            eps_present = False
                            break
                    if eps_present:
                        if 'e' not in first[non_terminal]:
                            first[non_terminal].append('e')
                    else:
                        if 'e' in first[non_terminal]:
                            first[non_terminal].remove('e')


if __name__ == '__main__':
    file_name = "grammar.txt"
    grammar = read_grammar_asDict(file_name)

    first = find_first(grammar)
    print(first)
