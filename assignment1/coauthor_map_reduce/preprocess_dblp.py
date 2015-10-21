#!/usr/bin/python

import xml.sax
import codecs
import time
import itertools

#init
start_time = time.time()
processedDblp = codecs.open("processedDblp.txt", "w", "utf_8")

#get from dblp.dtd
def isResearchTag(tag):
    if tag=="article" or tag=="inproceedings" or tag=="proceedings" or tag=="book" or tag=="incollection" or tag=="phdthesis" or tag=="mastersthesis" or tag=="www":
        return True
    else:
        return False
    
class AuthorHandler( xml.sax.ContentHandler ):    
    
    #init class variables
    processedResearch=0
    processedAuthor=0
    processedCoauthor=0
    authors = []
        
    def __init__(self):
        self.CurrentData = ""
        self.author = ""        

    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag        
        if isResearchTag(tag):
            #renew authors list
            del AuthorHandler.authors[:]        

    # Call when an elements ends
    def endElement(self, tag):        
        if self.CurrentData == "author":
            #put author name into author list
            AuthorHandler.authors.append("\""+self.author.strip()+"\"")
            AuthorHandler.processedAuthor+=1
            self.author=""
        elif isResearchTag(tag):            
            AuthorHandler.processedResearch+=1            
            if len(AuthorHandler.authors)>0:                
                #generate coauthor combinations
                AuthorHandler.authors.sort()
                combinations=itertools.combinations(AuthorHandler.authors,2)
                #print AuthorHandler.authors to file                                 
                for combination in combinations:
                    AuthorHandler.processedCoauthor+=1
                    processedDblp.write(" ".join(combination)+"\n")                                        
                    
            #log progress
            print "Processed Researchs=",AuthorHandler.processedResearch,"Authors=",AuthorHandler.processedAuthor,"Co-authors=",AuthorHandler.processedCoauthor,"Running Time=",time.time()-start_time,"s"
            
    # Call when a character is read
    def characters(self, content):
        if self.CurrentData == "author":
            self.author += content
  
if ( __name__ == "__main__"):
    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    
    # override the default ContextHandler
    Handler = AuthorHandler()
    parser.setContentHandler( Handler )
    
    parser.parse(codecs.open("dblp.xml","r","utf_8"))
    processedDblp.close()
    