import uuid
import random
from datetime import datetime
from searchQuery import SearchQuery

querySearchObj = SearchQuery()

class SearchHandler:
    def flatResults(self, results): 
        """flattened 

        Args:
            results ([type]): [description]
        """
        output = []

        for result in results:
            for section in result['sections']:
                section['_side_note'] = result['_side_note']
                output.append(section)
        
        return output
    
    def __init__(self,query):
        self.query = query
        self.searchId = str(random.randint(0,10000000))#uuid.uuid4()
        self.results = self.flatResults(querySearchObj.makeQueryResult(query))
        self.totalNumOfResults = len(self.results)
        self.nextResultsPointer = 0 
        self.startTime = datetime.now()

    def getRequestId(self):
        """return the object request ID
        """
        return self.searchId

    def getNextResults(self,numOfResults):
        """returns <numOfResults> results in:  

        Args:
            numOfResults (int): number of results to return
        """
        if(self.nextResultsPointer >= self.totalNumOfResults):
            return []

        if(self.nextResultsPointer + numOfResults >= self.totalNumOfResults):
            fromIndex = self.nextResultsPointer
            self.nextResultsPointer=self.totalNumOfResults
            return self.results[fromIndex: self.nextResultsPointer]

        self.nextResultsPointer = self.nextResultsPointer + numOfResults
        return self.results[self.nextResultsPointer - numOfResults : self.nextResultsPointer]


class SearchHandlerPool:
    def __init__(self):
        self.pool = {}

    def addHandler(self,query):
        handler = SearchHandler(query)
        self.pool[handler.getRequestId()] = handler
        return handler.getRequestId()

    def getSugestedSideNote(self, inputStr, numOfResults):
        """

        Args:
            inputStr ([type]): [description]
            numOfResults ([type]): [description]
        """
        return querySearchObj.getSugestedSideNote(inputStr, numOfResults)

    def getNextResults(self,searchId,numOfResults):
        return self.pool[searchId].getNextResults(numOfResults)