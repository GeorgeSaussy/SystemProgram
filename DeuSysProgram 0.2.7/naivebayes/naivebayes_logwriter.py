# naivebayes.py
# George Saussy
# version 0.0
# naive bayes with +1 smoothing, reporting binary logs
import sys,re,math
from optparse import OptionParser
parser=OptionParser() # [OptionParser] to be calculated -- reads from terminal if only functional words should be used
parser.add_option("-d", action="store", type="string", dest="dictionarysource")
(options,args)=parser.parse_args() # [tuple] stores parser calculation for if only functional words should be used
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
    Function to read the vocabulary from an array of text lines
    @param lineArray array containing the lines to mine
    @param blackList array containing words to ignore
    @return array containing all the allowed word used in lineArray
'''
def getVocabFromLines(lineArray,blackList):
    toret=[]
    for x in lineArray:
        temp=re.findall(r"[\w']+",x)
        for x1 in temp:
            elm=x1.lower()
            if (not elm in toret) and (not elm in blackList):
                toret.append(elm)
    return toret
'''
    Function to model an author
    @param authorlines array containing lines writen by the author
    @param vocab array containg the words to count
    @return toret1 dictionary containing the cumulative frequency of an authors use of words
    @return toret2 total number of word occurances in the authors collected works.
'''
def modelAuthor(authorlines,vocab):
    toret1={}
    for x in vocab:
        toret1[x]=1.0
    for x in authorlines:
        temp=re.findall(r"[\w']+",x)
        for x1 in temp:
            elm=x1.lower()
            if elm in vocab:
                toret1[elm]=toret1[elm]+1.0
    toret2=0.0
    for x in toret1:
        toret2=toret2+toret1[x]
    return (toret1,toret2)
hegelcorpusfile=open('hegelcorpus','r') # [file] reads Hegel's vocabulary
holderlincorpusfile=open('holderlincorpus','r') # [file] reads Holderlin's vocabulary
schellingcorpusfile=open('schellingcorpus','r') # [file] reads Schelling's vocabulary
print "input files open..."
hegellines=getLinesFromFile(hegelcorpusfile) # [array] -- holds the raw lines from the hegel corpus for later processing
hegelcorpusfile.close()
holderlinlines=getLinesFromFile(holderlincorpusfile) # [array] -- holds the raw lines from the holderlin corpus for later processing
holderlincorpusfile.close()
schellinglines=getLinesFromFile(schellingcorpusfile) # [array] -- holds the raw lines from the schelling corpus for later processing
schellingcorpusfile.close()
print "building dictionary..."
dictionary=[] # [array] to be calculated -- holds the all words searched for in processing
hasfailed=False # [bool] to be calculated -- is true only if terminal command not written properly
if options.dictionarysource=="func": # in case only funcitonal words to be used
    file1=open('functional_words_de','r') # [file] holds the functional word lines
    for line in file1:
        temparr=line[0:-1].split("/")
        for word in temparr:
            if word.lower() not in dictionary:
                dictionary.append(word.lower())
    file1.close()
else:
    if options.dictionarysource=="all": # in case all words to be used
        forbiddenwords=['georg','wilhelm','friedrich','hegel','h\xc3lderlin','joseph','schelling'] # [array] words which would bias classifier, names of the suspected authors
        for word in getVocabFromLines(hegellines,forbiddenwords):
            dictionary.append(word)
        for word in getVocabFromLines(holderlinlines,forbiddenwords):
            dictionary.append(word)
        for word in getVocabFromLines(schellinglines,forbiddenwords):
            dictionary.append(word)
    else: # in case terminal command not written propery
        hasfailed=True
if hasfailed: # in case terminal command not written properly, fail
    print "parameter needed -- see README for usage"
else: # in case terminal command written properly, continue
    print "dictionary built"
    print "modeling hegel..."
    (hegelcounts,hegeltotal)=modelAuthor(hegellines,dictionary) # [map<string,float>] hegelcounts stores the cumulative frequency Hegel uses words in dictionary
                                                                # [float] hegeltotal is the number of words Hegel used total
    print "modeling holderlin..."
    (holderlincounts,holderlintotal)=modelAuthor(holderlinlines,dictionary) # [map<string,float>] holderlincounts stores the cumulative frequency Holderlin uses words in dictionary
                                                                            # [float] holderlintotal is the number of words Holderlin used total
    print "modeling schelling..."
    (schellingcounts,schellingtotal)=modelAuthor(schellinglines,dictionary) # [map<string,float>] schellingcounts stores the cumulative frequency Schelling uses words in dictionary
                                                                                # [float] schellingtotal is the number of words Schelling used total
    print "done modeling"
    print "writing model to file..."
    logfreq=open('logfreq_data','w') # [file] contains log-frequency of ech authors use of a word
    logfreq.write("#hegel")
    for key in hegelcounts:
        hegelcounts[key]=math.log(hegelcounts[key]/hegeltotal,2)
        logfreq.write(key+"\t"+str(hegelcounts[key])+"\n")
    logfreq.write("#holderlin")
    for key in holderlincounts:
        holderlincounts[key]=math.log(holderlincounts[key]/holderlintotal,2)
        logfreq.write(key+"\t"+str(holderlincounts[key])+"\n")
    logfreq.write("#schelling")
    for key in schellingcounts:
        schellingcounts[key]=math.log(schellingcounts[key]/schellingtotal,2)
        logfreq.write(key+"\t"+str(schellingcounts[key])+"\n")
    print "done"
