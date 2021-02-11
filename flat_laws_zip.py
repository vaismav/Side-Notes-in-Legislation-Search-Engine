<<<<<<< HEAD
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
    
    for root,subFolder,files in os.walk(wrd+getPathOfOS("\\data")):
        for item in files:
            if(item.endswith("main.xml")):
                dst=wrd+getPathOfOS("\\data\\xmls\\law")+ str(counter)+".xml"
                # dst = wrd + paths.data_xml_law_file + str(counter)+".xml"
                src=str(root)+getPathOfOS("\\main.xml")
                copyfile(src, dst)
                counter += 1


flat_laws_zip()
=======
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
    
    for root,subFolder,files in os.walk(wrd+getPathOfOS("\\data")):
        for item in files:
            if(item.endswith("main.xml")):
                dst=wrd+getPathOfOS("\\data\\xmls\\law")+ str(counter)+".xml"
                # dst = wrd + paths.data_xml_law_file + str(counter)+".xml"
                src=str(root)+getPathOfOS("\\main.xml")
                copyfile(src, dst)
                counter += 1


flat_laws_zip()
>>>>>>> 8f16a66e5d1238f3289d1df17de957c751fdaedb
