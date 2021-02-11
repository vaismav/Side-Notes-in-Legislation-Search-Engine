import sys
import os
import platform
import fasttext

def getPathDevider():
    if(platform.system == "Windows"):
        return '\\'
    else:
        return '/'


pathDivider = getPathDevider()

def printEvent(output):
    print("\n=================================\n"+output+"\n=================================\n")


class FastTextModel:
    def __init__(self):
        self.model = None
        self.modelPath = None
        self.cleanDataSetPath = None


    def trainModel(self, dataSetPath):
        """[summary]

        Args:
            dataSetPath ([type]): [description]
        """
        # cwd= os.getcwd()
        printEvent("Start training model")
        model = fasttext.train_unsupervised(dataSetPath)
        printEvent("finished training model")
        model.save_model("result/model.bin")
        pass


    def clearDataSet(self, inputRelativePath, outputRelativePath, delimiter):
        """clean the dataset from the delimiter 

        Args:
            inputRelativePath ([type]): [description]
            outputRelativePath ([type]): [description]
            delimiter ([type]): [description]
        """
        # cwd= os.getcwd()
        inputFile = open(inputRelativePath,"r")
        print("open input file "+inputRelativePath)
        outputFile = open(outputRelativePath,"w")
        print("open output file "+outputRelativePath)

        inputString = inputFile.read()
        if((delimiter != None) | (delimiter != "")):
            outputString = inputString.replace(delimiter,'').replace('\n',' ').replace('\r',' ')
        else:
            outputString = inputString.replace('\n',' ').replace('\r',' ')

        outputFile.write(outputString)
        pass

    def clearDataSetObject(self, inputString, outputRelativePath, delimiter):
        """clean the dataset from the delimiter 

        Args:
            inputString (string): [description]
            delimiter ([type]): [description]
        """
        # cwd= os.getcwd()
        outputFile = open(outputRelativePath,"w")
        print("open output file "+outputRelativePath)

        if((delimiter != None) & (delimiter != "")):
            outputString = inputString.replace(delimiter,'').replace('\n',' ').replace('\r',' ')
        else:
            outputString = inputString.replace('\n',' ').replace('\r',' ')

        outputFile.write(outputString)
        pass

    def loadModel(self, trainedModelPath):
        """
            return model object of fasttext trained model dataset
        Args:
            trainedModelPath ([type]): [description]
        """
        self.model = fasttext.load_model(trainedModelPath)
        self.modelPath = trainedModelPath


    def getWordsOf(self, word, numOfReturnedItems):
        """
            return the nearest nehibore of 'word' in the fasttext model
        Args:
            word (string): the input string
            numOfReturnedItems (int): number of item to return from the head of the list
        """
        if(self.model == None):
            print("unTrained model error")
            exit()

        words = self.model.get_nearest_neighbors(word)
        output = []
        for index in range(0, min(numOfReturnedItems, len(words))):
            output.append(words[index][1])
        # print(output)
        return output

    


if __name__ == "__main__":
    model=FastTextModel()
    # clearDataSet('fasttext/data/all_side_notes_file.txt','fasttext/data/clean_side_notes',"@@@")
    argc = len(sys.argv)
    for i in range(1,argc): 
        if(sys.argv[i] == "--train"):
            if(argc < i+1):
                print("Error! need relative path for dataSet to train")
                exit()
            model.trainModel(sys.argv[i+1])
        elif(sys.argv[i] == "--cleanData"):
            if(argc < i+2):
                print("Error! need relative path for inputFile and output file")
                exit()
            model.clearDataSet(sys.argv[i+1],sys.argv[i+2],"@@@")
        elif (sys.argv[i] == "--testWord"):
            if(argc < i+1):
                print("Error! need string value after --testWord")
                exit()
            n=5
            if((argc >= i+3) &  (sys.argv[i+2] == "-n")):
                n = int(sys.argv[i+3])
            model.loadModel("result/model.bin")
            model.getWordsOf(sys.argv[i+1],n)

            

    # if(len(sys.argv) < 2):
    #     print("ERROR, need an argument to run")
    # else: 
    #     expandSearch(sys.argv[1])
