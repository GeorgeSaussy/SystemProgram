import sys,random,re
from optparse import OptionParser
parser=OptionParser() # [OptionParser] to be calculated -- reads from terminal if only functional words should be used
parser.add_option("--eta", action="store", type="float", dest="etavalue")
parser.add_option("--itrs",action="store",type="int",dest="numitrs")
(options,args)=parser.parse_args() # [tuple] stores parser calculation for the value of the learning parameter
'''
    Function to parse author's corpa into seperate text
    @param authorfile file containing the authors texts
    @return array of the texts, each as an array of lines
'''
def parseCorpus(authorfile):
    toret=[]
    temparr=[]
    for line in authorfile:
        if '#newtext' in line:
            toret.append(temparr)
            temparr=[]
        else:
            temparr.append(line)
    return toret
'''
    Function to get the functional word dictionary from file
    @return array of all functional words
'''
def getDictionary():
    file1=open('functional_words_de','r')
    funcwords=[]
    for line in file1:
        temparr=line[0:-1].split("/")
        for word in temparr:
            if word.lower() not in funcwords:
                funcwords.append(word.lower())
    file1.close()
    return funcwords
'''
    Fucntion to build the vecots to inputed into the perceptron model
    @param authortext array of the text by the author
    @param vocab array of the German functional words
    @return array of vectors to be moved to the perceptron
'''
def computeVectors(authortexts,vocab):
    toret=[]
    for text in authortexts:
        tempcounts={}
        for elm in vocab:
            tempcounts[elm]=0.0
        for line in text:
            temp=re.findall(r"[\w']+",line)
            for elm in temp:
                elm1=elm.lower()
                if elm1 in vocab:
                    tempcounts[elm1]=tempcounts[elm1]+1.0
        total=0
        for elm in tempcounts:
            total=total+tempcounts[elm]
        if not total==0:
            tempcounts1=[]
            for x in range(0,len(vocab)):
                tempcounts1.append(tempcounts[vocab[x]]/total)
            tempcounts1.append(1.0)
            toret.append(tempcounts1)
    return toret
'''
    Function to train a perceptron
    @param sumdata all data to train on
    @param trainfor int telling which author to train for
    @param lp the learning parameter (eta)
    @return weight the weight vector
'''
def trainPerceptron(sumdata,trainfor,lp):
    n=len(sumdata)
    d=len(sumdata[0])-1
    weights=[0.0 for k in range(0,d)]
    randinds=[k for k in range(0,n)]
    random.shuffle(randinds)
    for j in range(0,options.numitrs):
        random.shuffle(randinds)
        for k in range(0,n):
            digitSum=0
            for k1 in range(0,d):
                digitSum=digitSum+weights[k1]*sumdata[randinds[k]][k1]
            output=0
            if digitSum>0:
                output=1
            else:
                output=-1
            trainlabel=0
            if sumdata[randinds[k]][d]==trainfor:
                trainlabel=1
            else:
                trainlabel=-1
            errorvalue=trainlabel-output
            if not errorvalue==0:
                for k1 in range(0,d):
                    weights[k1]=weights[k1]+eta*errorvalue*sumdata[randinds[k]][k1]
    return weights

# First load and pre-process data
print "loading files..."
hegelcorpus=open('hegelcorpus2','r') # [file] containing Hegel's texts
hegeltexts=parseCorpus(hegelcorpus) # [array] containing Hegel's texts
hegelcorpus.close()
holderlincorpus=open('holderlincorpus2','r') # [file] containing Holderlin's texts
holderlintexts=parseCorpus(holderlincorpus) # [array] containing Holderlin's texts
holderlincorpus.close()
schellingcorpus=open('schellingcorpus2','r') # [file] containing Schelling's texts
schellingtexts=parseCorpus(schellingcorpus) # [array] containing Schelling's texts
schellingcorpus.close()
dictionary=getDictionary() # [array] holds the German funtional words
hegeldata=computeVectors(hegeltexts,dictionary) # [array] holds the vectors to be inputed into the perceptron for Hegel
holderlindata=computeVectors(holderlintexts,dictionary) # [array] holds the vectors to be inputed into the perceptron for Holderlin
schellingdata=computeVectors(schellingtexts,dictionary) # [array] holds the vectors to be inputed into the perceptron for Schelling
alldata=[]
# as convention Hegel is author 1, Holderlin is 2, and Schelling is 3
for line in hegeldata:
    temp=line
    temp.append(1)
    alldata.append(temp)
for line in holderlindata:
    temp=line
    temp.append(2)
    alldata.append(temp)
for line in schellingdata:
    temp=line
    temp.append(3)
    alldata.append(temp)

# Second train the perceptrons
print "training perceptrons..."
eta=options.etavalue # [float] learning parameter
hegelweights=trainPerceptron(alldata,1,eta) # [array] containg the weights of a Hegel trained perceptron
holderlinweights=trainPerceptron(alldata,2,eta) # [array] containg the weights of a Holderlin trained perceptron
schellingweights=trainPerceptron(alldata,3,eta) # [array] containg the weights of a Schelling trained perceptron

# Third classify the First System Program of German Idealism
sysprog=open('systemprogram','r')
sysprogvec=[]
tempcounts={}
for elm in dictionary:
    tempcounts[elm]=0.0
for line in sysprog:
    temp=re.findall(r"[\w']+",line)
    for elm in temp:
        elm1=elm.lower()
        if elm1 in dictionary:
            tempcounts[elm1]=tempcounts[elm1]+1.0
total=0
for elm in tempcounts:
    total=total+tempcounts[elm]
for x in range(0,len(dictionary)):
    sysprogvec.append(tempcounts[dictionary[x]]/total)
sysprogvec.append(1.0)
hegelprob=0.0
for k in range(0,len(hegelweights)):
    hegelprob=hegelprob+hegelweights[k]*sysprogvec[k]
holderlinprob=0.0
for k in range(0,len(holderlinweights)):
    holderlinprob=holderlinprob+holderlinweights[k]*sysprogvec[k]
schellingprob=0.0
for k in range(0,len(schellingweights)):
    schellingprob=schellingprob+schellingweights[k]*sysprogvec[k]
print "Making prediction..."
print "Hegel:",hegelprob
print "Holderlin:",holderlinprob
print "Schelling:",schellingprob

# Fourth retrain to print confusion matrix
traindata=[] # [array] holds the new training data
testdata=[] # [array] holds the new testing data
for k in range(0,len(hegeldata)):
    if k%10==0:
        testdata.append(hegeldata[k])
    else:
        traindata.append(hegeldata[k])
for k in range(0,len(holderlindata)):
    if k%10==0:
        testdata.append(holderlindata[k])
    else:
        traindata.append(holderlindata[k])
for k in range(0,len(schellingdata)):
    if k%10==0:
        testdata.append(schellingdata[k])
    else:
        traindata.append(schellingdata[k])
hegelweights=trainPerceptron(traindata,1,eta)
holderlinweights=trainPerceptron(traindata,2,eta)
schellingweights=trainPerceptron(traindata,3,eta)
confusion=[[0,0,0] for k in range(0,3)]
for k in range(0,len(testdata)):
    c1=0.0
    c2=0.0
    c3=0.0
    for k1 in range(0,len(testdata[k])-1):
        c1=c1+hegelweights[k1]*testdata[k][k1]
        c2=c2+holderlinweights[k1]*testdata[k][k1]
        c3=c3+schellingweights[k1]*testdata[k][k1]
    c0=0
    if c1>c2 and c1>c3:
        c0=1
    if c2>c1 and c2>c3:
        c0=2
    if c3>c1 and c3>c2:
        c0=3
    if not c0==0:
        confusion[testdata[k][len(testdata[k])-1]-1][c0-1]=confusion[testdata[k][len(testdata[k])-1]-1][c0-1]+1
print 'confusion matrix:'
print 'hegel\tholderlin\tschelling'
print 'hegel'
print confusion[0][0],confusion[0][1],confusion[0][2]
print 'holderlin'
print confusion[1][0],confusion[1][1],confusion[1][2]
print 'schelling'
print confusion[2][0],confusion[2][1],confusion[2][2]
