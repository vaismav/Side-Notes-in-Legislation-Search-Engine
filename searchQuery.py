import json
import paths
import side_notes_set_in_list

def throwError(message):
    print("ERROR!" + message)


class SearchQuery:
    def log(self, message):
        print("Log ===> SearchQuery: "+ message)

    def __init__(self):
        self.sideNotesStrings = []
        self.log("Start loading Ngrams JSON")
        with open(paths.notes_ngrams_path) as f:
            self.ngrams  = json.load(f)
            f.close()
        
        self.log("Finished loading Ngrams JSON")

        self.log("Start loading Section JSON")
        with open(paths.all_sections_path) as f:
            self.sections  = json.load(f)
            f.close()
        self.log("Finished loading Section JSON")
        
        self.log("Creating list of side-notes")
        self.side_note_list = self.sections.keys()
        self.log("Finished creating list of side-notes")

        self.queries = {}

    def getSugestedSideNote(self, inputStr, numOfResults):
        """return list of all side-notes which contains the substring inputStr

        Args:
            inputStr ([type]): [description]
        """
        output = []
        resultsFound = 0

        for item in self.side_note_list:
            if inputStr in item:
                output.append(item)
                resultsFound += 1
            if resultsFound >= numOfResults:
                break
        
        return output


    def getAllSideNotes(self):
        """return array of keys in all_sections json

        Returns:
            [type]: [description]
        """
        self.sideNotesStrings = side_notes_set_in_list.side_notes_list

    def createResultObject(self, side_note_string, sections):
        """

        Args:
            side_note_string ([type]): [description]
            sections ([type]): [description]
        """
        output = {}
        output['_side_note'] =  side_note_string
        output['sections']= []
        output['sections'].extend(sections)
        return output


    def makeQueryResult(self,query):
        """gets a query of side-note and add all of its relevent responses 
        to the dictionary in with the same key.
        we store the result in single array by the order of the search depth

        Args:
            query ([type]): [description]
        """
        query_ngrams = self.ngrams.get(query)
        if query_ngrams == None :
            throwError("couldnt find ngrams for \"" + query + "\"")
            return []

        queryOutput = {}
        queryOutput['included_side_notes' ] = []
        queryOutput['results' ] = []

        query_ngrams[0] = [query_ngrams[0]] #temporery patch TODO: fix the ngrams function
        for ngrams_level in query_ngrams:
            if ngrams_level != None:
                for item in ngrams_level :
                    if len(item) >= 2 and not item in queryOutput['included_side_notes']:
                        for side_note_string in self.sections :
                            if item in side_note_string:
                                queryOutput['included_side_notes'].append(side_note_string)
                                # current_side_note_result = {}
                                # current_side_note_result['_side_note'] =  side_note_string
                                # current_side_note_result['sections']= []
                                # current_side_note_result['sections'].extend(self.sections[side_note_string].values())
                                current_side_note_result = self.createResultObject(side_note_string, self.sections[side_note_string].values())
                                queryOutput['results'].append(current_side_note_result)
        
        return queryOutput['results']

    def updateAllQueries(self):
        self.getAllSideNotes()
        # for side_note in self.sideNotesStrings:
        #     print("N0"+str(runNumber) + " Start creating results for: " + side_note)
        #     self.makeQueryResult(side_note)
        #     print("N0"+str(runNumber) + " Finished creating results for: " + side_note)
        #     runNumber+=1
        with open(paths.queries_path, 'w' , encoding="utf-8") as fp:
                json.dump(self.makeQueryResult(self.sideNotesStrings[0]), fp, ensure_ascii=False, indent=4, sort_keys=True)
        



    



if __name__ == "__main__":
    obj = SearchQuery()
    obj.updateAllQueries()
    
    