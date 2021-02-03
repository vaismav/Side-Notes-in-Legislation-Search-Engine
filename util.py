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

def trainModel(dataSetPath):
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


def clearDataSet(inputRelativePath, outputRelativePath, delimiter):
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
    

if __name__ == "__main__":
    # clearDataSet('fasttext/data/all_side_notes_file.txt','fasttext/data/clean_side_notes',"@@@")
    for i in range(1,len(sys.argv)):
        if(sys.argv[i] == "--train"):
            if(len(sys.argv) < i+1):
                print("Error! need relative path for dataSet to train")
                exit()
            trainModel(sys.argv[i+1])
        elif(sys.argv[i] == "--cleanData"):
            if(len(sys.argv) < i+2):
                print("Error! need relative path for inputFile and output file")
                exit()
            clearDataSet(sys.argv[i+1],sys.argv[i+2],"@@@")

            

    # if(len(sys.argv) < 2):
    #     print("ERROR, need an argument to run")
    # else: 
    #     expandSearch(sys.argv[1])
