import os
import xml.etree.ElementTree as ET
from shutil import copyfile

def get_all_laws():
    counter=0
    wrd = "".join(os.getcwd())
    laws_dir=wrd+"\\akn"
    for root,subFolder,files in os.walk(wrd):
        for item in files:
            if(item.endswith("main.xml")):
                dst = wrd + "\\xmls\\law" + str(counter)+".xml"
                src=str(root)+"\\main.xml"
                copyfile(src, dst)
                counter += 1


get_all_laws()
