# naivebayesclassifier.py
# George Saussy
# version 0.0
# reads in classifier data and applies it
import sys,re,math
'''
    Function to get the vocabulary from the model file
    @param modelFile file containing the model
    @return array of the vocabulary
'''
def getVocab(modelFile):
    toret=[]
    for x in modelFile:
        temp=x.split()
        toret.append(temp[0])
    return toret
'''
    Function to read the model data from a file
    @param modelFile file containing the data
    @return hegel [hash] the hegel model
    @return holderlin [hash] the hegel model
    @return schelling [hash] the hegel model
    @return vocab [array] the ocabulary used by the models
'''
def readLogFreqModel(modelFile):
    hegel={}
    holderlin={}
    schelling={}
    vocab=[]
    onhegel=True
    onholderlin=False
    onschelling=False
    for line in modelFile:
        if '#hegel' in line:
            onhegel=True
            onholderlin=False
            onschelling=False
        if '#holderlin' in line:
            onhegel=False
            onholderlin=True
            onschelling=False
        if '#schelling' in line:
            onhegel=False
            onholderlin=False
            onschelling=True
        temp=line.split()
        if len(temp)>1:
            if onhegel:
                hegel[temp[0]]=float(temp[1])
            if onholderlin:
                holderlin[temp[0]]=float(temp[1])
            if onschelling:
                schelling[temp[0]]=float(temp[1])
            vocab.append(temp[0])
    return (hegel,holderlin,schelling,vocab)
'''
    Function to read lines from file
    @param fileVar a file object to be read
    @return array containing the lines in the file
'''
def getLinesFromFile(fileVar):
    toret=[]
    for x in fileVar:
        toret.append(x)
    return toret
'''
    Function to read the lines from a formatted corpus for testing
    @param corpusFile a file containing
    @return array containg seperated texts
'''
def seperateTexts(rawauthorcorpus):
    toret=[]
    for k in range(1,len(rawauthorcorpus)):
        if '#newtext' in rawauthorcorpus[k]:
            k1=k-1
            temp=[]
            while not '#newtext' in rawauthorcorpus[k1]:
                temp.append(rawauthorcorpus[k1])
                k1=k1-1
            temptext=''
            for k2 in range(0,len(temp)):
                temptext=temptext+temp[len(temp)-k2-1]
            toret.append(temptext)
    return toret
'''
    Function to seperate texts into training and test sets
    @param authortexts the seperated author texts
    @return testauthor the test set
    @return trainauthor the training set
'''
def buildTest(authortexts):
    testauthor=[]
    trainauthor=[]
    for k in range(0,len(authortexts)):
        if k%10==0:
            testauthor.append(authortexts[k])
        else:
            trainauthor.append(authortexts[k])
    return (testauthor,trainauthor)
'''
    Function to retrain the model given the test set
    @param trainauthor array of text to train on
    @param vocab array of words to train for
    @return hash of the model containing log-likelihood of an author using a word
'''
def resetModel(trainauthor,vocab):
    toret={}
    for x in vocab:
        toret[x]=1.0
    for text in trainauthor:
        temp=re.findall(r"[\w']+",text)
        for elm in temp:
            if elm.lower() in vocab:
                toret[elm.lower()]=toret[elm.lower()]+1.0
    authortotal=0.0
    for x in toret:
        authortotal=authortotal+toret[x]
    for x in toret:
        toret[x]=math.log(toret[x]/authortotal,2)
    return toret
logfreq=open('logfreq_data','r') # [file] outputted from naivebayes_logwriter.py
#dictionary=getVocab(logfreq)
(hegelmodel,holderlinmodel,schellingmodel,dictionary)=readLogFreqModel(logfreq) # [hash] hegelmodel contains Hegel's log frequency word use
                                                           # [hash] holderlinlmodel contains Holderlin's log frequency word use
                                                           # [hash] schellingmodel contains Schelling's log frequency word use
                                                           # [array] dictionary contains the vocabulary
logfreq.close()
systemprogram=open('systemprogram','r') # [file] holds the contents of the The First System Program of German Idealism
testwords=[] # [array] to be calculated -- hold the words to be tested by the models
for line in systemprogram:
    temp=re.findall(r"[\w']+",line)
    for elm in temp:
        testwords.append(elm.lower())
hegelsum=0.0 # [double] to be calculated -- the log-likelihood of Hegel having wrote the System Program
holderlinsum=0.0 # [double] to be calculated -- the log-likelihood of Holderlin having wrote the System Program
schellingsum=0.0 # [double] to be calculated -- the log-likelihood of Schelling having wrote the System Program
for word in testwords:
    if word in hegelmodel:
        hegelsum=hegelsum+hegelmodel[word]
    if word in holderlinmodel:
        holderlinsum=holderlinsum+holderlinmodel[word]
    if word in schellingmodel:
        schellingsum=schellingsum+schellingmodel[word]
print 'log - likelihood, hegel\t',hegelsum
print 'log - likelihood, holderlin\t',holderlinsum
print 'log - likelihood, schelling\t',schellingsum
# the following calculations print the confusions matrix of the model in logfreq_data
hegelcorpusfile=open('hegelcorpus2','r') # [file] contains all Hegel's text for testing
rawhegelcorpus=getLinesFromFile(hegelcorpusfile) # [array] holds the unprocessed lines from the Hegel corpus
hegelcorpusfile.close()
hegeltexts=seperateTexts(rawhegelcorpus) # [array] containes the seperated texts by Hegel
holderlincorpusfile=open('holderlincorpus2','r') # [file] contains all Holderlin's text for testing
rawholderlincorpus=getLinesFromFile(holderlincorpusfile) # [array] holds the unprocessed lines from the holderlin corpus
holderlincorpusfile.close()
holderlintexts=seperateTexts(rawholderlincorpus) # [array] containes the seperated texts by Holderlin
schellingcorpusfile=open('schellingcorpus2','r') # [file] contains all Schelling's text for testing
rawschellingcorpus=getLinesFromFile(schellingcorpusfile) # [array] holds the unprocessed lines from the schelling corpus
schellingcorpusfile.close()
schellingtexts=seperateTexts(rawschellingcorpus) # [array] containes the seperated texts by Schelling
print 'retraining for test...'
(testhegel,trainhegel)=buildTest(hegeltexts) # [array] testhegel the Hegel texts to test
                                             # [array]  trainhegel the Hegel texts to train on
(testholderlin,trainholderlin)=buildTest(holderlintexts) # [array] testholderlin the Holderlin texts to test
                                                         # [array] trainholderlin the Holderlin texts to train on
(testschelling,trainschelling)=buildTest(schellingtexts) # [array] testschelling the Schelling texts to test
                                                         # [array] trainschelling the Schelling texts to train on


# first we reset the models
hegelmodel=resetModel(trainhegel,dictionary)
holderlinmodel=resetModel(trainholderlin,dictionary)
schellingmodel=resetModel(trainschelling,dictionary)
print 'confusion matrix:'
print 'hegel\tholderlin\tschelling'
c11=0
c21=0
c31=0
print 'hegel'
for text in testhegel:
    temp1=re.findall(r"[\w']+",text)
    d1=0
    d2=0
    d3=0
    for elm in temp1:
        elm1=elm.lower()
        if elm1 in hegelmodel:
            d1=d1+hegelmodel[elm1]
        if elm1 in holderlinmodel:
            d2=d2+holderlinmodel[elm1]
        if elm1 in schellingmodel:
            d3=d3+schellingmodel[elm1]
    if d1>d2 and d1>d3:
        c11=c11+1
    if d2>d1 and d2>d3:
        c21=c21+1
    if d3>d1 and d3>d2:
        c31=c31+1
print c11,'\t',c21,'\t',c31
c12=0
c22=0
c32=0
print 'holderlin'
for text in testholderlin:
    temp1=re.findall(r"[\w']+",text)
    d1=0
    d2=0
    d3=0
    for elm in temp1:
        elm1=elm.lower()
        if elm1 in hegelmodel:
            d1=d1+hegelmodel[elm1]
        if elm1 in holderlinmodel:
            d2=d2+holderlinmodel[elm1]
        if elm1 in schellingmodel:
            d3=d3+schellingmodel[elm1]
    if d1>d2 and d1>d3:
        c12=c12+1
    if d2>d1 and d2>d3:
        c22=c22+1
    if d3>d1 and d3>d2:
        c32=c32+1
print c12,'\t',c22,'\t',c32
c13=0
c23=0
c33=0
print 'schelling'
for text in testschelling:
    temp1=re.findall(r"[\w']+",text)
    d1=0
    d2=0
    d3=0
    for elm in temp1:
        elm1=elm.lower()
        if elm1 in hegelmodel:
            d1=d1+hegelmodel[elm1]
        if elm1 in holderlinmodel:
            d2=d2+holderlinmodel[elm1]
        if elm1 in schellingmodel:
            d3=d3+schellingmodel[elm1]
    if d1>d2 and d1>d3:
        c13=c13+1
    if d2>d1 and d2>d3:
        c23=c23+1
    if d3>d1 and d3>d2:
        c33=c33+1
print c13,'\t',c23,'\t',c33
