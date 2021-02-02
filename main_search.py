import os
import xml.etree.ElementTree as ET

class main_search:
    def __init__(self,words_list):
        """
        :param words_list: Expanded words lists to be found as notes in the laws xmls
        """
        self.sections_returned=0
        self.num_of_sections_each_time=5
        self.lists_of_words=words_list
        self.lists_of_scetions=[]

    def get_more_sections(self):
        """
        :return: List of lists (index, note, law name, html element as string) to be return to the client
        """
        ret_list=[]
        for i in range(self.sections_returned, len(self.lists_of_scetions)):
            ret_list.append(self.lists_of_scetions[i])

        self.sections_returned += self.num_of_sections_each_time

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


    def found_already(self,word,law,section):
        """
        :param word: String of side note to found.
        :param law: Law name
        :param section: Xml element of a section as string.
        :return: True if the the section with word as a side note already in self.list_of_sections
        """
        for (i,word2,law2,section2) in self.lists_of_scetions:
            if law==law2 and word2==word and section==section2 :
                return True

        return False



    def find_words_original_zip(self):
        """
        This function creates the list of sections, each record look like: (index,side_note,law_name,html_element (as string))
        """
        work_dir = "".join(os.getcwd())
        for words_list in self.lists_of_words:
            for word in words_list:
                for i in  range (len( os.listdir(work_dir+"\\xmls"))):

                    tree = ET.parse(work_dir+"\\xmls\\law" + str(i)+".xml" )
                    root = tree.getroot()
                    for element in root.iter():
                        if(self.slice_prefix(element.tag)=="point"):
                            for sub_element in element.iter():
                                if (self.this_side_note(word,sub_element)):
                                    law_name=self.find_law_name(root)
                                    str_to_html= self.get_element_as_string(element)+"<br> <br> \n\n"
                                    if not self.found_already(word, law_name,str_to_html):
                                        self.lists_of_scetions.append([i,word,law_name,str_to_html])


        # return self.lists_of_scetions
    def extract_all_side_notes(self):
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



words_list=[["הגדרות"],["הגבלת פעילות במוסדות חינוך","שעה"]]
# y=main_search(words_list)
# y.extract_all_side_notes()
# y.find_words_original_zip()
print(y.get_more_sections())
print(y.get_more_sections())
