# Side-Notes-in-Legislation-Search-Engine

* [General info](#general-info)
* [Screenshots](#screenshots)
* [Technologies](#technologies)
* [Setup](#setup)
* [How to run](#how-to-run)
* [How it works](#how-it-works)
* [Features](#features)
* [Status](#status)




## General info
This project is part of "Digital Humanities for CS" course.
It is a search engine of sections by side notes in laws in Israel, built to help lawyers to write laws.

## Screenshots

![main web page](https://github.com/vaismav/Side-Notes-in-Legislation-Search-Engine/blob/main/screenshot.jpeg)

## Technologies
* Server - Python (3.7) flask
* Client - React

## Setup
* install python3 (or above)
* install pip (sudo apt-get install python3-pip)
* install flask (pip3 install Flask)

## How to run
* On terminal run:
 git clone https://github.com/vaismav/Side-Notes-in-Legislation-Search-Engine.git

 cd Side-Notes-in-Legislation-Search-Engine
 
 python3 install.py

## How it works
* All xml(law) files extracted from /data/LawRepoWiki.zip to /data/xmls.
* A JSON fill of all sections created.
* FastText model ( https://fasttext.cc/docs/en/unsupervised-tutorial.html ) run on all the side notes in the JSON.
* A flask application created from 'app.py'.
* The user ask for a side note x, the server search for a side notes that are closest to x in in the trained model data and offers them to te user.
* The user pick a side note y and get a list of sections witch y is their side note.

## Code Examples

```
   def fill_local_db_to_json():
    """
    This function creates a JSON file(all_sections.json) contains all the sections(law_id, law_names, html element representing the section, uploaded_to_db(True/False).
    """
    section_id = 0
    my_json={}
    work_dir = "".join(os.getcwd())
    for law_id in range(len(os.listdir(work_dir + paths._data_xmls))):
        tree = ET.parse(work_dir + paths._data_xml_law_file + str(law_id) + ".xml")
        root = tree.getroot()
        for element in root.iter():
            if (slice_prefix(element.tag) == "point"):
                for sub_element in element.iter():
                    word = get_side_note_string(sub_element)
                    if (len(word) > 1):
                        print(section_id)
                        section_id+=1
                        law_name = find_law_name(root)
                        str_to_html = get_element_as_string2(element)
                        if (word not in my_json ):
                            my_json[word]={0:{"law_id":law_id,
                                         "law_names":[law_name],
                                          "string_to_html":str_to_html,
                                          "uploaded_to_db":False

                                         }}
                        else:
                            index = index_of_same_html(my_json[word], str_to_html)
                            if (index > -1):
                                my_json[word][index]["law_names"].append(law_name)
                            else:
                                my_json[word][len(my_json[word].keys())]={"law_id":law_id,
                                                                         "law_names":[law_name],
                                                                         "string_to_html":str_to_html,
                                                                         "uploaded_to_db":False
                                                                         }


    with open(paths.all_sections_path, "w", encoding='utf8') as outfile:
        json.dump(my_json, outfile, ensure_ascii=False, indent=4, sort_keys=True)

```


<!-- ### Requirements
To run this project, Python3, pip3 & pip are requierd -->