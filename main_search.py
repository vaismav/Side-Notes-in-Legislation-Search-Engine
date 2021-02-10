import json
import os
import sys
import xml.etree.ElementTree as ET
import time

from googlesearch import search



class main_search:
    def __init__(self,words_list):
        """
        :param words_list: Expanded words lists to be found as notes in the laws xmls
        """
        self.sections_returned=0
        self.num_of_sections_each_time=5
        self.lists_of_words=words_list
        self.dict_of_side_notes={}
        self.build_req_dict_from_big_json()

        # Use a service account
        # cred = credentials.Certificate('./side-notes-search-engine-firebase-adminsdk-l1e10-9d9bbece62.json')
        # firebase_admin.initialize_app(cred)

        # self.db = firestore.client()

    def get_more_sections(self,word):
        """
        :return: List of lists (index, note, law name, html element as string) to be return to the client
        """
        word_dict=self.dict_of_side_notes[word]
        ret_list=[]


        for i in range(word_dict["sections_returned"],word_dict["sections_returned"]+self.num_of_sections_each_time):
            try:
                ret_list.append(word_dict[str(i)])
            except:
                break

        word_dict["sections_returned"] += self.num_of_sections_each_time

        return ret_list

    def slice_prefix(self,original):
        """
        :param original: Original tag of the element (with akn prefix)
        :return: Sliced element tag (without the prefix)
        """
        return (original[original.find("}")+1:len(original)])


    def get_element_as_string(self,element):
        """
        :param element: Xml element
        :return: A string representing the element.
        """
        return ET.tostring(element,encoding='unicode')


    def this_side_note(self,word,element):
        """
        :param word: String of side note to found.
        :param element: Xml element
        :return: True if element is a side note with the exact string word, else, False.
        """
        if self.slice_prefix(element.tag) == "authorialNote" and element.get("placement") == "side" :
            for sub_element in element.iter():
                if(self.slice_prefix(sub_element.tag) == "p"  and sub_element.text==word):
                    return True

            return False

        else:
            return False

    def get_side_note_string(self,element):
        if self.slice_prefix(element.tag) == "authorialNote" and element.get("placement") == "side" :
            for sub_element in element.iter():
                if(self.slice_prefix(sub_element.tag) == "p"  and sub_element.text!=" "):
                    return sub_element.text

        return  ""

    def find_law_name(self,root):
        """
        :param root: Xml element representing the root of the xml of the law.
        :return: The law name as string.
        """
        for element in root.iter():
            if(self.slice_prefix(element.tag) == "title" and element.get("eId")== "title"):
                for sub_element in element.iter():
                 if (self.slice_prefix(sub_element.tag) == "p"):

                    return sub_element.text



    # def found_already(self,word,law,section):
    #     """
    #     :param word: String of side note to found.
    #     :param law: Law name
    #     :param section: Xml element of a section as string.
    #     :return: True if the the section with word as a side note already in self.list_of_sections
    #     """
    #     for (i,word2,law2,section2) in self.lists_of_scetions:
    #         if law==law2 and word2==word and section==section2 :
    #             return True
    #
    #     return False


    def build_req_dict_from_big_json(self):
        f = open('all_sections.json', "r", encoding="utf8")
        data = json.load(f)
        for words_list in self.lists_of_words:
            for word in words_list:
                self.dict_of_side_notes[word]=data[word]
                self.dict_of_side_notes[word]["sections_returned"]=0
        print(self.dict_of_side_notes.keys())




    def find_words_original_zip(self):
        """
        This function creates the list of sections, each record look like: (index,side_note,law_name,html_element (as string))
        """
        work_dir = "".join(os.getcwd())
        for words_list in self.lists_of_words:
            for word in words_list:
                for law_id in  range (len( os.listdir(work_dir+"\\xmls"))):

                    tree = ET.parse(work_dir+"\\xmls\\law" + str(law_id)+".xml" )
                    root = tree.getroot()
                    for element in root.iter():
                        if(self.slice_prefix(element.tag)=="point"):
                            for sub_element in element.iter():
                                if (self.this_side_note(word,sub_element)):
                                    law_name=self.find_law_name(root)
                                    str_to_html= self.get_element_as_string(element)+"<br> <br> \n\n"
                                    #modify dictionary
                                    if(word not in self.dict_of_side_notes):
                                        self.dict_of_side_notes[word]=[{"law_id":law_id,
                                                                         "law_names":[law_name],
                                                                         "string_to_html":str_to_html
                                                                         }]
                                    else:
                                        index=self.index_of_same_html(self.dict_of_side_notes[word],str_to_html)
                                        if(index>-1):
                                            self.dict_of_side_notes[word][index]["law_names"].append(law_name)
                                        else:
                                            self.dict_of_side_notes[word].append({"law_id":law_id,
                                                                                  "law_names":[law_name],
                                                                                  "string_to_html":str_to_html
                                                                                  })




    def extract_all_side_notes(self):
        """
        This function creates a text file contains all the side notes in the corpus.
        """
        all_side_notes_file=open("all_side_notes_file.txt","w",encoding="utf8")
        work_dir = "".join(os.getcwd())
        for i in range(len(os.listdir(work_dir + "\\xmls"))):
            tree = ET.parse(work_dir + "\\xmls\\law" + str(i) + ".xml")
            root = tree.getroot()
            for element in root.iter():
                if self.slice_prefix(element.tag) == "authorialNote" and element.get("placement") == "side":
                    for sub_element in element.iter():
                        if (self.slice_prefix(sub_element.tag) == "p" ):
                            s=sub_element.text
                            if(len(s)>1):
                                all_side_notes_file.write( sub_element.text +" @@@\n")
                                break
        all_side_notes_file.close()


    def fill_local_db_to_json(self):
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
                if (self.slice_prefix(element.tag) == "point"):
                    for sub_element in element.iter():
                        word = self.get_side_note_string(sub_element)
                        if (len(word) > 1):
                            law_name = self.find_law_name(root)
                            str_to_html = self.get_element_as_string(element) + "<br> <br> \n\n"
                            if (word not in my_json ):
                                my_json[word]={0:{"law_id":law_id,
                                             "law_names":[law_name],
                                              "string_to_html":str_to_html,
                                              "uploaded_to_db":False

                                             }}
                            else:
                                index = self.index_of_same_html(my_json[word], str_to_html)
                                if (index > -1):
                                    my_json[word][index]["law_names"].append(law_name)
                                else:
                                    my_json[word][len(my_json[word].keys())]={"law_id":law_id,
                                                                             "law_names":[law_name],
                                                                             "string_to_html":str_to_html,
                                                                             "uploaded_to_db":False
                                                                             }


        with open("all_sections2.json", "w", encoding='utf8') as outfile:
            json.dump(my_json, outfile, ensure_ascii=False)


    def slice_triangle(self,param):
        return param[param.find(">") + 1:len(param)]


    def get_element_as_string2(self, element):
        ret=""
        for sub_element in element.iter():
            # print(self.slice_prefix(sub_element.tag))
            try:
                if(self.slice_prefix(sub_element.tag)=="num"):
                    ret = ret + sub_element.text
                    # print(ret)
                elif(self.slice_prefix(sub_element.tag) in ["content","intro"]):
                    for sub_sub_element in sub_element.iter():
                        # print(self.slice_prefix(sub_sub_element.tag))
                        if (self.slice_prefix(sub_sub_element.tag) == "p"):
                                if(len(sub_sub_element.text)>1):
                                    ret=ret+sub_sub_element.text+"<br> <br> "
                                    # print(ret)
                                else:
                                    for comment in sub_sub_element.iter():
                                        # print(self.slice_prefix(comment.tag))
                                        if (self.slice_prefix(comment.tag) == "wikicomment"):
                                            ret = ret + comment.text + "<br>  "
                                            # print(ret)
                        elif (self.slice_prefix(sub_sub_element.tag) == "def"):
                                ret=ret+self.slice_triangle(ET.tostring(sub_sub_element,encoding="unicode")) +"<br>  "


            except:
                x = 5
        return (ret)
    
    
    # def fill_sections_documents_in_db(self):
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
    #                     doc_ref = self.db.collection(u'notes').document(u'' + str(key))
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

    # def section_already_in_db(self, word, law_name, str_to_html):
    #     users_ref = self.db.collection(u'sections')
    #     docs = users_ref.stream()
    #     for doc in docs:
    #         doc_dict=doc.to_dict()
    #         if(doc_dict["side_note"]==word and doc_dict["law_name"]==law_name
    #                 and doc_dict["string_to_html"]==str_to_html ):
    #             print("its here -inside if")
    #             return True
    #
    #     return False

    def index_of_same_html(self, lst, str_to_html):
        for i in range (len(lst)):
            dict=lst[i]
            if (dict["string_to_html"]==str_to_html):
                return i
        return -1

    def get_law_url_on_web(self, law_name):
        for url in search(law_name, tld='co.il', num=10, stop=1, pause=2):
            return url

    # def section_already_in_local_db(self, my_json, word, law_name, str_to_html):
    #     # users_ref = self.db.collection(u'sections')
    #     # docs = users_ref.stream()
    #     if(word not in my_json):
    #         return False
    #     for json_object in my_json[word]:
    #         if json_object["string_to_html"]==str_to_html:
    #             return law_name in json_object[]


words_list=[["פירוש","הגדרות"],["הגבלת פעילות מוסדות","מועד זכות־היוצרים"]]
y=main_search(words_list)
y.fill_local_db_to_json()
