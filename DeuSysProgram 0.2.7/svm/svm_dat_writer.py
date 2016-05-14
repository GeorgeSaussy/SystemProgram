# naivebayes.py
# George Saussy
import sys,re,math

print "reading authors' corpera..."
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
    toret=[]
    for line in file1:
        temparr=line[0:-1].split("/")
        for word in temparr:
            if word.lower() not in toret:
                toret.append(word.lower())
    file1.close()
    return toret
'''
    Function to compute frequency of of functional words occuring in texts of a given author
    @param author array of the author's texts
    @param vocab array of the dictionary of functional words
    @return array of hashes containing the frequencies
'''
def buildHashes(author,vocab):
    allauthor=[]
    for text in author:
        authorcounts={}
        for elm in funcwords:
            authorcounts[elm]=0.0
        for line in text:
            temp=re.findall(r"[\w']+",line)
            for elm in temp:
                elm1=elm.lower()
                if elm1 in funcwords:
                    authorcounts[elm1]=authorcounts[elm1]+1.0
        #print authorcounts
        total=0
        for elm in authorcounts:
            total=total+authorcounts[elm]
        if not total==0:
            for key in authorcounts:
                authorcounts[key]=authorcounts[key]/total
            allauthor.append(authorcounts)
    return allauthor


# Frist read all the files
hegelcorpus=open('hegelcorpus2','r') # [file] containing Hegel's texts
hegel=parseCorpus(hegelcorpus) # [array] containing Hegel's texts
hegelcorpus.close()
holderlincorpus=open('holderlincorpus2','r') # [file] containing Holderlin's texts
holderlin=parseCorpus(holderlincorpus) # [array] containing Holderlin's texts
holderlincorpus.close()
schellingcorpus=open('schellingcorpus2','r') # [file] containing Schelling's texts
schelling=parseCorpus(schellingcorpus) # [array] containing Schelling's texts
schellingcorpus.close()

# Second read all the German functional words from the file
print "reading functional words..."
funcwords=getDictionary() # [array] holds the German functional words

# Third compute the data vectors for each author
print "computing vectors..."
hegeldata=buildHashes(hegel,funcwords) # [array] holds the vectors to be inputed into the SVM for Hegel
holderlindata=buildHashes(holderlin,funcwords) # [array] holds the vectors to be inputed into the SVM for Holderlin
schellingdata=buildHashes(schelling,funcwords) # [array] holds the vectors to be inputed into the SVM for Schelling

# Fourth write the data vectors to  files in the proper format
print "writing data to files..."
training=open('training_svm_data','w')
testing=open('testing_svm_data','w')
alldat=open('all_svm_data','w')
ind=0
for text in hegeldata:
    ind=ind+1
    tempstr='1 '
    index=1
    for key1 in funcwords:
        tempstr=tempstr+' '+str(index)+':'+str(text[key1])
        index=index+1
    tempstr=tempstr+'\n'
    if not ind%10==0:
        training.write(tempstr)
    else:
        testing.write(tempstr)
    alldat.write(tempstr)
ind=0
for text in holderlindata:
    ind=ind+1
    tempstr='2 '
    index=1
    for key1 in funcwords:
        tempstr=tempstr+' '+str(index)+':'+str(text[key1])
        index=index+1
    tempstr=tempstr+'\n'
    if not ind%10==0:
        training.write(tempstr)
    else:
        testing.write(tempstr)
    alldat.write(tempstr)
ind=0
for text in schellingdata:
    ind=ind+1
    tempstr='3 '
    index=1
    for key1 in funcwords:
        tempstr=tempstr+' '+str(index)+':'+str(text[key1])
        index=index+1
    tempstr=tempstr+'\n'
    if not ind%10==0:
        training.write(tempstr)
    else:
        testing.write(tempstr)
    alldat.write(tempstr)
print "done."
