__author__ = "Harsh"
from first import find_first

def read_grammar(file_name):

  fp = open(file_name,'r')

  grammar_productions_list =[]

  for eachLine in fp:
    grammar_productions_list.append(eachLine.strip())

  return grammar_productions_list

def read_grammar_asDict(filename):

  grammar_list = read_grammar(filename)   
  grammar={}
  for eachElement in grammar_list:
    eachElement = eachElement.replace(" ","")
    production = eachElement.split("->")
    if production[0] in grammar:
        grammar[production[0]].append(production[1])
    else:
        grammar[production[0]] = [production[1]]

  return grammar

def find_follow(grammar):
  follow_not_found_dictionary ={}   
  grammar_dictionary = {}
  list_of_symbols_in_order = []

  for eachGrammarProduction in grammar:
 
     eachGrammarProduction = eachGrammarProduction.split("->")
     eachGrammarProduction[0] = eachGrammarProduction[0].replace(" ","")
     eachGrammarProduction[0] = eachGrammarProduction[0].replace("\n","")
     eachGrammarProduction[1] = eachGrammarProduction[1].replace(" ","")
     eachGrammarProduction[1] = eachGrammarProduction[1].replace("\n","")

     if not(eachGrammarProduction[0] in list_of_symbols_in_order):

      list_of_symbols_in_order.append(eachGrammarProduction[0])

     
     if(eachGrammarProduction[0] in grammar_dictionary):
       grammar_dictionary[eachGrammarProduction[0]].append(eachGrammarProduction[1])

     else:
       grammar_dictionary[eachGrammarProduction[0]] = [eachGrammarProduction[1]]

  follow_dictionary = {}
  first = find_first(grammar_dictionary)
  

  start_symbol = list_of_symbols_in_order[0]
  follow_dictionary[start_symbol] = ['$']

  for everySymbol in list_of_symbols_in_order[1:]:
      follow_dictionary[everySymbol] =[]

  for everySymbol in list_of_symbols_in_order:

      productions_found = find_productions(grammar_dictionary,everySymbol)
      process_productions_found(productions_found,first,follow_dictionary,follow_not_found_dictionary,everySymbol)


  for everySymbol in follow_not_found_dictionary:
    if len(follow_not_found_dictionary[everySymbol]) != 0:
      for NonTerminal in follow_not_found_dictionary[everySymbol]:
        for eachTerminal in follow_dictionary[NonTerminal]:
          if eachTerminal not in follow_dictionary[everySymbol]:
            follow_dictionary[everySymbol].append(eachTerminal)


  return follow_dictionary


def find_productions(grammar , symbol):
    
    productions_found_dictionary = {}
    for eachKey in grammar:
        temp_list = []
        for eachElement in grammar[eachKey]:
            
            if symbol in eachElement:
                temp_list.append(eachElement)

        productions_found_dictionary[eachKey] = temp_list

    for eachKey in productions_found_dictionary:
      if len(productions_found_dictionary[eachKey]) == 0:
        productions_found_dictionary[eachKey] = "X"

    dict2 ={}
    for eachKey in productions_found_dictionary:
        if productions_found_dictionary[eachKey]!="X":
            dict2[eachKey]=productions_found_dictionary[eachKey]

    productions_found_dictionary = dict2

            
    return productions_found_dictionary  


def process_productions_found(productions,first,follow,follow_not_found_dictionary,symbol):
       
    follow_not_found_dictionary[symbol] = []

    for eachLeftHandSide in productions:
       
       
       for eachRightHandSide in productions[eachLeftHandSide]:
         flag = 0
         i = -1 


         for everyCharacter in eachRightHandSide:
          if(flag == 0):
             i = i+ 1 
             if everyCharacter == symbol:
                 flag = 1
                
                 if((i+1)==len(eachRightHandSide)):

  

                     

                     if not(eachLeftHandSide == eachRightHandSide[i]):
                         
                         if len(follow[eachLeftHandSide]) == 0:

                              follow_not_found_dictionary[symbol].append(eachLeftHandSide)
                         else:
                               for everySymbol in follow[eachLeftHandSide]:
                                 if not(everySymbol in follow[symbol]):
                                  follow[symbol].append(everySymbol)


                     else:
                          if not ("$" in follow[symbol]):
                              follow[symbol].append("$")


                                          
                 else:
                     
                     temp_list = []
                     first_union_flag = 0
                     no_of_non_terminals_found_continuously = 0;
                     no_of_epsolon = 0
                     
                            
                     for s in range((i+1),len(eachRightHandSide)):
                         if not(eachRightHandSide[s].isupper()):
 
                            first_union_flag = 1
                            temp_list.append(eachRightHandSide[s])
                            no_of_non_terminals_found_continuously = 0;
                            no_of_epsolon = 0
                            break


                         else:
                              no_of_non_terminals_found_continuously =  no_of_non_terminals_found_continuously + 1
                              has_epsolon_flag = 0

                              for eachTerminal in first[eachRightHandSide[s]]:
                                
                                  if eachTerminal == "e":
                                      no_of_epsolon = no_of_epsolon +1
                                      has_epsolon_flag =1

                                  else:

                                      if not(eachTerminal in temp_list):
                                          temp_list.append(eachTerminal)

                              if has_epsolon_flag == 0:
                                break

                     if first_union_flag == 1:
                         for eachSymbol in temp_list:
                             follow[symbol].append(eachSymbol)

                     elif no_of_non_terminals_found_continuously == no_of_epsolon and not(no_of_non_terminals_found_continuously == 0):
                         for m in follow[eachLeftHandSide]:
                             if not(m in follow[symbol]):
                                 follow[symbol].append(m)

                         for a in temp_list:
                             if not(a in follow[symbol]):
                                 follow[symbol].append(a)

                              

                     elif no_of_non_terminals_found_continuously != no_of_epsolon:
                          for n in temp_list:
                              if not(n in follow[symbol]):
                                  follow[symbol].append(n)
                                  

             else:
                 continue

if __name__ == '__main__':
        
    file_name = "grammar.txt"
    grammar = read_grammar(file_name)
    print(find_follow(grammar))


