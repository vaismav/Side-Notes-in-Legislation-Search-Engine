import uuid
from searchQuery import SearchQuery

searchObj = SearchQuery()

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
        self.searchId = uuid.uuid4()
        self.results = self.flatResults(searchObj.makeQueryResult(query))
        self.totalNumOfResults = len(self.results)
        self.nextResultsPointer = 0 

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