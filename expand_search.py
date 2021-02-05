import sys
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

PATHtoChromeDtiver = "./chromedriver"

driver=webdriver.Chrome(PATHtoChromeDtiver)

dictaURL = "https://tip.dicta.org.il/typeahead"

def getDicta(str):
    driver.get('https://tip.dicta.org.il/')
    element = driver.find_element_by_xpath("//div[@iclassd='react-tags__search-input']/input[1]")
    element.send_keys(str)


def createNGrams(ngrams,N):
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


# gets a string and return array of array of search terms by order
#example input="hi there partner"
#   output = [ 
#               ["hi there partner"],
#               Null,
#               ["hi there", there partner"],
#               ["hi", "there", "partner"],
#               ...
#               ...
#               ... ]
def expandSearch(str):
    ngrams =  str.split()
    print(ngrams)
    print(createNGrams(ngrams,3))
    print(createNGrams(ngrams,2))
    for i in ngrams:
        getDicta(i)

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("ERROR, need an argument to run")
    else: 
        expandSearch(sys.argv[1])