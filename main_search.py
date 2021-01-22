import os
import xml.etree.ElementTree as ET

class main_search:
    def __init__(self,words_list):
        self.notes_returned=0
        self.lists_of_words=words_list
        self.lists_of_scetions=[]

    def slice_prefix(self,original):
        return (original[original.find("}")+1:len(original)])


    def get_paragraph_content_in_element(self,element):
        ret_list=[]
        for sub_element in element.iter():
            if(self.slice_prefix(sub_element.tag)== "p"):
                ret_list.append(sub_element)

        return ret_list



    def get_element_as_string(self,element):
        return ET.tostring(element,encoding='unicode')


    def this_side_note(self,word,element):
        # print(slice_prefix(element.tag))
        if self.slice_prefix(element.tag) == "authorialNote" and element.get("placement") == "side" :
            for sub_element in element.iter():
                if(self.slice_prefix(sub_element.tag) == "p"  and sub_element.text==word):
                    return True
                # else:
                #     print("this_side_note function ")


    def find_law_name(self,root):
        for element in root.iter():
            if(self.slice_prefix(element.tag) == "title" and element.get("eId")== "title"):
                for sub_element in element.iter():
                 if (self.slice_prefix(sub_element.tag) == "p"):

                    return sub_element.text


    def remove_duplicates(self,list):
        for i in range(len(list)-1,-1,-1):
            [_, name1, html1] = list[i]
            for j in range(i - 1,-1,-1):
                [_, name2, html2] = list[j]
                if (name1 == name2 and html1 == html2):
                    list.remove(list[i])

        return list



    def find_words(self,expanded_words_list):
        work_dir = "".join(os.getcwd())
        # ret_str=""
        # list_to_return=[] # list of lists([index, law name,html element as string]) to be returned
        # print(os.listdir(work_dir + "\\xmls"))
        for words_list in expanded_words_list:
            for word in words_list:
                for i in  range (len( os.listdir(work_dir+"\\xmls"))):
                # for i in  range (20):

                    tree = ET.parse(work_dir+"\\xmls\\law" + str(i)+".xml" )
                    # tree = ET.parse("law" + str(i)+".xml" )

                    root = tree.getroot()
                    for element in root.iter():
                        if(self.slice_prefix(element.tag)=="point"):
                            for sub_element in element.iter():
                                if (self.this_side_note(word,sub_element)):
                                    str_to_html= self.get_element_as_string(element)
                                    self.lists_of_scetions.append([i,self.find_law_name(root),str_to_html+"<br> <br> \n\n"])

        print(len(self.lists_of_scetions))
        self.lists_of_scetions=self.remove_duplicates(self.lists_of_scetions)
        print(len(self.lists_of_scetions))

        # print(lists_of_scetions)

        return self.lists_of_scetions

words_list=[["הגדרות"],["הגבלת פעילות במוסדות חינוך","שעה"]]
y=main_search(words_list)
x =y.find_words(words_list)
