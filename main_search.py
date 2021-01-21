import os
import xml.etree.ElementTree as ET

def slice_prefix(original):
    return (original[original.find("}")+1:len(original)])


def get_paragraph_content_in_element(element):
    ret_list=[]
    for sub_element in element.iter():
        if(slice_prefix(sub_element.tag)=="p"):
            ret_list.append(sub_element)

    return ret_list



def get_element_as_string(element):
    return ET.tostring(element,encoding='unicode')


def this_side_note(word,element):
    # print(slice_prefix(element.tag))
    if slice_prefix(element.tag) == "authorialNote" and element.get("placement") == "side" :
        for sub_element in element.iter():
            if(slice_prefix(sub_element.tag) == "p"  and sub_element.text==word):
                return True
            # else:
            #     print("this_side_note function ")


def find_law_name(root):
    for element in root.iter():
        if(slice_prefix(element.tag) == "title" and element.get("eId")=="title" ):
            for sub_element in element.iter():
             if (slice_prefix(sub_element.tag) == "p"):

                return sub_element.text


def find_words(expanded_words_list):
    work_dir = "".join(os.getcwd())
    # ret_str=""
    list_to_return=[] # list of lists([index, law name,html element as string]) to be returned
    print(os.listdir(work_dir + "\\xmls"))
    for words_list in expanded_words_list:
        for word in words_list:
            # for i in  range (len( os.listdir(work_dir+"\\xmls"))):
            for i in  range (20):

                tree = ET.parse(work_dir+"\\xmls\\law" + str(i)+".xml" )
                # tree = ET.parse("law" + str(i)+".xml" )

                root = tree.getroot()
                for element in root.iter():
                    if(slice_prefix(element.tag)=="point"):
                        for sub_element in element.iter():
                            if (this_side_note(word,sub_element)):
                                str_to_html= get_element_as_string(element)
                                print(i,find_law_name(root))
                                list_to_return.append([i,find_law_name(root),str_to_html+"<br> <br> \n\n"])
                                # ret_str=ret_str+str_to_html +"<br> <br> \n\n"
    # print(ret_str)
    return list_to_return





words_list=[["הגדרות"],["הגבלת פעילות במוסדות חינוך","שעה"]]
#
# # find_words(5)
# find_words(words_list)


# import lxml.etree as ET
# f = ET.StringIO('<a><b>Text</b></a>')
# doc = ET.parse(f)
# result_tree = transform(doc)
x =find_words(words_list)