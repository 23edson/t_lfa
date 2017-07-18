#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict
from terminaltables import AsciiTable
from copy import copy
import itertools

#pip install terminaltables
#table_data
#[['Heading1', 'Heading2'], ['row1 column1', 'row1 column2'], ['row2 column1', 'row2 column2'], ['row3 column1', 'row3 column2']]
# table = AsciiTable(table_data)
# print(table.table)
#states = 0
#op = 0
#auto = defaultdict(list)
#mapGrammar = {}
#removidos = {}
#symbol  = list()
''' 
* 	Universidade Federal da Fronteira Sul
*
* 	TRABALHO I
*	Disciplina: Linguagens formais e automâtos
*  Professor: Braulio Adriano de Mello
*
*  Aluno: Edson Lemes da Silva
*
*
*	A aplicação consiste em ler tokens e gramáticas de um
*	arquivo externo, então construir o autômato finito
*	não-determinístico. Posteriormente é feito a determinização
*	e em sequência a minimização do mesmo.
*
*	No final é acrescido um estado de erro para os estados
*	que não estão mapeados.
*
'''
class determinizeAfnd:
	def __init__(self, arq):
		#Constrói os atributos da classe
		
		self.arq = arq
		self.states = 0
		self.op = 0
		self.auto = defaultdict(list)
		self.mapGrammar = {}
		self.removidos = {}
		self.symbol = list()
		self.ready = False
		self.fileReader(self.arq)
	
	'''
		Preenche o AFD com o estado de erro, na aplicação
		o este é identificado como 'X'. Assim todas as posições
		não mapeadas são preenchidas com 'X'.
	'''	
	def fillTable(self):
		self.mapGrammar["Xf"] = self.states
	
	
		for i in self.auto.keys():
			for j in range(len(self.auto[i])):
				if(self.auto[i][j]==''):
					self.auto[i][j] = self.states
		self.auto[self.states] = [self.states] * len(self.symbol)
		self.states = self.states + 1		
	
	#Diferencia quais são estados final e quais não são.			
	def printAux2(self,stg):
		if("f" in stg):
			stg = stg[0:-1]
		stg = stg.split(",")
		stg = [(k.strip()) for k in stg]
		return stg

	#Controla a função printAux
	def subName(self,sb):
		getName = self.printAux(sb)
		sb = getName[0]			
		if(getName[1] == 1):
			sb = sb + "f"
		return sb
	
	#Diferencia AFND e AFD para impressão				
	def printAux(self,sb):
	
		sr= ''
		final =0
		if(sb[0].isalpha() is not True):
			sb = self.printAux2(sb)
			for i in sb:
				if(int(i) in self.mapGrammar.values()):
					p = self.mapGrammar.keys()[self.mapGrammar.values().index(int(i))]
				else:
					p = self.removidos.keys()[self.removidos.values().index(int(i))]
				if(p[0].isalpha() is not True):
					sr = sr + self.printAux(p)[0] 
				else:
					if("f" in p):
						p = p[0:-1]
						final = 1
					sr = sr + p
			return sr,final 
	
		else:
			if("f" in sb):
				sb = sb[0:-1]
				final = 1
			return sb,final  
	
	'''
		A função imprime o AFND ou AFD, usando o pacote terminalTables
		(para formato de tabela). 
	'''
	def printTable(self):
		flag = 2
		##print("_____|    " + "    ".join([chr(i) for i in symbol]))
		header = ['']*(len(self.symbol)+2)
		header[0] = header[1] = "  "
		vet = ["  " + chr(i) + " " for i  in self.symbol]
	
		for i in vet:	
			header[flag] = i
			flag = flag + 1
		row = ['']*(len(self.symbol)+2)
		tableAFND = ['']
		tableAFND[0] = header
		#tableAFND = "[[" + ','.join(header) + "],"
		for i in self.auto.keys():
			if('TEf' in self.mapGrammar.keys()):
				if(i == self.mapGrammar['TEf'] and self.ready is True):
					continue
			estado = ""
			row = list(row)
			row[0] = str(i)
			flag = 1
			estado = self.mapGrammar.keys()[self.mapGrammar.values().index(i)]
			if(estado[0].isalpha() is not True):
				estado =  self.subName(estado) 
			
					
			if(estado[-1] == 'f'):
				row[flag] = "*" +estado[0:-1]
			
			else:
				row[flag] = estado
			flag = flag + 1
		
			for j in self.auto[i]:
				estado = ""
				if(type(j) is list):
				
					#print("j" + str(j))
					for k in j:
						estado = estado + self.mapGrammar.keys()[self.mapGrammar.values().index(k)]
						if("f" in estado):
							estado = estado[:-1]					
						estado = estado +","
					estado = estado[:-1]+" "
				
				elif(j == ''):
				
					estado = estado + "   -   " 
				else:
					#print("    " + mapGrammar.keys()[mapGrammar.values().index(j)] + "  ")
				
					estado = self.mapGrammar.keys()[self.mapGrammar.values().index(j)]				
					if(estado[0].isalpha() is not True):
						estado = self.subName(estado) 
					estado = "   "+ estado
								
					if("f" in estado):
						estado = estado[:-1]			
				row[flag] = estado			
				flag = flag + 1
			tableAFND.append(row)
		
		
		table = AsciiTable(tableAFND)
		if(self.ready == True):
			arq2 = open("automato.txt","w")
			arq2.write(table.table)
			arq2.close()
		print(table.table)
		
			#print(tableAFND)
	#Identifica estados com rótulos iguais (i.e AB = BA)
	def deltaAux(self,i,j,sname):
	
		#global self.states
		t = list(itertools.permutations(sname))
		flagd = 0
		for k in t:
			st = str(k)
			st = st[1:-1]
		
			if(st in self.mapGrammar or st+"f" in self.mapGrammar):
				flagd = 1
	
		sname = str(sname)
		sname = sname[1:-1]
		if sname+"f" in self.mapGrammar:
			sname = sname+"f"
	
	
		if(flagd == 0):
			self.mapGrammar[sname] = self.states
			self.auto[self.states] = ['']*(len(self.symbol))
			self.states = self.states + 1
		self.auto[i][j] = self.mapGrammar[sname]
	
	'''
		Esta função faz a determinização do AFND após a construção do mesmo,
		primeiramente, é verificado estado por estado se há alguma símbolo
		cuja produções contém indeterminismos. Quando esta situação é identificada,
		a função cria um novo estado para com referência para os estados que geraram
		o indeterminismo. Assim, estes novos estados são verificados apenas após a
		análise de todos os estados originais. Novamente, se há símbolos com 
		referência para mais de um estado, é criado um novo, assim segue até
		convergir.	
	
	'''
	def determinize(self):
		kys = list(self.auto.keys())
		for i in kys:
			est = self.mapGrammar.keys()[self.mapGrammar.values().index(i)]
			est1 = est
		
			if(est[0].isalpha() is not True):
			
				est = est.split(",")
				est = [(k.strip()) for k in est]
				
				print("\n")
				print("Verificando novo estado:"+str(i))
				dados = []
				
				for k in range(len(self.symbol)):
					nv = list()
					for  m in est:
						test = self.mapGrammar.keys()[self.mapGrammar.values().index(int(m))]
						test1 = self.mapGrammar.keys()[self.mapGrammar.values().index(i)]
						if("f" in test and "f" not in test1):
							copy = self.mapGrammar[est1]
							self.mapGrammar[est1 + "f"] = copy
							self.mapGrammar.pop(est1)	
						
						if(self.auto[int(m)][k] != ''):
							if(self.auto[int(m)][k] not in nv):
								nv.append(self.auto[int(m)][k])
					if(len(nv)==1):
						self.auto[i][k] = nv[0]	
						string1 = str(chr(self.symbol[k]))+":"+str(nv[0])
						dados.append(string1)				
					if(len(nv)>=2):
						self.deltaAux(i,k,nv)
						#for ty in nv:
						#	print(ty)
						#print(str(i) + " " + str(k))
						string = [str(qr) for qr in nv]
						string = ','.join(string)
						print("Novo Indeterminismo:")
						print("Estado: "+ str(i) + ", Simbolo: " + chr(self.symbol[k])+" / Estados envolvidos:"+ string + "/ Novo:"+str(self.states-1) )
			
				if(len(dados)>0):		
					print("Determinizados")
					print("Simbolos " + ','.join(dados))
				else:
					print("Determinizacao:Ok")			
						
						
			else:			
				for (l,j) in enumerate(self.auto[i]):
					if(type(j) is list):
						self.deltaAux(i,l,j)
						string = [str(qr) for qr in j]
						string = ','.join(string)
						print("Indeterminismo:")
						print("Estado: "+ str(i) + ", Simbolo: " + chr(self.symbol[l])+" / Estados envolvidos:"+ string + "/ Novo:"+str(self.states-1) )
					
						#print(str(len(auto.keys())) + " " +str(len(kys)))
						#print(auto.keys())
						#print(kys)
						 	
			if(len(self.auto.keys()) > len(kys)):
				cpy = set(self.auto.keys())-set(kys)
				[kys.append(x) for x in cpy]
			#print(kys)
		self.minimize()
		self.fillTable()
		self.ready = True	
	
	#Remove estado identificado na minimização		
	def remove_states(self,diff):
		for i in diff:
			val = self.mapGrammar.keys()[self.mapGrammar.values().index(int(i))]
			self.removidos[val] = self.mapGrammar[val]
			self.mapGrammar.pop(val)
			self.auto.pop(i)			

	def exception(self,diff):
		if('TEf' in self.mapGrammar):
			if(self.mapGrammar['TEf'] in diff):
				diff.pop(diff.index(self.mapGrammar['TEf']))
		return diff

	'''
		A função é chamada após a determinização, ela é responsável
		por minimizar o autômato, isto é, eliminar estados inalcançáveis
		e mortos. A requisição destes estados acontece através de uma
		busca em profundidade.
	'''
	def minimize(self):
		new = copy(self.auto)
		visitado = self.dfs(0,new)
		diff = list(set(new.keys())-visitado)
	
		if(len(diff)>0):
			#diff = self.exception(diff)
			self.remove_states(diff)
	
		vetor = []
		for k in self.mapGrammar.values():
			test = self.mapGrammar.keys()[self.mapGrammar.values().index(k)]
			if("f" in test):
				vetor.append(self.mapGrammar[test])
			
		for i in self.auto.keys():
			if('TEf' in self.mapGrammar):
				if(self.mapGrammar['TEf'] == i):
					continue
			visitado = self.dfs(i,new)
			flag = 0	
			for j in vetor:
				if(j in list(visitado)):
					flag = 1
			if(flag == 0):		
				self.remove_states([i])

	#Busca em profundidade não-recursiva		
	def dfs(self,inicio,ws):
		visitado = set()
		pilha = [inicio]
	
		while pilha:
			alf = pilha.pop()
			if(alf not in visitado):
				visitado.add(alf)
				pilha.extend(set(ws[alf]) - visitado)
			
				if('' in pilha):
					tnm = pilha.count('')
					for i in range(int(tnm)):
						pilha.pop(pilha.index(''))
	
		return visitado	
	''' Identifica se é um estado único(determinístico), ou
		 se é um estado múltiplo(não-determinístico). O estado
		 é em relação ao símbolo de alfabeto da linguagem.
		 
	'''	  
	def ruleCopy(self,sbol,nterm,state):
		idt = self.mapGrammar[state]
		indx = self.mapGrammar[nterm]
		
		y = self.symbol.index(ord(sbol))
		
		if(self.auto[idt][y]!=''):
			if(type(self.auto[idt][y]) is list):
				vet = self.auto[idt][y]
			else:
				vet = [self.auto[idt][y]]
			if(indx not in vet):
				vet.append(self.mapGrammar[nterm])
				if(len(vet) > len([self.auto[idt][y]])):
					self.auto[idt][y] = vet
			
		else:
			self.auto[idt][y] = self.mapGrammar[nterm]  
	
	#Acrescenta 'f' se for final
	def getState(self,arq,epoch):
		if(('' in arq or ' ' in arq) ):
			return "f"
		else:
			return ""

	#Identifica formato do tipo a<A>,<A>a	
	def getAlphaSymbol(self,prod,pos1,pos2):
		if(pos1 > 0):
			return prod[0:pos1]
		else: return prod[pos2+1:-1]
	
	''' 
		A função lê a linha passado por parâmetro. Assume-se
		que ela faz parte de uma gramática previamente identificada,
		assim, a tabela de estados do AFND é incrementada/construída
		com os estados descritos nesta linha de acordo com as regras
		e produções.
			
	
	'''
	def grammarReader(self,rule):
	
		#global self.states
		pos1 = rule[0].find("<")
		pos2 = rule[0].find(">")
		if(pos1<0 or pos2<0):
			return None
		est = rule[0][pos1+1:pos2]
		est = est  + self.getState(rule,0)
	
	
		if(est not in self.mapGrammar.keys()):
			if('S' == est and (est not in self.mapGrammar.keys())):
				self.mapGrammar[est] = 0
				self.auto[0] =  ['']*len(self.symbol)
				self.states = self.states + 1
			elif(('f' in est) and ( est[0:-1] in self.mapGrammar.keys())):
				copy = self.mapGrammar[est[0:-1]]
				self.mapGrammar[est] = copy
				self.mapGrammar.pop(est[0:-1])
			
			else:
				self.mapGrammar[est] = self.states
				self.auto[self.states] =  ['']*len(self.symbol)
				self.states = self.states + 1 
		init = est
	
		for i in range(1,len(rule)):
			if(rule[i]!=' ' and rule[i]!=''):
				pos1 = rule[i].find("<")
				pos2 = rule[i].find(">")
				est = rule[i][pos1+1:pos2]
				#print(str(pos1) + " " + str(pos2))
				if(pos1<0 and pos2<0):
					est = "TEf"
					if(est not in self.mapGrammar.keys()):
						self.mapGrammar[est] = self.states
						self.auto[self.states] =  ['']*len(self.symbol)
						self.states = self.states + 1
					
					self.ruleCopy(rule[i],est,init)
					#print(rule[i] + " " + est + " " + init)
				else:					
					if(est + "f" in self.mapGrammar.keys()):
						est = est + 'f'
					if(est not in self.mapGrammar.keys()):
						self.mapGrammar[est] = self.states	
						self.auto[self.states] =  ['']*len(self.symbol)
						self.states = self.states + 1
					sbol = self.getAlphaSymbol(rule[i],pos1,pos2)	
				
					self.ruleCopy(sbol,est,init)
		
	'''
		Após a identificação da linha ser lida, e ser
		dada como token, é feito a chamada desta função
		que incrementa/constrói o AFND com o respectivo
		token passado pelo parâmetro.
	
	'''		
	def tokenReader(self,rule):
		#global self.states
		if('Sf' in self.mapGrammar.keys()):
			init = 'Sf'
		else: init = 'S'
	
		for i in range(0,len(rule)):
			if(self.states == 0):
				self.mapGrammar[init] = self.states
				self.auto[self.states] = ['']*len(self.symbol)
				self.states = self.states + 1
			if(i == len(rule)-1):
				est = "T" + str(self.states) + "f"
			else:
				est = "T" + str(self.states)
			if(est not in self.mapGrammar.keys()):
				self.mapGrammar[est] = self.states
				self.auto[self.states] = ['']*len(self.symbol)
				self.states = self.states + 1
	
			self.ruleCopy(rule[i],est,init)
			init = est

	#Conta os símbolos do alfabeto da linguagem
	def countAlphabetSymbols(self,string,tipo):
		if(tipo == 0):
			for i in range(1,len(string)):
				pos1 = string[i].find("<")
				pos2 = string[i].find(">")
				if(pos1>=0 and pos2>=0):
					sbol = self.getAlphaSymbol(string[i],pos1,pos2)
					if(ord(sbol) not in self.symbol):
						self.symbol.append(ord(sbol[0]))
				elif(len(string[i])==1):
					if(ord(string[i]) not in self.symbol):
						self.symbol.append(ord(string[i]))
		else:
			for i in range(0,len(string)):
				if(ord(string[i]) not in self.symbol):
					self.symbol.append(ord(string[i]))
	
	'''A função fileReader lê o arquivo de entrada e
		identifica o que é token ou gramática.	
		Chamada no construtor da classe.
	'''			
	def fileReader(self,name):
		f = open(name,"r")
		if(f == None):return None
		getFirst = 0
		
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
				self.countAlphabetSymbols(a,op)
		
			if(op == 0 and getFirst == 1):
				self.grammarReader(a)
			elif(op == 1 and getFirst == 1):
				self.tokenReader(a)
			
		
#fileReader("test.in")
#printAFND()
#determinize()
#fillTable()
	
