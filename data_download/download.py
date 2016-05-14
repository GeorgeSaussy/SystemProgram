# download.py
# George Saussy
# version 0.0
import os,sys
'''
    Function to download an index from Project Gutenberg
    @param authorname author's name
    @param dllink base url
    @param numpages number of web pages to index
'''
def indexWriter(authorname,dllink,numpages):
    for k in range(1,numpages):
		os.system('lynx -dump '+dllink+str(k)+' >> '+authorname+'_index')
'''
    Function to download all of the pages containing an author's texts
    @param authorname the author's name
    @param key idetifier that guarontees a line has a relevent link in it
'''
def dleverything(authorname,key):
    file1=open(authorname+'_index','r')
    lines=[]
    for line in file1:
    	lines.append(line)
    file1.close()
    links=[]
    for k in range(0,len(lines)-1):
    	if 'http://gutenberg.spiegel.de/autor/georg-wilhelm-friedrich-hegel-253' in lines[k+1]:
    		links.append(lines[k].split()[len(lines[k].split())-1])
    for link in links:
    	os.system('lynx -dump '+link+' >> '+authorname+'_work')
'''
    Function to parse the author texts from the *_work files
    @param authorname the author's name
'''
def cleanMessy(authorname):
    file1=open(authorname+'_work','r')
    file2=open(authorname+'corpus','w')
    file3=open(authorname+'corpus2','w')
    alllines=[]
    for line in file1:
    	alllines.append(line)
    file1.close()
    final=[]
    for k in range(0,len(alllines)):
    	if 'SPIEGEL-ONLINE-Partnern' in alllines[k]:
    		temptext=[]
    		k1=k-4
    		while not ('[' in alllines[k1] and len(alllines[k1])<50):
    			temptext.append(alllines[k1])
    			k1=k1-1
    		temptext1=''
    		for k1 in range(0,len(temptext)):
    			temptext1=temptext1+temptext[len(temptext)-k1-1]
    		final.append(temptext1)
    		file3.write('#newtext')
    		file3.write(temptext1)
            file2.write(temptext1)
    file1.close()
    file2.close()
    file3.close()



indexWriter('hegel','http://gutenberg.spiegel.de/suche?q=Georg+Wilhelm+Friedrich+Hegel&page=',18)
indexWriter('holderlin','http://gutenberg.spiegel.de/suche?q=Friedrich+H%F6lderlin&page=',20)
indexWriter('schelling','http://gutenberg.spiegel.de/suche?q=Friedrich+Wilhelm+Joseph+Schelling&page=',5)

dleverything('hegel','http://gutenberg.spiegel.de/autor/georg-wilhelm-friedrich-hegel-253')
dleverything('holderlin','http://gutenberg.spiegel.de/buch/friedrich-h-')
dleverything('schelling','http://gutenberg.spiegel.de/autor/friedrich-wilhelm-joseph-von-schelling-514')

cleanMessy('hegel')
cleanMessy('holderlin')
cleanMessy('schelling')
