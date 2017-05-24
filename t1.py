from collections import defaultdict
from terminaltables import AsciiTable
import itertools

#pip install terminaltables
#table_data
#[['Heading1', 'Heading2'], ['row1 column1', 'row1 column2'], ['row2 column1', 'row2 column2'], ['row3 column1', 'row3 column2']]
# table = AsciiTable(table_data)
# print(table.table)
states = 0
op = 0
auto = defaultdict(list)
mapGrammar = {}
symbol  = list()


def printAFND():
	flag = 1
	##print("_____|    " + "    ".join([chr(i) for i in symbol]))
	header = ['']*(len(symbol)+1)
	header[0] = "  "
	vet = ["  " + chr(i) + " " for i  in symbol]
	
	for i in vet:	
		header[flag] = i
		flag = flag + 1
	row = ['']*(len(symbol)+1)
	tableAFND = ['']
	tableAFND[0] = header
	#tableAFND = "[[" + ','.join(header) + "],"
	for i in auto.keys():
		estado = ""
		row = list(row)
		flag = 0
		estado = mapGrammar.keys()[mapGrammar.values().index(i)]
		if(estado[-1] == 'f'):
			row[flag] = "*" +estado[0:-1]
			
		else:
			row[flag] = estado
		flag = flag + 1
		
		for j in auto[i]:
			estado = ""
			if(type(j) is list):
				
				#print("j" + str(j))
				for k in j:
					estado = estado + mapGrammar.keys()[mapGrammar.values().index(k)]
					if("f" in estado):
						estado = estado[:-1]					
					estado = estado +","
				estado = estado[:-1]+" "
				
			elif(j == ''):
				
				estado = estado + "   -   " 
			else:
				#print("    " + mapGrammar.keys()[mapGrammar.values().index(j)] + "  ")
				estado = estado  + "   "+ mapGrammar.keys()[mapGrammar.values().index(j)]
								
				if("f" in estado):
					estado = estado[:-1]			
			row[flag] = estado			
			flag = flag + 1
		tableAFND.append(row)
		
	table = AsciiTable(tableAFND)
	print(table.table)
	
	#print(tableAFND)

def deltaAux(i,j,sname):
	
	t = list(itertools.permutations(sname))
	flagd = 0
	for k in t:
		st = str(k)
		st = st[1:-1]
		
		if(st in mapGrammar or st+"f" in mapGrammar):
			flagd = 1
	
	sname = str(sname)
	sname = sname[1:-1]
	if sname+"f" in mapGrammar:
		sname = sname+"f"
	
	
	if(flagd == 0):
		mapGrammar[sname] = states
		auto[states] = ['']*(len(symbol))
		states = states + 1
	auto[i][j] = mapGrammar[sname]
	
def determinize():
	
	for i in auto.keys():
		est = mapGrammar.keys()[mapGrammar.values().index(i)]
		est1 = est
		if(est[0].isalpha() is not True):
			est = est.split(",")
			est = [(k.strip()) for k in est]
			#for (l,j) in enumerate(auto[i]):
				for k in range(symbol):
					nv = list()
					for  m in est:
						test = mapGrammar.keys()[mapGrammar.values().index(int(m))]
						if("f" in test):
							copy = mapGrammar[est1]
							mapGrammar[est1 + "f"] = copy
							mapGrammar.pop(est1)	
						
						if(auto[int(m)][k] != ''):
							nv.append(auto[int(m)][k])
					if(len(nv)==1):
						auto[i][k] = nv[0]					
					if(len(nv)>=2):
						deltaAux(i,k,nv)
						
						
		else:			
			for (l,j) in enumerate(auto[i]):
				if(type(j) is list):
					deltaAux(i,l,j)
			
						 	
						
		

def ruleCopy(sbol,nterm,state):
	idt = mapGrammar[state]
	indx = mapGrammar[nterm]
	
	y = symbol.index(ord(sbol))
	#print(str(idt) +" "+ str(y))
	if(auto[idt][y]!=''):
		#print(len(auto[idt][y]))
		
		if(type(auto[idt][y]) is list):
			vet = auto[idt][y]
		else:
			vet = [auto[idt][y]]
		if(indx not in vet):
			vet.append(mapGrammar[nterm])
			if(len(vet) > len([auto[idt][y]])):
				auto[idt][y] = vet
			
	else:
		#y = symbol.index(ord(sbol))
		auto[idt][y] = mapGrammar[nterm]  
	
def getState(arq,epoch):
	if(('' in arq or ' ' in arq) ):
		return "f"
	else:
		return ""

def getAlphaSymbol(prod,pos1,pos2):
	if(pos1 > 0):
		return prod[0:pos1]
	else: return prod[pos2+1:-1]
	
def grammarReader(rule):
	
	global states
	pos1 = rule[0].find("<")
	pos2 = rule[0].find(">")
	if(pos1<0 or pos2<0):
		return None
	est = rule[0][pos1+1:pos2]
	est = est  + getState(rule,0)
	
	
	if(est not in mapGrammar.keys()):
		if('S' == est and (est not in mapGrammar.keys())):
			mapGrammar[est] = 0
			auto[0] =  ['']*len(symbol)
			states = states + 1
		elif(('f' in est) and ( est[0:-1] in mapGrammar.keys())):
			copy = mapGrammar[est[0:-1]]
			mapGrammar[est] = copy
			mapGrammar.pop(est[0:-1])
			
		else:
			mapGrammar[est] = states
			auto[states] =  ['']*len(symbol)
			states = states + 1 
	init = est
	
	for i in range(1,len(rule)):
		if(rule[i]!=' ' and rule[i]!=''):
			pos1 = rule[i].find("<")
			pos2 = rule[i].find(">")
			est = rule[i][pos1+1:pos2]
			
			if(pos1<0 and pos2<0):
				est = "TEf"
				if(est not in mapGrammar.keys()):
					mapGrammar[est] = states
					auto[states] =  ['']*len(symbol)
					states = states + 1
				
				ruleCopy(rule[i],est,init)
			else:					
				if(est + "f" in mapGrammar.keys()):
					est = est + 'f'
				if(est not in mapGrammar.keys()):
					mapGrammar[est] = states	
					auto[states] =  ['']*len(symbol)
					states = states + 1
				sbol = getAlphaSymbol(rule[i],pos1,pos2)	
				
				ruleCopy(sbol,est,init)
		
			
def tokenReader(rule):
	global states
	if('Sf' in mapGrammar.keys()):
		init = 'Sf'
	else: init = 'S'
	#est = "t" + str(states)
	#if(est not in mapGrammar.keys()):
#		mapGrammar[est] = states
#		auto[states] = list()
#		states = states + 1
#	sbol = rule[0]
#	symbol.append(ord(sbol[0]))
#	ruleCopy(sbol,est,init)
#	last = est
	for i in range(0,len(rule)):
		if(states == 0):
			mapGrammar[init] = states
			auto[states] = ['']*len(symbol)
			states = states + 1
		if(i == len(rule)-1):
			est = "T" + str(states) + "f"
		else:
			est = "T" + str(states)
		if(est not in mapGrammar.keys()):
			mapGrammar[est] = states
			auto[states] = ['']*len(symbol)
			states = states + 1
		#if ord(rule[i]) not in symbol:
	#		symbol.append(ord(rule[i]))
		ruleCopy(rule[i],est,init)
		init = est

def countAlphabetSymbols(string,tipo):
	if(tipo == 0):
		for i in range(1,len(string)):
			pos1 = string[i].find("<")
			pos2 = string[i].find(">")
			if(pos1>=0 and pos2>=0):
				sbol = getAlphaSymbol(string[i],pos1,pos2)
				if(ord(sbol) not in symbol):
					symbol.append(ord(sbol[0]))
	else:
		for i in range(0,len(string)):
			if(ord(string[i]) not in symbol):
				symbol.append(ord(string[i]))
				
def fileReader(name):
	f = open(name,"r")
	if(f == None):return None
	getFirst = 0
	ty = 0
	while True:
		a = f.readline()
		
		if(len(a) == 0 or len(a)==1):
			if(getFirst == 0):
				getFirst = 1
				f.seek(0)
				continue
			else: break
			
		
		if("::=" in a):
			a = a.replace('::=', '|')
			a = a.split("|")
			a = [(i.strip()) for i in a]
			op = 0
			
		else:
			a = a.strip()
			op = 1
		
		if(getFirst == 0):
			countAlphabetSymbols(a,op)
		
		if(op == 0 and getFirst == 1):
			#countAlphabetSymbols(a,op)
			if(ty == 0):			
				print(auto)
				print(mapGrammar)
				
				#print("aaa")
			ty = ty  +1
			grammarReader(a)
		elif(op == 1 and getFirst == 1):
			
			#countAlphabetSymbols(a,op)
			tokenReader(a)
			
		
fileReader("test.in")
