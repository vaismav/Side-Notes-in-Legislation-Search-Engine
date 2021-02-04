import sys
import json
from side_notes_set_in_list import side_notes_list 

from util import FastTextModel 
from util import printEvent 



class SideNotesNgrams:

    def __init__(self):
        self.dictionary = {}
        self.fastTextModel = FastTextModel()
        self.numOfAlternativesWords = 5
        self.fastTextModel.loadModel("result/model.bin")

    
    def createNGrams(self, ngrams,N):
        """gets array of strings and return array of N-grams strings
        if there are N or less strings return None
        Args:
            ngrams (Arrat of string): [description]
        """
        if( len(ngrams) < N+1 ):
            return None

        output = []

        for index in range(0, len(ngrams) - N + 1  ):
            # print(list(range(index,index + N)))
            output.append(" ".join([ngrams[i] for i in list(range(index,index + N))]))
        return output

    
    def getAlternativWords(self, twoWordsString):
        """return array with alternativ apperance for the 2 words combination

        Args:
            twoWordsString ([type]): [description]
        """
        output = []
        firstWord = twoWordsString.split()[0]
        secondWord = twoWordsString.split()[1]

        firstWord_Alternatives = self.fastTextModel.getWordsOf(firstWord, self.numOfAlternativesWords)
        secondWord_Alternatives = self.fastTextModel.getWordsOf(secondWord,self.numOfAlternativesWords)
        
        for word1 in firstWord_Alternatives:
            for word2 in secondWord_Alternatives:
                output.append(word1+" "+word2)
        
        return output

    def makeAlternativeApprance(self, termsArray):
        """

        Args:
            termsArray ([type]): [description]

        Returns:
            [type]: [description]
        """
        if( len(termsArray[0].split()) != 2):
            print("error! expect array of strings contains 2 words")
            return None

        output = []
        for term in termsArray:
            output.extend(self.getAlternativWords(term))
        
        return output
    
    
    def expandSearchTerm(self, searchTerm):
        """# gets a string and return array of array of search terms by order
            #example input="hi there partner"
            #   output = [ 
            #               ["hi there partner"],
            #               Null,
            #               ["hi there", there partner"],
            #               ["hi", "there", "partner"],
            #               ...
            #               ...
            #               ... ]
        Args:
            searchTerm ([type]): [description]
        """
        if(self.dictionary.get(searchTerm) != None):
            return 
        ngrams =  searchTerm.split()

        newSearchTerms = []
        newSearchTerms.append(searchTerm)
        newSearchTerms.append(self.createNGrams(ngrams,3))
        twoWords = self.createNGrams(ngrams,2)
        newSearchTerms.append(twoWords)
        if twoWords != None :
            newSearchTerms.append(self.makeAlternativeApprance(twoWords))
        else:
            newSearchTerms.append(None)
        newSearchTerms.append(ngrams)
        self.dictionary[searchTerm] = newSearchTerms
    

if __name__ == "__main__":
    obj = SideNotesNgrams()
    if(len(sys.argv) < 2):
        print("ERROR, need an argument to run")
    else: 
        # print(side_notes_list[int(sys.argv[1])])
        if(sys.argv[1] == "-a"):
            printEvent("Creating dictionary")
            index = 0
            for note in side_notes_list:
                print("Working on term N0"+ str(index))
                obj.expandSearchTerm(note)
                print("Finished term N0"+str(index))
                index+=1
                if(index >500):
                    break

            printEvent("Finished Creating dictionary")
            printEvent("Creating JSON")

            with open('data.json', 'w') as fp:
                json.dump(obj.dictionary, fp)

            printEvent("Finished Creating JSON")
        else:
            obj.expandSearchTerm(side_notes_list[int(sys.argv[1])])