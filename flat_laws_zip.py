import os
import xml.etree.ElementTree as ET
from shutil import copyfile
import paths

def flat_laws_zip():
    """
    This function flat the zip of laws and creates a put all the law's xmls in a folder called \\data\\xmls
    """
    counter=0
    wrd = "".join(os.getcwd())
    for root,subFolder,files in os.walk(wrd):
        for item in files:
            if(item.endswith("main.xml")):
                dst = wrd + paths.data_xml_law_file + str(counter)+".xml"
                src=str(root)+"/main.xml"
                copyfile(src, dst)
                counter += 1


flat_laws_zip()
