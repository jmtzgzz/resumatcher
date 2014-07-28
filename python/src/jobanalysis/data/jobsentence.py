# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 16:24:09 2014

@author: dlmu__000

"""
from tokenfilter import *

class JSentence():
    puncts = [".", ",", ";","?", "!", ":" ]
    tagDict = { "or": "OR", "and" : "AND" }    
    
    def __init__(self, words):
        self.words = words
        self.lower_words = [word.lower() for word in self.words]
        self.tags = [None] * len(self.words)
        self._firstTag()
        
    def _firstTag(self):         
        
        i = 0       
        while i < len(self.words):
            word = self.words[i]     
            if word in  JSentence.puncts :
                self.tags[i] = (  word , True )                
            elif JSentence.tagDict.has_key(word):
                self.tags[i] = ( JSentence.tagDict[word], True )
            i+=1
    
    
    def findUntaggedRanges( self ):
        ranges = []
        i = 0
        word_len = len(self.words)
        while i  < word_len :
        #    print "i=", i
            if self.tags[i] != None :
                i += 1
            else:
                j  =  i                
                while j < word_len and  self.tags[j] == None:
                    j+=1
             #       print "j=", j
                if  self.tags[j-1] == None :
                    ranges.append( (i , j-i ) )
                    i = j + 1
                if j == word_len :
                    break
                
        return ranges                
         
           
    def labelWithTuple(self, labelTuple):
        toekens , label =  labelTuple  
        has_tagged = True
        while has_tagged:
            has_tagged = False
            # after tag one label, reset ranges
            ranges = self.findUntaggedRanges()
     #       print "ranges=", ranges
            for untagged in ranges:
                i = findTokenSquence(toekens, self.words, scope = untagged )
            # here only find once in one range            
     #           print untagged , i 
                if i != -1 :
                     self.tags[i] = (label, True)
                     j=1 
                     while j < len(toekens) :
                         self.tags[i+j] = (label, False)
                         j += 1        
                     has_tagged = True
                     break
  
def test_sentence1():
    words = "I am ok or not , with you and me .".split()  
    
    sent = JSentence(words)
 #   print sent.tags
    sent.labelWithTuple(( ["or", "not", ",", "with"] , "AAAA" ))
    print sent.tags  
    
def test_sentence2():
    words = "I am ok or not , am ok and am ok . and  am ok".split()  
    
    sent = JSentence(words)
 #   print sent.tags
  #  sent.labelWithTuple(( ["am", "ok"] , "AAAA" ))
  #  sent.labelWithTuple(( ["am" ] , "AAAA" ))
    sent.labelWithTuple(( ["am", "ok" , "and"] , "AAAA" ))
    print sent.tags  
                
                
def main(): 
   test_sentence2()
 #  beforeDegree()
    
if __name__ == "__main__": 
    main() 