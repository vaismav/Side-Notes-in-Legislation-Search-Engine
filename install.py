import os
import sys
import xml.etree.ElementTree as ET
from shutil import copyfile
import zipfile
import paths
import main_search
from wordsModel import FastTextModel
from ngrams import SideNotesNgrams
import json


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
        os.mkdir(paths.data_xmls)
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
    run_all = False
    build_all_sections = False
    train_model = False
    create_ngrams = False
    errorMsg = """Invalid Argument Input:
 OPTIONS
    -a, --all                     Run the entire installation process
    -d, --builddatabase           Create loacle sections DB
    -t, --trainmodel              Train the fasttext Words Model
    -n, --createngrams            Create the ngrams dataset
    -h, --help                    Print this help

    you can use multiple flags together
"""
    if len(sys.argv) < 2 :
        print(errorMsg)
        exit()
    
    for arg in sys.argv:
        if arg == "-a":
            run_all = True
            break
        elif arg == "-s":
            build_all_sections = True
        elif arg == "-t":
            train_model = True
        elif arg == "-n":
            create_ngrams = True
        else:
            print(errorMsg)
            exit()
    # extractLawsXML()
    # flat_laws_zip()
    # main_search.fill_local_db_to_json()
    # #train word model
    # wordModel = FastTextModel()
    # with open(paths.all_sections_path, 'r',encoding="utf8") as f:
    #     sections_json = json.load(f)
    #     print("log ===> collecting all strings of side notes")
    #     keys_str = ""
    #     keys_str += " ".join(sections_json.keys())
    #     # create clean dataset file
    #     print("log ===> creating clean corpus")
    #     wordModel.clearDataSetObject(keys_str,paths.data_dataset,None)
    #     print("log ===> Start training word model")
    #     wordModel.trainModel(paths.data_dataset)
    #     print("log ===> Finished training word model")

    #     ngramsCreator = SideNotesNgrams()
    #     ngramsCreator.createNoteNgramsJson(sections_json.keys())



