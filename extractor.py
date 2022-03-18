import numpy as np
import os, os.path
from string import punctuation
from collections import Counter
from itertools import chain
import random
import datetime
import matplotlib.pyplot as plt

now = datetime.datetime.now()
print ("Current date and time : ")
print (now.strftime("%Y-%m-%d %H:%M:%S"))

### GETTING THE TEXT ###

DIR = 'corpus1/'
path, dirs, files = next(os.walk(DIR))
file_count = len(files)
lenames=len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
names=[name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]
i=0
docs={}
total=''
while i<lenames:
    doc=''
    with open(DIR+names[i],encoding="utf8") as file:
        line = file.read().rstrip('\n').lower()
        data=line
        doc=doc+line
        total=total+data
    total=total+' '
    doc=doc+' '
    docs[i]=doc
    i=i+1
data=total


i=0
text=''
foo = 'baz "\\"'
chars=['\t','•',',','”',
       '“','“','!','/','?','‘','(',')','.',':',';','<', '>','"','[',']','+','«','{','}','»','*','´','=', "'",'_','-','-','–','—','%','|',"\n",'@','$','€','\\']
lastspace=0
onegram={}
twogram={}
allinone={}
a=''
omega={}
vowels=['a','e','i','u','o','y','w']

def countInFile(filename):
    with open(filename) as f:
        linewords = (line.translate([None, punctuation]).lower().split() for line in f)
        return Counter(chain.from_iterable(linewords))
        

### WHICH GRAM IS IT? ###
def getGram(count):
    if count==1:
        return onegram
    if count<8:
        
        return allinone
    else:
        return 'Insert valid gram'
    
### Trim expressions ###
def trim(gram):
    if gram[0]==' ':
        gram=gram[1:]
    if gram[-1]==' ':
        gram=gram[:len(gram)-1]
    return gram

### Get splits of expressions ###
def splits(gram):
    gram=gram
    grams=[]
    a=''
    for i in range(len(gram)):
        if gram[i]== ' ':
            grams.append(a)
        a=a+gram[i]
    grams.append(a)
    return grams


def getwords(gram):
    text=''
    res=[]
    for i in range(len(gram)):
        if i==len(gram)-1:
            text=text+gram[i]
            if text not in chars:
                res.append(text)
        else:
            if gram[i]==' ':
                if text not in chars:
                    if(i!=0):
                        res.append(text)
                text=''
            else:
                text=text+gram[i]
    return res

def countgrams(gram):
    count=1
    for i in range(len(gram)-1):
        if gram[i] == ' ' and not gram[i+1]==' ':
            count=count+1
    return count


def getleft(gram):
    x=len(gram)-1
    while x>0:
        if gram[x] ==' ':
            return gram[:x]
        x=x-1

def getright(gram):
    return gram[gram.find(" ")+1:]


####### Cohesion metrics #######

def scp(gram):
    count=countgrams(gram) #ver
    numerator=allinone[gram][0][0]**2
    allgrams=splits(gram) ##ver
    mult=[]
    for x in allgrams:
        if len(x)==len(gram):
            break
        else:
            lenofgram=countgrams(x)
            firstgram=getGram(lenofgram)#Dá o dicionario de Xgram
            if lenofgram==1:
                firstgramfreq=firstgram[x][0]
            else:
                firstgramfreq=firstgram[x][0][0]
    
            secgram=getGram(countgrams(trim(gram[len(x):len(gram)])))
            lenofgram2=countgrams(trim(gram[len(x):len(gram)]))
            if lenofgram2==1:
                secgramfreq=secgram[trim(gram[len(x):len(gram)])][0]
            else:
                secgramfreq=secgram[trim(gram[len(x):len(gram)])][0][0]
            mult.append(firstgramfreq*secgramfreq)
    f=(1/(count-1))*sum(mult)
    scp=numerator/f
    return scp

def phi(gram):
    numgram=countgrams(gram)
    whichgram=getGram(numgram)
    allgrams=splits(gram)
    avq=[]
    avd=[]
    for x in allgrams:
        if len(x)==len(gram):
            break
        else:
            lenofgram=countgrams(x)
            firstgram=getGram(lenofgram)#Dá o dicionario de Xgram
            if lenofgram==1:
                firstgramfreq=firstgram[x][0]
            else:
                firstgramfreq=firstgram[x][0][0]
            lenofgram2=countgrams(trim(gram[len(x):len(gram)]))
            secgram=getGram(lenofgram2)
            if lenofgram2==1:
                secgramfreq=secgram[trim(gram[len(x):len(gram)])][0]
            else:
                secgramfreq=secgram[trim(gram[len(x):len(gram)])][0][0]
            thirdpart=(nwords-firstgramfreq)*(nwords-secgramfreq)
            avq.append(firstgramfreq*secgramfreq)               
            avd.append(firstgramfreq*secgramfreq*thirdpart)
    npequeno=len(gram.split(' '))
    
    numerator=(nwords*whichgram[gram][0][0]-(1/(npequeno-1))*sum(avq))**2 
    res=((npequeno-1)*numerator)/(sum(avd))
    return res

  
def dice(gram):
    count=countgrams(gram)
    xgram=getGram(count)
    numerator=2*xgram[gram][0][0]
    allgrams=splits(gram)
    mult=[]
    for x in allgrams:
        if len(x)==len(gram):
            break
        lenofgram=countgrams(x)
        firstgram=getGram(lenofgram)#Dá o dicionario de Xgram
        if lenofgram==1:
            firstgramfreq=firstgram[x][0]
        else:
            firstgramfreq=firstgram[x][0][0]
        secgram=getGram(countgrams(trim(gram[len(x):len(gram)])))
        lenofgram2=countgrams(trim(gram[len(x):len(gram)]))
        if lenofgram2==1:
            secgramfreq=secgram[trim(gram[len(x):len(gram)])][0]
        else:
            secgramfreq=secgram[trim(gram[len(x):len(gram)])][0][0]
        mult.append(firstgramfreq+secgramfreq)
    f=(1/(count-1))*sum(mult)
    dice=numerator/f
    return dice    

def mi(gram):
    count=countgrams(gram)
    xgram=getGram(count)
    numerator=xgram[gram][0][0]/nwords
    allgrams=splits(gram)
    mult=[]
    for x in allgrams:
        if len(x)==len(gram):
            break
        lenofgram=countgrams(x)
        firstgram=getGram(lenofgram)#Dá o dicionario de Xgram
        if lenofgram==1:
            firstgramfreq=firstgram[x][0]/nwords
        else:
            firstgramfreq=firstgram[x][0][0]/nwords
        secgram=getGram(countgrams(trim(gram[len(x):len(gram)])))
        lenofgram2=countgrams(trim(gram[len(x):len(gram)]))
        if lenofgram2==1:
            secgramfreq=secgram[trim(gram[len(x):len(gram)])][0]/nwords
        else:
            secgramfreq=secgram[trim(gram[len(x):len(gram)])][0][0]/nwords
        mult.append(firstgramfreq*secgramfreq)
    f=(1/(count-1))*sum(mult)
    mi=np.log(numerator/f)
    return mi



### Format text and save 1grams with count ###


def getNrelevant(gram,n):
    if len(gram)>=n:
        return gram[0:n+1]
    else:
        print('Not enough relevant expressions in list')

def getNrandomRelevant(gram,n):
     if len(gram)>=n:
        return random.sample(gram, n)
     else:
        print('Not enough relevant expressions in list')

def avglen(gram):
    soma=0
    words=getwords(gram)
    for x in words:
        soma=soma+len(x)
    d=soma/countgrams(gram)
    return d

def getSylables(gram):
    count=0
    justcounted=False
    g=gram.lower()
    for letter in g:
        if letter in vowels:
            if not justcounted:
                count=count+1
                justcounted=True
            else:
                continue
        else:
            justcounted=False
    return count
   

   
        
''' FORMATTING'''

numspace=0
justspaced=False
size=len(data)
for i in range(size):
    if data[i]=='\n':
        if text[-1]!=' ':
            text=text+" "
            justspaced=True
        continue
    else:
        if i<size-1:    
            if data[i]== ' ' and data[i+1]==' ':
                continue
        
        if data[i] in chars:
            if data[i-1]!=' ' and not justspaced:
                text=text+" "
                justspaced=True
            if i<size-1:
                    if data[i+1]!=' ':
                        text=text+data[i]
                        text=text+" "
                        justspaced=True
                        continue
        justspaced=False
        text=text+data[i]
        
now = datetime.datetime.now()
print ("Time of formatting : ")
print (now.strftime("%Y-%m-%d %H:%M:%S"))




size=len(text)
update=''
for i in range(size-1):
    if text[i]==' ' and text[i+1]==' ':
        continue
    update=update+text[i]
text=update

nwords=len(text.split(' '))

###END OF FORMATTING###

###COUNT FREQUENCY###

###ONEGRAMS###
    
for i in range(len(text)):
    if text[i]==' ':
        if a not in onegram: 
            onegram[a]=[1,0,0,getSylables(a)]
            
        else:
            onegram[a][0]=onegram[a][0]+1
        lastspace=i
        a='' 
    else:
        a=a+text[i]

###TWOGRAMS###

spacecounter=0
a=""
i=0
while i < len(text):
    if text[i]==' ':
        if spacecounter==1:
            if a not in allinone: 
                allinone[a]=[None]*2
                allinone[a][0]=[1,0,0]
                allinone[a][1]=[None]*2
                allinone[a][1][0]=[] #left omegas+1
                allinone[a][1][1]=[] #right omegas
            else:
                allinone[a][0][0]=allinone[a][0][0]+1
            a='' 
            spacecounter=0
            i=lastspace
        else:
            lastspace=i
            spacecounter = spacecounter+1
            a=a+text[i]  
    else:
        a=a+text[i] 
    i=i+1

###THREEGRAMS###

i=0
a=''
spacecounter=0 
while i < len(text):
    if text[i]==' ':
        if spacecounter==2:
            if a not in allinone: 
                allinone[a]=[None]*2
                allinone[a][0]=[1,0,0]
                allinone[a][1]=[None]*2
                allinone[a][1][0]=[]#left omegas+1
                allinone[a][1][1]=[] #right omegas
            else:
                allinone[a][0][0]=allinone[a][0][0]+1
            a='' 
            spacecounter=0
            i=lastspace
        else:
            if spacecounter==0:
                lastspace=i
            spacecounter = spacecounter+1
            a=a+text[i]  
    else:
        a=a+text[i] 
    i=i+1

###FOURGRAMS###

i=0
a=''
spacecounter=0 
while i < len(text):
    if text[i]==' ':
        if spacecounter==3:
            if a not in allinone: 
                allinone[a]=[None]*2
                allinone[a][0]=[1,0,0]
                allinone[a][1]=[None]*2
                allinone[a][1][0]=[] #left omegas+1
                allinone[a][1][1]=[]#right omegas
            else:
                allinone[a][0][0]=allinone[a][0][0]+1
            a='' 
            spacecounter=0
            i=lastspace
        else:
            if spacecounter==0:
                lastspace=i
            spacecounter = spacecounter+1
            a=a+text[i]  
    else:
        a=a+text[i] 
    i=i+1




###FIVEGRAMS###
    
i=0
a=''
spacecounter=0 
while i < len(text):
    if text[i]==' ':
        if spacecounter==4:
            if a not in allinone: 
                allinone[a]=[None]*2
                allinone[a][0]=[1,0,0]
                allinone[a][1]=[None]*2
                allinone[a][1][0]=[] #left omegas+1
                allinone[a][1][1]=[] #right omegas
            else:
                allinone[a][0][0]=allinone[a][0][0]+1
            a='' 
            spacecounter=0
            i=lastspace
        else:
            if spacecounter==0:
                lastspace=i
            spacecounter = spacecounter+1
            a=a+text[i]  
    else:
        a=a+text[i] 
    i=i+1
    
    
    
    
###SIXGRAMS###
    
i=0
a=''
spacecounter=0 
while i < len(text):
    if text[i]==' ':
        if spacecounter==5:
            if a not in allinone: 
                allinone[a]=[None]*2
                allinone[a][0]=[1,0,0]
                allinone[a][1]=[None]*2
                allinone[a][1][0]=[] #left omegas+1
                allinone[a][1][1]=[] #right omegas
            else:
                allinone[a][0][0]=allinone[a][0][0]+1
            a='' 
            spacecounter=0
            i=lastspace
        else:
            if spacecounter==0:
                lastspace=i
            spacecounter = spacecounter+1
            a=a+text[i]  
    else:
        a=a+text[i] 
    i=i+1
    
    
###SEVENGRAMS###
    
i=0
a=''
spacecounter=0 
while i < len(text):
    if text[i]==' ':
        if spacecounter==6:
            if a not in allinone: 
                allinone[a]=[None]*2
                allinone[a][0]=[1,0,0]
                allinone[a][1]=[None]*2
                allinone[a][1][0]=[] #left omegas+1
                allinone[a][1][1]=[] #right omegas
            else:
                allinone[a][0][0]=allinone[a][0][0]+1
            a='' 
            spacecounter=0
            i=lastspace
        else:
            if spacecounter==0:
                lastspace=i
            spacecounter = spacecounter+1
            a=a+text[i]  
    else:
        a=a+text[i] 
    i=i+1

now = datetime.datetime.now()
print ("Time count frequencies : ")
print (now.strftime("%Y-%m-%d %H:%M:%S"))

###END COUNTING FREQUENCY###



###CALCULATE OMEGAS AND GLUE###

for x in allinone:
    scpd=phi(x)
    right=getright(x)
    left=getleft(x)
    allinone[x][0][2]=scpd
    if countgrams(x)==2:
        if onegram[right][1]<scpd:
            onegram[right][1]=scpd
        if onegram[left][1]<scpd:
            onegram[left][1]=scpd
    else:
        if allinone[right][0][1]<scpd:
            allinone[right][0][1]=scpd
        if allinone[left][0][1]<scpd:
            allinone[left][0][1]=scpd
        allinone[left][1][0].append(x)
        allinone[right][1][1].append(x)



    
re=[]

now = datetime.datetime.now()
print ("Time calc glue and omegas : ")
print (now.strftime("%Y-%m-%d %H:%M:%S"))

###END CALCULATION OMEGA / GLUE###

###CALCULATE RELEVANTE EXPRESSIONS### 

count=0
for x in allinone:
    if countgrams(x)==2:
        if allinone[x][0][2]>allinone[x][0][1] and allinone[x][0][0]>1 and len(allinone[x][1][0])>1 and len(allinone[x][1][1])>1:
            re.append(x)

    else:
        if countgrams(x)==7:
            break
        left=getleft(x)
        right=getright(x)
        maxi=max(allinone[left][0][2],allinone[right][0][2])
        rel=(maxi+allinone[x][0][1])/2
        if allinone[x][0][2]>rel and allinone[x][0][0]>1 and len(allinone[x][1][0])>1 and len(allinone[x][1][1])>1:
            re.append(x)



print('done')
      
re=list(re)
index=[]

now = datetime.datetime.now()
print ("Time is relevant or not : ")
print (now.strftime("%Y-%m-%d %H:%M:%S"))


    
################ UNIGRAM SECTION ############################    
    

now = datetime.datetime.now()
print ("Current date and time : ")
print (now.strftime("%Y-%m-%d %H:%M:%S"))




DIR = 'corpus1/'
path, dirs, files = next(os.walk(DIR))
file_count = len(files)
lenames=len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
names=[name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]
i=0
docs={}
total=''
while i<lenames:
    doc=''
    with open(DIR+names[i],encoding="utf8") as file:
        line = file.read().rstrip('\n').lower()
        data=line
        doc=doc+line
        total=total+data
    docs[i]=doc+' '
    i=i+1
data=total

###

i=0
text=''

a=''

def getNrandomRelevant(gram,n):
     if len(gram)>=n:
        return random.sample(gram, n)
     else:
        print('Not enough relevant expressions in list')

### FORMATTING ###

for j in range(lenames):
    data=docs[j]
    numspace=0
    justspaced=False
    size=len(data)
    text=''
    for i in range(size):
        if data[i]=='\n':
            if len(text)>0:
                if text[-1]!=' ':
                    text=text+" "
                    justspaced=True
                continue
            else:
                text=''
        else:
            if i<size-1:    
                if data[i]== ' ' and data[i+1]==' ':
                    continue
            
            if data[i] in chars:
                if data[i-1]!=' ' and not justspaced:
                    text=text+" "
                    justspaced=True
                if i<size-1:
                        if data[i+1]!=' ':
                            text=text+data[i]
                            text=text+" "
                            justspaced=True
                            continue
            justspaced=False
            text=text+data[i]
        
    
    
    size=len(text)
    update=''
    for i in range(size-1):
        if text[i]==' ' and text[i+1]==' ':
            continue
        update=update+text[i]
    text=update
    docs[j]=text
now = datetime.datetime.now()
print ("Time of formatting : ")
print (now.strftime("%Y-%m-%d %H:%M:%S"))
### END FORMATTING ###

### Count Frequency ###

dummy={}
dictdocs={}
numOfDocsPerWord={}
freqOfWord={}
diff={}


for i in range(lenames):
    wordsdoc=docs[i].split(' ')
    dictdocs[i]={}
    onegram2={} #new onegram dictionary
    prev=''
    for x in wordsdoc:
        if x not in onegram2: 
            onegram2[x]=1
            if x not in numOfDocsPerWord:
                numOfDocsPerWord[x]=1
                freqOfWord[x]=1
            else:
                numOfDocsPerWord[x]=numOfDocsPerWord[x]+1
                freqOfWord[x]=freqOfWord[x]+1
        else:
            onegram2[x]=onegram2[x]+1
            freqOfWord[x]=freqOfWord[x]+1
        
    dictdocs[i]=onegram2

def tfidf(t,ind):
    if t not in dictdocs[ind]:
        return 0
    else:
        tf=dictdocs[ind][t]
        aux=np.log(lenames/numOfDocsPerWord[t])
        final=tf*aux
        return final
    


###Context###

neighbours={}
n=1
for i in range(lenames):
    aux=docs[i].split(' ')
    sizedoc=len(aux)
    for ind, x in enumerate(aux):
        if x in chars:
            continue
        if x not in neighbours:
            neighbours[x]=[]
        if ind>0 and ind<sizedoc-1:
            if (aux[ind+1] not in neighbours[x]):
                neighbours[x].append(aux[ind+1])
            if (aux[ind-1] not in neighbours[x]) and (aux[ind-1] not in chars):
                neighbours[x].append(aux[ind-1])

neighfinal={}
for x in neighbours:
    if len(neighbours[x])==0:
        continue
    aux1=list(x)
    check=False
    for i in aux1:
        if chars in aux1:
            check=True
            break
    if check:
        continue
    neighfinal[x]=len(neighbours[x])
    
neighorder={k: v for k, v in sorted(neighfinal.items(), key=lambda item: item[1],reverse=False)}

neighval=list(neighorder.values())

plt.plot(neighval)
plt.ylabel('Valores de contexto')
plt.show()


### FITTING THE MODEL ###

x = np.arange(0, len(neighval), 1)
xp = np.linspace(0, 20, 100)
poli= np.polyfit(x, neighval,9)
p = np.poly1d(poli)
p_1d=p.deriv()
new_vals=[]
for i in range(len(x)):
    calc=p_1d(i+1)
    new_vals.append(calc)
    
'''plt.plot(new_vals)
plt.ylabel('1derivada')
plt.show()'''

#################################################

#### NOT FITTING THE MODEL ###

salto=2
res=0
diffY=[]
for i in range(0,len(neighval)-1,salto):
    if i+salto<len(neighval)-1:
        res=(neighval[i+salto]-neighval[i])/salto
        diffY.append(res)



res=0
gradlist=[]
for j in range(0,len(diffY)-1,1):
    if diffY[j-1]>0:
        res=abs(diffY[j]/diffY[j-1])
        gradlist.append(res)
    else:
        gradlist.append(-1)
    
index_context=(gradlist.index(max(gradlist))+1)*salto

a=list(neighorder)[0:index_context]

def getFirstWord(gram):
    b=str.split(gram)
    return b[0]

def getLastWord(gram):
    b=str.split(gram)
    return b[-1]

def isExtremity(expressions, words):
    res=[]
    off=[]
    for exp in expressions:
        first=getFirstWord(exp)
        last=getLastWord(exp)
        if (first in words) and (last in words):
            res.append(exp)
        else:
            off.append(exp)
    return res,off
    
def getAllEdgesOfRE(re)  :
    res=[]
    for x in re:
        first=getFirstWord(x)
        last=getLastWord(x)
        res.append(first)
        res.append(last)
    return res
  
######################################################  
 
b=list(neighorder)[index_context:]
refinal=[]
#BACKSLASH
backslash="\\"
for x in re:
    first=getFirstWord(x)
    last=getLastWord(x)
    if (first not in b) and (last not in b) and (first not in chars) and (last not in chars) and backslash not in r"%r" % x and (not last.isnumeric()) and (not first.isnumeric()) :
        refinal.append(x)   
    
rescore={}

for x in refinal:
    first=getFirstWord(x)
    last=getLastWord(x)
    
    
    


totlen=len(names)


expsorted={k: v for k, v in sorted(rescore.items(), key=lambda item: item[1],reverse=False)}

vals=list(expsorted.values())
plt.plot(vals)

final=[]
for x in refinal:
    found=0
    for char in chars:
        if char in x:
            found=1
    if found==0:
        final.append(x)

def checkrecall(lista):
    numwords=len(lista)
    notpresent=0
    for wrd in lista:
        word=wrd.lower()
        if word not in final:
            notpresent=notpresent + 1
            print(word + '---> ' + str(allinone[word][0][0]))
    return 1-(notpresent/numwords)

def f_beta(beta,precision, recall):
    aux=(1+beta**2)
    aux2=(precision*recall)
    aux3=(precision*(beta**2))+recall
    if aux3 > 0:
        res=aux*(aux2/aux3)
        return res
    else:
        return 'ERROR'


score={}
neighfinalwithoutnumb={}
allREEdges=getAllEdgesOfRE(final)
for x in neighfinal:
    check=0
    for letter in x:
        if letter.isnumeric():
            check=1
            break
    if check==0 and x in allREEdges:
        neighfinalwithoutnumb[x]=neighfinal[x]
    
        
for x in neighfinalwithoutnumb:
    neighbs=neighfinalwithoutnumb[x]
    freq=onegram[x][0]
    comp=len(x)
    score[x]=neighbs/(comp)

scoreorder={k: v for k, v in sorted(score.items(), key=lambda item: item[1],reverse=False)}

scoreval=list(scoreorder.values())

plt.plot(scoreval)
plt.ylabel('Valores de contexto')
plt.show()

salto=2
res=0
diffY=[]
for i in range(0,len(scoreval)-1,salto):
    if i+salto<len(scoreval)-1:
        res=(scoreval[i+salto]-scoreval[i])/salto
        diffY.append(res)



res=0
gradlist=[]
for j in range(0,len(diffY)-1,1):
    if diffY[j-1]>0:
        res=abs(diffY[j]/diffY[j-1])
        gradlist.append(res)
    else:
        gradlist.append(-1)
    
index_context=(gradlist.index(max(gradlist))+1)*salto

a_onegrams=list(scoreorder)[0:index_context]
b_onegrams=list(scoreorder)[index_context:]
