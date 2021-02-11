import os
import xml.etree.ElementTree as ET
from shutil import copyfile
import zipfile
import paths


def extractResultJsons():
    print("start extracting JSON DB")
    with zipfile.ZipFile(paths.results_zip, 'r') as zip_ref:
        zip_ref.extractall(paths.resulst_dir)
    
    print("Finished extracting JSON DB")

def extractLawsXML():
    print("start extracting JSON DB")
    with zipfile.ZipFile(paths.data_LawRepoWikiZIP, 'r') as zip_ref:
        zip_ref.extractall(paths.dataDIR)
    
    print("Finished extracting JSON DB")

def flat_laws_zip():
    """
    This function flat the zip of laws and creates a put all the law's xmls in a folder called \\data\\xmls
    """
    counter=0
    wrd = "".join(os.getcwd())
    try:
        os.mkdir(paths._data_xmls)
    except OSError:
        pass
    
    for root,subFolder,files in os.walk(wrd+paths._data):
        for item in files:
            if(item.endswith("main.xml")):
                dst=wrd+paths._data_xml_law_file+ str(counter)+".xml"
                # dst = wrd + paths.data_xml_law_file + str(counter)+".xml"
                src=str(root)+paths._mainXML
                copyfile(src, dst)
                counter += 1



if __name__ == "__main__":
    extractLawsXML()
    flat_laws_zip()
    

