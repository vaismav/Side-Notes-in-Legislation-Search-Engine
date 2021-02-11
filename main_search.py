import json
import os
import sys
import xml.etree.ElementTree as ET
import time

from googlesearch import search

def slice_prefix(original):
    """
    :param original: Original tag of the element (with akn prefix)
    :return: Sliced element tag (without the prefix)
    """
    return (original[original.find("}")+1:len(original)])


def this_side_note(word,element):
    """
    :param word: String of side note to found.
    :param element: Xml element
    :return: True if element is a side note with the exact string word, else, False.
    """
    if slice_prefix(element.tag) == "authorialNote" and element.get("placement") == "side" :
        for sub_element in element.iter():
            if(slice_prefix(sub_element.tag) == "p"  and sub_element.text==word):
                return True

        return False

    else:
        return False

def get_side_note_string(element):
    if slice_prefix(element.tag) == "authorialNote" and element.get("placement") == "side" :
        for sub_element in element.iter():
            if(slice_prefix(sub_element.tag) == "p"  and sub_element.text!=" "):
                return sub_element.text

    return  ""

def find_law_name(root):
    """
    :param root: Xml element representing the root of the xml of the law.
    :return: The law name as string.
    """
    for element in root.iter():
        if(slice_prefix(element.tag) == "title" and element.get("eId")== "title"):
            for sub_element in element.iter():
             if (slice_prefix(sub_element.tag) == "p"):

                return sub_element.text

def build_req_dict_from_big_json():
    f = open('all_sections.json', "r", encoding="utf8")
    data = json.load(f)
    for words_list in lists_of_words:
        for word in words_list:
            dict_of_side_notes[word]=data[word]
            dict_of_side_notes[word]["sections_returned"]=0
    print(dict_of_side_notes.keys())


def find_words_original_zip():
    """
    This function creates the list of sections, each record look like: (index,side_note,law_name,html_element (as string))
    """
    work_dir = "".join(os.getcwd())
    for words_list in lists_of_words:
        for word in words_list:
            for law_id in  range (len( os.listdir(work_dir+"\\xmls"))):

                tree = ET.parse(work_dir+"\\xmls\\law" + str(law_id)+".xml" )
                root = tree.getroot()
                for element in root.iter():
                    if(slice_prefix(element.tag)=="point"):
                        for sub_element in element.iter():
                            if (this_side_note(word,sub_element)):
                                law_name=find_law_name(root)
                                str_to_html= get_element_as_string2(element)+"<br> <br> \n\n"
                                #modify dictionary
                                if(word not in dict_of_side_notes):
                                    dict_of_side_notes[word]=[{"law_id":law_id,
                                                                     "law_names":[law_name],
                                                                     "string_to_html":str_to_html
                                                                     }]
                                else:
                                    index=index_of_same_html(dict_of_side_notes[word],str_to_html)
                                    if(index>-1):
                                        dict_of_side_notes[word][index]["law_names"].append(law_name)
                                    else:
                                        dict_of_side_notes[word].append({"law_id":law_id,
                                                                              "law_names":[law_name],
                                                                              "string_to_html":str_to_html
                                                                              })


def extract_all_side_notes():
    """
    This function creates a text file contains all the side notes in the corpus.
    """
    all_side_notes_file=open("all_side_notes_file.txt","w",encoding="utf8")
    work_dir = "".join(os.getcwd())
    for i in range(len(os.listdir(work_dir + "\\xmls"))):
        tree = ET.parse(work_dir + "\\xmls\\law" + str(i) + ".xml")
        root = tree.getroot()
        for element in root.iter():
            if slice_prefix(element.tag) == "authorialNote" and element.get("placement") == "side":
                for sub_element in element.iter():
                    if (slice_prefix(sub_element.tag) == "p" ):
                        s=sub_element.text
                        if(len(s)>1):
                            all_side_notes_file.write( sub_element.text +" @@@\n")
                            break
    all_side_notes_file.close()


def fill_local_db_to_json():
    """
    This function creates a JSON file(all_sections.json) contains all the sections(law_id, law_names, html element representing the section, uploaded_to_db(True/False).
    """
    section_id = 0
    my_json={}
    work_dir = "".join(os.getcwd())
    for law_id in range(len(os.listdir(work_dir + "\\data\\xmls"))):
        tree = ET.parse(work_dir + "\\data\\xmls\\law" + str(law_id) + ".xml")
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


    with open("all_sections.json", "w", encoding='utf8') as outfile:
        json.dump(my_json, outfile, ensure_ascii=False)


def slice_triangle(param):
    return param[param.find(">") + 1:len(param)]

def get_element_as_string2( element):
    ret=""
    for sub_element in element.iter():
        # print(slice_prefix(sub_element.tag))
        try:
            if(slice_prefix(sub_element.tag)=="num"):
                ret = ret + sub_element.text
                # print(ret)
            elif(slice_prefix(sub_element.tag) in ["content","intro"]):
                for sub_sub_element in sub_element.iter():
                    # print(slice_prefix(sub_sub_element.tag))
                    if (slice_prefix(sub_sub_element.tag) == "p"):
                            if(len(sub_sub_element.text)>1):
                                ret=ret+sub_sub_element.text+"<br> <br> "
                                # print(ret)
                            else:
                                for comment in sub_sub_element.iter():
                                    # print(slice_prefix(comment.tag))
                                    if (slice_prefix(comment.tag) == "wikicomment"):
                                        ret = ret + comment.text + "<br>  "
                                        # print(ret)
                    elif (slice_prefix(sub_sub_element.tag) == "def"):
                            ret=ret+slice_triangle(ET.tostring(sub_sub_element,encoding="unicode")) +"<br>  "


        except:
            x = 5
    return (ret)


# def fill_sections_documents_in_db():
#     """
#     This function add the sections to the firebase db.
#     """
#     notes_pushed=5000
#     f = open('all_sections.json',"r",  encoding="utf8")
#     data = json.load(f)
#     f.close()
#     keys = data.keys()
#     for key in keys:
#         for next_key in data[key].keys():


#             if (not data[key][next_key]["uploaded_to_db"]) :

#                 with open("all_sections.json", "w", encoding='utf8') as outfile:
#                     json.dump(data, outfile, ensure_ascii=False)
#                 try:
#                     data[key][next_key]["uploaded_to_db"] = True
#                     doc_ref = db.collection(u'notes').document(u'' + str(key))
#                     doc_ref.set(data[key])
#                     print("note " + str(key) + f"pushed to db -->{notes_pushed} pushed so far  ")

#                     notes_pushed = notes_pushed + 1

#                     if(notes_pushed==48000):
#                         return
#                 except:
#                     data[key][next_key]["uploaded_to_db"] = False
#                     print( str(key)+"["+str(next_key)+"]" +" wasn't uploaded")
#                     break

#             else:
#                 print("here")

# def section_already_in_db( word, law_name, str_to_html):
#     users_ref = db.collection(u'sections')
#     docs = users_ref.stream()
#     for doc in docs:
#         doc_dict=doc.to_dict()
#         if(doc_dict["side_note"]==word and doc_dict["law_name"]==law_name
#                 and doc_dict["string_to_html"]==str_to_html ):
#             print("its here -inside if")
#             return True
#
#     return False

def index_of_same_html( lst, str_to_html):
    for i in range (len(lst)):
        dict=lst[i]
        if (dict["string_to_html"]==str_to_html):
            return i
    return -1

def get_law_url_on_web( law_name):
    for url in search(law_name, tld='co.il', num=10, stop=1, pause=2):
        return url

# def section_already_in_local_db( my_json, word, law_name, str_to_html):
#     # users_ref = db.collection(u'sections')
#     # docs = users_ref.stream()
#     if(word not in my_json):
#         return False
#     for json_object in my_json[word]:
#         if json_object["string_to_html"]==str_to_html:
#             return law_name in json_object[]


fill_local_db_to_json()
