#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' 
* 	Universidade Federal da Fronteira Sul
*
* 	TRABALHO II
*	Disciplina: Linguagens formais e automâtos
*  Professor: Braulio Adriano de Mello
*
*  Aluno: Edson Lemes da Silva
*
*
*	A aplicação consiste em ler um arquivo de 
*  entrada contendo um conjunto de transições
*  para um APND, juntamente com uma sequência de
*  símbolos para ser analisado. O reconhecimento
*  da sequência é feita por Pilha vazia.
*
*	No final, caso for acontecer o reconhecimento,
*  exibe-se a execução no autômato de pilha que 
*  levou ao estado de aceitação. Caso contrário,
*  é imprimido uma mensagem de rejeição.
*
'''
class Pilha(object):
    def __init__(self):
        self.dados = []
        #self.est = []
        #self.parent = -1 
 
    def empilha(self, elemento):
        self.dados.append(elemento)
        #self.est.append(num)
        #self.parent = num
    def desempilha(self):
        if not self.vazia():
            return self.dados.pop(-1)
 
    def vazia(self):
        return len(self.dados) == 0
    def topo(self):
    	  return self.dados[-1]
        
class Ap:
	
	def __init__(self,name,debug=False):
		#lista de estados de transicao
		self.estados = []
		
		#lista de transicao para cada estado
		self.transicao = []
		
		#conteudo da fita
		self.fita = ''
		
		#lista de fila
		self.fila = []
		
		#contador de transicoes
		self.contador = 0
		
		#Le o arquivo 
		self.readFile(name)
		self.debug = debug
	
	#Imprime um elemento da fila na posicao passada por parametro
	def printData(self,pos):
		data = []
		for i in range(0,len(self.fila[pos].dados)):
			nx =  [self.fila[pos].dados[i][0],self.fila[pos].dados[i][1].replace("$",""),self.fila[pos].dados[i][2].replace("$","")]
			data.append(nx)
		print(data)
	#Le o arquivo de entrada
	#@para: name: nome do arquivo a ser lido	
	def readFile(self,name):
		arq = open(name,"r")
		if(arq == None):return None
		getFirst = 0
		
		while True:
			#Le linha por linha
			a = arq.readline()
		
			if(len(a)==0 or len(a)==1):
				if(getFirst==0):
					getFirst = 1
					arq.seek(0)
					cont = 0
					[(self.estados.append([])) for i in range(0,self.contador-1)]
					[(self.transicao.append([])) for i in range(0,self.contador-1)]
					#[(rowns.append([])) for i in range(0,self.contador-1)]
					self.contador-=1
					numeros = 0
					continue
				else: break
			
		   #Verifica se esta no formato correto
			if("::=" in a and getFirst==1):
				a = a.replace("::=", "|")
				a = a.split("|")
				a = [(i.strip()) for i in a]
			
				#Acrescenta o estado na lista				
				self.estados[cont] = a[0].split(",")
				a.remove(a[0])
				
				#Substitui os espacos em branco por '$' e coloca na lista
				#de transicao
				for i in range(0,len(a)):
					temp = ' '.join(a[i].split())
					temp = temp.replace(" ","$")
					self.transicao[cont].append(temp)
					#rowns[contador].append(numeros)
					numeros+=1
				#for i in range(0,len(a)):
				cont+=1
			elif(getFirst == 1):
				
				#coloca na fita os elementos lido e substitui
				#espacos vazios por '$'
				aux = ' '.join(a.split())
				aux = aux.replace(" ","$")
				
				aux = [(i.strip()) for i in aux]
				self.fita = ''.join(aux)
				#print(fita)
			elif(getFirst == 0):
				#Conta o numero de transicao
				self.contador+=1
				
			
	#Procura nos estados da pilha aquele que melhor atende ao topo da pilha
	#@param: nro : numero do estado
	#@param: topo : simbolo no topo da fita
	#@param: state: simbolo no topo da pilha		
	def getState(self,nro,topo,state):
		#global estados
	
		if topo == state:
			for i in range(0,len(self.estados)):
				if((nro==self.estados[i][0] and topo==self.estados[i][1]) and state==self.estados[i][2]):
					return i
		else:
			if(topo.isupper() is not True and state.isupper() is not True):
				return -1
			for i in range(0,len(self.estados)):
				if(nro==self.estados[i][0] and state==self.estados[i][2]):
					return i
		return -1


   #Copia todos os elementos de uma pilha
	def copyStack(self,ex,cpy):
		pilha = Pilha()
	
		for i in range(0,len(ex.dados)):
			pilha.empilha(ex.dados[i])
		pilha.empilha(cpy)
		return pilha


	
      	   	
   #Verifica cada simbolo ou estado
   #@param: fit : conteudo da fita, pilha: conteudo da pilha
	def getSymbol(self,fit,pilha):
		n=fit.find("$")
		n1=pilha.find("$")
	
		if(n>-1 and n1==-1):
			return fit[0:n],pilha
		elif(n==-1 and n1>-1):
			return fit,pilha[0:n1]
		elif(n>-1 and n1>-1):
			return fit[0:n],pilha[0:n1]
		else:
			return fit,pilha
	
	#Algoritmo busca em largura
	#@param: pos: posicao inicial da fila, limit: limite de busca		
	def bfs(self,pos,limit):
		#global transicao
	
		while pos<len(self.fila):
			if(pos > limit):break
			
         #Elemento do topo da pilha para estado que esta na fila			
			n = self.fila[pos].topo()
			
			test = self.getSymbol(n[1],n[2])
			#Imprime o elemento no topo da pilha
			if(self.debug==True):
				self.printData(pos)
			
			#Testa se condicao de pilha vazia eh aceita
			if(test[0]=='' and test[1]==''):
				print("Sequencia reconhecida:")
				
				self.printData(pos)
				return 1
				
			elif(test[0]=='' and test[1]!=''):
				n = self.getState(n[0],'',test[1])
			elif(test[0]!='' and test[1]==''):
				n = self.getState(n[0],test[0],'')
			else:
				n = self.getState(n[0],test[0],test[1])
			
			#se for um estado valido	
			if n>=0:
				#Acrescenta na fila uma instancia para todas as 
				#transicoes do estado sendo estado
				for i in range(len(self.transicao[n])):
					data = self.fila[pos].topo()
					
					new = self.transicao[n][i].split(",")
					
					#se o topo da fita e pilha sao iguais, remove-os
					if(test[0]==test[1]):
						if(data[1]=='' and data[2]==''):
							#print(fila[pos].dados)
							return 1
						else:
							fit = data[1]
							st = data[2]
							fit = fit[len(test[0])+1:len(fit)]
							st = st[len(test[1])+1:len(st)]
							
							nx = [new[0],fit,st]
							pilha = self.copyStack(self.fila[pos],nx)
							self.fila.append(pilha)
							
					else:
						#Caso contrario acrescenta no topo da pilha sem remover nada
						# da fita
						if((test[0].isupper() is not True) & (test[1].isupper() is not True)==False):
							st = data[2]
							st = st[len(test[1]):len(st)]
							st = new[1]+st
							if(st[0]=="$"):
								st = st[1:len(st)]
							
							nx = [new[0],data[1],st]
							pilha = self.copyStack(self.fila[pos],nx)
							self.fila.append(pilha)
				
			pos+=1
		
		return 0							
	
	#Funcao principal que executa a verificacao
	#@param: limit : condicao secundaria de parada
	def execute(self,limit):
	
		pilha = Pilha()
		pilha.empilha([self.estados[0][0],self.fita,self.estados[0][2]])
	
	   #inicializa a fila com o primeiro elemento
		self.fila.append(pilha)
		if(self.bfs(0,limit)==0):
			print("Sequencia nao reconhecida")