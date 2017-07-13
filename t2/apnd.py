
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
	
	def __init__(self,name):
		self.estados = []
		self.transicao = []
		self.fita = ''
		self.fila = []
		self.contador = 0
		self.readFile(name)
		
	def readFile(self,name):
		arq = open(name,"r")
		if(arq == None):return None
		getFirst = 0
		
		while True:
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
		
			if("::=" in a and getFirst==1):
				a = a.replace("::=", "|")
				a = a.split("|")
				a = [(i.strip()) for i in a]
			
				self.estados[cont] = a[0].split(",")
				a.remove(a[0])
				for i in range(0,len(a)):
					temp = ' '.join(a[i].split())
					temp = temp.replace(" ","$")
					self.transicao[cont].append(temp)
					#rowns[contador].append(numeros)
					numeros+=1
				#for i in range(0,len(a)):
				cont+=1
			elif(getFirst == 1):
				aux = ' '.join(a.split())
				aux = aux.replace(" ","$")
				#aux = a.replace(" ","$")
				##aux = a.split(" ")
				aux = [(i.strip()) for i in aux]
				self.fita = ''.join(aux)
				#print(fita)
			elif(getFirst == 0):
				self.contador+=1
				
			
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


	def copyStack(self,ex,cpy):
		pilha = Pilha()
	
		for i in range(0,len(ex.dados)):
			pilha.empilha(ex.dados[i])
		pilha.empilha(cpy)
		return pilha

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
			
	def bfs(self,pos,limit):
		#global transicao
	
		while pos<len(self.fila):
			if(pos > limit):break
			
			n = self.fila[pos].topo()
			
			test = self.getSymbol(n[1],n[2])
			if(test[0]=='' and test[1]==''):
				copy = []
				for i in range(len(self.fila[pos].dados)):
					nx = [self.fila[pos].dados[i][0],self.fila[pos].dados[i][1].replace("$",""),self.fila[pos].dados[i][2].replace("$","")]
					copy.append(nx)
				print(copy)
				return 1
				
			elif(test[0]=='' and test[1]!=''):
				n = self.getState(n[0],'',test[1])
			elif(test[0]!='' and test[1]==''):
				n = self.getState(n[0],test[0],'')
			else:
				n = self.getState(n[0],test[0],test[1])
				
			if n>=0:
				for i in range(len(self.transicao[n])):
					data = self.fila[pos].topo()
					
					new = self.transicao[n][i].split(",")
					
					if(test[0]==test[1]):
						if(data[1]=='' and data[2]==''):
							#print(fila[pos].dados)
							return 1
						else:
							fit = data[1]
							st = data[2]
							fit = fit[len(test[0])+1:len(fit)]
							st = st[len(test[1])+1:len(st)]
							#st = new[1]+st
							#st = ' '.join(st.split())
							#st = st.replace(" ","$")
							nx = [new[0],fit,st]
							pilha = self.copyStack(self.fila[pos],nx)
							self.fila.append(pilha)
							#atual+=1
					else:
						#if((data[1][0].isupper() is not True) & (data[2][0].isupper() is not True)):
						#print(str(data[1][0])+" " + str(data[2][0]))					
						#	print("Sequencia nao reconhecida2")
						#continue
						#return -1
						if((test[0].isupper() is not True) & (test[1].isupper() is not True)==False):
							st = data[2]
							st = st[len(test[1]):len(st)]
							st = new[1]+st
							if(st[0]=="$"):
								st = st[1:len(st)]
							#st = st.replace(" ","")
							nx = [new[0],data[1],st]
							pilha = self.copyStack(self.fila[pos],nx)
							self.fila.append(pilha)
							#atual+=1
			pos+=1
		
		return 0							
	
	def execute(self,limit):
	
		pilha = Pilha()
		pilha.empilha([self.estados[0][0],self.fita,self.estados[0][2]])
	
		self.fila.append(pilha)
		if(self.bfs(0,limit)==0):
			print("Sequencia nao reconhecida")