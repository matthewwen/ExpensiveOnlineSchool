import re

def change_str(index, str1):
    word1 = re.split(r'\s|-', str1)
    if index < len(word1):
        count = 0
        for i in range(index):
            count += len(word1[i]) + 1
        return str1[count::] 
    else:
        return None

def change_list(index, jlist):
    newList = []
    for item in jlist:
        item["name"] = change_str(index, item["name"])
        if item["name"] != None:
            newList.append(item)
    return newList
