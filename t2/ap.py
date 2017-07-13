estados = []
transicao = []
rowns = []
fita = ''
count  =0
ex = []
class Pilha(object):
    def __init__(self):
        self.dados = []
        self.est = []
        self.parent = -1 
 
    def empilha(self, elemento,num):
        self.dados.append(elemento)
        #self.est.append(num)
        self.parent = num
 
    def filhos(self):
    	  return self.est
    def desempilha(self):
        if not self.vazia():
            return self.dados.pop(-1)
 
    def vazia(self):
        return len(self.dados) == 0
    def topo(self):
    	  return self.dados[-1]
        

def readFile(name):

	arq = open(name,"r")
	if(arq == None):return None
	getFirst = 0
	global count 
	global fita
	while True:
		a = arq.readline()
		
		if(len(a)==0 or len(a)==1):
			if(getFirst==0):
				getFirst = 1
				arq.seek(0)
				contador = 0
				[(estados.append([])) for i in range(0,count-1)]
				[(transicao.append([])) for i in range(0,count-1)]
				[(rowns.append([])) for i in range(0,count-1)]
				count-=1
				numeros = 0
				continue
			else: break
		
		if("::=" in a and getFirst==1):
			a = a.replace("::=", "|")
			a = a.split("|")
			a = [(i.strip()) for i in a]
			
			estados[contador] = a[0].split(",")
			a.remove(a[0])
			for i in range(0,len(a)):
				temp = ' '.join(a[i].split())
				temp = temp.replace(" ","$")
				transicao[contador].append(temp)
				rowns[contador].append(numeros)
				numeros+=1
			#for i in range(0,len(a)):
			contador+=1
		elif(getFirst == 1):
			aux = ' '.join(a.split())
			aux = aux.replace(" ","$")
			#aux = a.replace(" ","$")
			##aux = a.split(" ")
			aux = [(i.strip()) for i in aux]
			fita = ''.join(aux)
			#print(fita)
		elif(getFirst == 0):
			count+=1
				
			
def getState(nro,topo,state):
	global estados
	
	if topo == state:
		for i in range(0,len(estados)):
			if((nro==estados[i][0] and topo==estados[i][1]) and state==estados[i][2]):
				return i
	else:
		if(topo.isupper() is not True and state.isupper() is not True):
			return -1
		for i in range(0,len(estados)):
			if(nro==estados[i][0] and state==estados[i][2]):
				return i
	return -1

def checkCond(data,atual,limit):
	
	#rt = 
	rt = data[1:len(data)]
	if len(rt)>=limit:
		for i in range(0,len(rt)):
			if atual!= rt[i]:
				return 0
		return 1
	return 0 


def copyStack(ex,cpy):
	pilha = Pilha()
	
	for i in range(0,len(ex.dados)):
		pilha.empilha(ex.dados[i],1)
	pilha.empilha(cpy,1)
	return pilha

def getSymbol(fit,pilha):
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
			
def bfs(fila,pos,atual,prox):
	global transicao
	
	while pos<len(fila):
		n = fila[pos].topo()
		#print(n)
		test = getSymbol(n[1],n[2])
		if(test[0]=='' and test[1]==''):
			copy = []
			for i in range(len(fila[pos].dados)):
				nx = [fila[pos].dados[i][0],fila[pos].dados[i][1].replace("$",""),fila[pos].dados[i][2].replace("$","")]
				copy.append(nx)
			print(copy)
			return 1
			#n=getState(n[0],'','')
		elif(test[0]=='' and test[1]!=''):
			n = getState(n[0],'',test[1])
		elif(test[0]!='' and test[1]==''):
			n = getState(n[0],test[0],'')
		else:
			n = getState(n[0],test[0],test[1])
		#if n == -1:
		#	print("Sequencia nao reconhecida1")
			#continue
			#return -1
		if n>=0:
			for i in range(len(transicao[n])):
				data = fila[pos].topo()
				print(data)
				new = transicao[n][i].split(",")
				print(new)
				print(test)
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
						pilha = copyStack(fila[pos],nx)
						fila.append(pilha)
						atual+=1
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
						pilha = copyStack(fila[pos],nx)
						fila.append(pilha)
						atual+=1
		pos+=1
		
	return 0							
	
def execute():
	
	global ex
	global estados
	global transicao
	#ex.append([estados[0][0],fita,estados[0][2]])
	atual = 0
	pilha = Pilha()
	pilha.empilha([estados[0][0],fita,estados[0][2]],0)
	#n = pilha.topo()
	#n = getState(n[0],n[1][0],n[2][0])
	#for i in range(0,len(transicao[n])):
	#	atual = atual +1
	#	pilha.est.append(atual)
	ex.append(pilha)
	bfs(ex,0,1,atual+1)
	#while pilha.vazia is not True:
	#	aux = ex[:]
	#	n = getState(aux[atual-1][0],aux[atual-1][2])