__author__ = "Harsh"


import re
import copy
from follow import find_follow

#input: file, output: rules in a list
def read_grammar(file_name):

    fp = open(file_name, 'r')

    grammar_productions_list = []

    for eachLine in fp:
        grammar_productions_list.append(eachLine.strip())

    return grammar_productions_list


#input: file, output: rules in a dictionary
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


# --------------------------------------------------------------------------------

# Find Closure--------------------------------------------------------------------


class item:
    def __init__(self):
        self.sl = []
        self.name = " "
        self.fro = " "
        self.on = " "
        self.D = {}

    def setname(self, nu):
        self.name = str(nu)

    def setfron(self, fr, o):
        self.fro = fr
        self.on = o

    def __eq__(self, it):
        if self.sl == item.sl:
            return 1

        else:
            return 0


def findSym(it):
    l = []
    for st in it.sl:
        m = re.search(".*[.](.).*", st)
        if m:
            if m.group(1) not in l:
                l.append(m.group(1))

    return l


def shiftDot(st):
    m1 = re.search("(.*)[.](.)(.*)", st)
    tar = m1.group(1) + m1.group(2) + '.' + m1.group(3)
    return tar


def closure(a, temp, sym):
    temp_list = list()

    for st in a:
        m1 = re.match('(%s)->.*' % sym, st)
        if m1:
            temp.append(m1.group())
            temp_list.append(m1.group())

    for stri in temp:
        if stri in a:
            a.remove(stri)
  

    for s in temp_list:
        m1 = re.search('.*[.](.).*', s)
        if m1:
            ch = str(m1.group(1))
            if (ch != sym) and (ch.isupper()):
                closure(a, temp, ch)


def createspace(string):
    temp = ""
    for s in string:
        c = s + ' '
        temp = temp + c

    return temp


def getclosures(list_):
   
    l = []
    for i in range(len(list_)):
        list_[i] = list_[i].replace(" ", "")

    for st in list_:
 
        l.append(st)


    m = re.search("(.)->.*", l[0])
    ns = 'H' + '->' + m.group(1)
    l.insert(0, ns)

    b = []
    for st in l:
        m = re.search("(.*)->(.*)", st)
        if m.group(2) == 'e':
            s = m.group(1) + '->' + m.group(2) + '.'
            b.append(s)
        else:

            s = m.group(1) + '->' + '.' + m.group(2)
            b.append(s)

    a = []
    onemore = b[:]
    m = re.search(".*[.](.).*", b[0])
    closure(onemore, a, m.group(1))
    a.insert(0, b[0])


    fol = []
    i0 = item()
    i0.setname('0')
    fol.append(i0)

    for st in a:
        i0.sl.append(st)

    visited = []
    count = 0
    for curr_item in fol:
   
        if curr_item.name in visited:
            continue

        else:
            visited.append(curr_item.name)
            symlist = findSym(curr_item)
         
            for sym in symlist:
      
                ni = item()
     

                l1 = []
                for st in curr_item.sl:
                    m1 = re.match('.*[.](.).*', st)
                    if m1 and m1.group(1) == sym:
                        l1.append(m1.group())
   

                l2 = []
                for st in l1:
                    l2.append(shiftDot(st))

   

                for s in l2:
                    ni.sl.append(s)
                    tlist = []
                    m1 = re.search("(.)->.*[.](.).*", s)
                    if m1:
                        ch1 = m1.group(1)
  
                        ch2 = m1.group(2)
              
                        if (ch2.isupper()):
                            onemore = b[:]
                            closure(onemore, tlist, ch2)
                    for stri in tlist:
                        ni.sl.append(stri)

                ni1 = item()

                for st in ni.sl:
                    if st not in ni1.sl:
                        ni1.sl.append(st)

                del (ni)

                ni1.setfron(curr_item.name, sym)

                flag = 1
                for kr in range(0, len(fol)):
                    if fol[kr].sl == ni1.sl:
                        flag = 0
                        name = fol[kr].name[:]
                        ni1.setname(name)
                        break

                if flag == 1:
                    count += 1
                    ni1.setname(count)

                fol.append(ni1)


    lod = []

    for j in range(0, len(fol)):
        d = {}
        d['from'] = [fol[j].fro]
        d['to'] = [fol[j].name]
        d['on'] = [fol[j].on]
        for k in fol[j].sl:
            m1 = re.search("(.)->(.*)", k)
            str1 = m1.group(1)[:]
            str2 = m1.group(2)[:]
            if str1 in d.keys():
                d[str1].append(createspace(str2))
            else:
                d[str1] = [createspace(str2)]

        lod.append(d)

    return lod


# ---------------------------------------------------------------------------------------------------------------------------------------------

# Generate Table-------------------------------------------------------------------------------------------------------------------------------

def shift(a, i, j, K, T):
    for t in T:
        if i in t['from']:
            if a in t['on']:

                if a.isupper():
                    if K[j][a] == '':
                        K[j][a] = t['to'][0]
                    elif K[j][a] == t['to'][0]:
                        pass
                    else:
                        K[j][a] = K[j][a] + t['to'][0]
                else:
                    if K[j][a] == '':
                        K[j][a] = 's' + t['to'][0]

                    elif K[j][a] == 's' + t['to'][0]:
                        pass
                    else:
                        K[j][a] = K[j][a] + 's' + t['to'][0]
    return K



def reduce(u, r, i, K, grammar, follow):
    i1 = int(i)
    r1 = r.split('.')
    r2 = r1[0].replace(' ', '')
    for g in grammar:
        if u == g[0] and r2 == g[1]:
            for f1 in follow[u]:
                if K[i1][f1] == '':
                    K[i1][f1] = 'r' + str(grammar.index(g) + 1)
                elif K[i1][f1] == 'r' + str(grammar.index(g) + 1):
                    pass
                else:
                    K[i1][f1] = K[i1][f1] + " " + \
                        'r' + str(grammar.index(g) + 1)

            return K


def generate_table(grammar1):
    grammar_list = grammar1[:]
    O = getclosures(grammar1)
    grammar = []
    k = 0
    for prod in grammar_list:
        prod = prod.split("->")
        grammar.append(prod)
        s = grammar[k][0].replace(' ', '')
        t = grammar[k][1].replace(' ', '')
        grammar[k][0] = s
        grammar[k][1] = t
        k = k + 1

    follow = find_follow(grammar1)

    max = 0
    for o in O:
        S = o['to']
        integer = int(S[0])
        if integer > max:
            max = integer

    di = {}
    di['$'] = ''
    t = []
    for g in grammar:
        di[g[0]] = ''
        list_ = list(g[1])
        for l in list_:
            di[l] = ''
    L = []

    di['e'] = ''
    di[''] = ''
    del di['e']
    del di['']

  
    for i in range(0, max + 1):
        L.append(copy.deepcopy(di))

    for o in O:
        i = o['to'][0]
        i1 = int(i)
        R = o.items()
        for r in R:
            for r1 in r[1]:
    
                if '.' in r1:
                    pos_of_dot = r1.index('.')

                    if pos_of_dot < (len(r1) - 2):

                        L = shift(r1[pos_of_dot + 2], i, i1, L, O)
 
                    elif pos_of_dot == len(r1) - 2:
                        if len(r1) == 4:

                            r2 = r1.split('.')
                            r3 = r2[0].split(' ')

                            if r3[0] == grammar[0][0] and r[0] == 'H':
                                L[i1]['$'] = 'accept'
                            else:
                                L = reduce(r[0], r1, i, L, grammar, follow)
                        else:
                            L = reduce(r[0], r1, i, L, grammar, follow)

    return L


# --------------------------------------------------------------------------------------------------------------------
# Input Parsing-------------------------------------------------------------------------------------------------------
def parse_input(grammar_list, input_):
    grammar = grammar_list[:]

    table = generate_table(grammar_list)
    return_value = []
    stack = ['0']
    symbols = ['$']
    if len(input_) == 0:
        return "Empty string"
    temp = []
    for i in input_:
        temp.append(i)

    input_ = temp
    input_.append("$")

    try:
        state = table[int(stack[len(stack) - 1])][input_[0]]
        while state != "":
            current_line = {}
            current_line["stack"] = str(stack)
            current_line["symbols"] = str(symbols)
            current_line["input"] = str(input_)
            current_line["state"] = state
            if state.startswith('s'):
    
                stack.append(state[1:])
                symbols.append(input_.pop(0))
                state = table[int(stack[len(stack) - 1])][input_[0]]
            elif state.startswith("r"):
    
                prev_state = state[:]
                length = len(grammar[int(prev_state[1:]) -
                                     1].split("->")[1].strip().split(" "))
                check_eps = grammar[int(
                    prev_state[1:]) - 1].split("->")[1].replace(" ", "")
                if check_eps != "e":
                    for i in range(length):
                        stack.pop()
                next_state_num = table[int(stack[len(stack) - 1])][
                    grammar[int(prev_state[1:]) - 1].split("->")[0].strip()]
                stack.append(next_state_num)
                symbols = symbols[0:len(symbols) - length]
                next_symbol = grammar[int(prev_state[1:]) - 1][0]
                symbols.append(next_symbol)
                state = table[int(stack[len(stack) - 1])][input_[0]]
            elif state.startswith("a"):
 
                state = table[int(stack[len(stack) - 1])][input_[0]]
   
                break
            return_value.append(current_line)
        else:
            current_line = {}
  
            current_line["stack"] = str(stack)
            current_line["symbols"] = str(symbols)
            current_line["input"] = str(input_)
            current_line["state"] = "reject"
     
        return_value.append(current_line)
    except KeyError:
  
        return "String symbol not in grammar"
    return return_value


# --------------------------------------------------------------------------------------------------------------------------------------------------------------


def dfa(fl):
    statelist = []
    aug = fl[0]["H"][0][2]+"'"

    for d in fl:
        # print(d)
        if d['to'][0] not in statelist:
            statelist.append(d['to'][0])

            print("State "+"I"+d['to'][0]+":")
            print("-------------")
            for i in d:
                if i != "from" and i != "to" and i != "on":

  
                    for j in d[i]:
                        if i == "H":
                            print(aug+" - > ", end="")
                            print(j)

                        else:
                            print(i+" - > ", end="")
                            print(j)
            print("")

    print("Transitions:")
    print("-------------------")

    for i in fl:

        if i["from"][0] != " ":
            print("I"+i["from"][0]+" on "+i["on"]
                  [0]+" goes to "+"I"+i["to"][0])


def OrderingOfList(uli):
    oli = []
    for i in uli:
        tempdict = {}
        for j in i:
            if j.islower():
                tempdict[j] = i[j]
        tempdict["$"] = i["$"]

        for j in i:
            if j.isupper():
                tempdict[j] = i[j]

        oli.append(tempdict)

    return oli



def Steps(x):

    print()
    print("Following are the parsing steps : ")
    print("---------------------------------------------")

    st = "x"
    for i in x:
        ll = []

        if st[0] == "r":
            for j in i:

                ll.append(i[j])

            
            print("goto["+ll[0][len(ll[0])-8]+","+ll[1][len(ll[1])-3]+"] = "+ll[0][len(ll[0])-3])
            
            st = i["state"][0]
            print()
            print("action["+ll[0][len(ll[0])-3]+","+ll[2][2]+"] = "+ll[3])
            print()
            


        else:
            for j in i:
 
                ll.append(i[j])

        

            print("action["+ll[0][len(ll[0])-3]+","+ll[2][2]+"] = "+ll[3])
            print()
            st = i["state"][0]
    print()
    print("                   THE END                   ")
    print("---------------------------------------------")
    print()


def supertable(baa):

    print()
    print()
    print("Parsing Table:")
    print("---------------------------------------------")
    print("\t    Action", end="")
    print("\t\t  Goto")
    print()

    a = baa[0]
    print("", end="\t")
    [print(i, end="\t") for i in (a)]
    print()
    print("---------------------------------------------")

    count = 0
    for i in range(len(baa)):
        print(count, end="\t")
        for j in baa[i].values():
            print(j, end="\t")
        print()
        count += 1



#Main Program Starts from here.

filename = "grammar.txt"
grammar = read_grammar(filename)

#Printing grammar
print("grammar:")
print("---------------------------------------------")
for i in grammar:
    print(i)
print()
print()


# Finding and printing Closures
dfa(getclosures(grammar))


# Printing table
supertable(OrderingOfList(generate_table(grammar)))

# Parsing String
grammar = read_grammar(filename)
print()
print()
print("Parsing a string:")
print("---------------------------------------------")
input_ = input("Enter input string:\n").strip()


#Printing Steps
x = parse_input(grammar, input_)
if x == "String symbol not in grammar":
    print(x)

else:
    Steps(x)

            
    
        

