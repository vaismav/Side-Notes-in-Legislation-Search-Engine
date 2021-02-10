import platform

def getPathOfOS(path):
    if(platform.system == "Windows"):
            return path.replace("/","\\")
    return path

data_xml_law_file   = getPathOfOS("data/xmls/law")
all_sections_path   = getPathOfOS("result/all_sections.json")
model_path          = getPathOfOS("result/model.bin")
notes_ngrams_path   = getPathOfOS("result/notes_ngrams.json")
queries_path        = getPathOfOS("result/queries.json")
results_zip         = getPathOfOS("result/results.zip")
resulst_dir         = getPathOfOS("result")

