import zipfile
import paths


def extractJsons():
    print("start extracting JSON DB")
    with zipfile.ZipFile(paths.results_zip, 'r') as zip_ref:
        zip_ref.extractall(paths.resulst_dir)
    
    print("Finished extracting JSON DB")

if __name__ == "__main__":
    extractJsons()

