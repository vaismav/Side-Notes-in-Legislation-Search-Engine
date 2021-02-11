import platform

def getPathOfOS(path):
    if(platform.system == "Windows"):
            return path.replace("/","\\")
    return path

_data_xml_law_file   = getPathOfOS("/data/xmls/law")
all_sections_path   = getPathOfOS("result/all_sections.json")
model_path          = getPathOfOS("result/model.bin")
notes_ngrams_path   = getPathOfOS("result/notes_ngrams.json")
queries_path        = getPathOfOS("result/queries.json")
results_zip         = getPathOfOS("result/results.zip")
resulst_dir         = getPathOfOS("result")
divider             = getPathOfOS("/")
data_LawRepoWikiZIP = getPathOfOS("data/LawRepoWiki.zip")
_mainXML            = getPathOfOS("/main.xml")
_data               = getPathOfOS("/data")
dataDIR             = getPathOfOS("data")
data_xmls           = getPathOfOS("data/xmls")
_data_xmls           = getPathOfOS("/data/xmls")
data_dataset        = getPathOfOS("data/dataset")
