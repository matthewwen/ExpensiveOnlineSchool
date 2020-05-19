import json
import copy
import re

def strcmp(str1, str2, inst, dist=0, count=-1, index=-1, queryAtIndex=False):
    if inst == 0: 
        count = count if count != -1 else len(str1) if len(str1) >= len(str2) else len(str2)
        i = 0
        for i in range(count):
            if len(str1) == i or len(str2) == i:
                return 0
            elif str1[i] != str2[i]:
                diff = ord(str2[i]) - ord(str1[i])
                return diff if dist == 0 else -1 * diff 
        return 0
    else:
        return str2 - str1 if dist == 0 else str1 - str2

def swap(data, i1, i2):
    temp = data[i1]
    data[i1] = data[i2]
    data[i2] = temp

def binary_search(data, searchVal, queryList, start=0, end=-1, index=-1):
    end = len(data) if end == -1 else end
    midIdx = int((start + end) / 2)
    obj = data[midIdx]
    diff = strcmp(obj["name"], searchVal, 0, dist=0, count=len(searchVal), index=index)
    if diff == 0:
        # go backwards
        foundIdx = midIdx
        while (foundIdx + 1) > 0 and strcmp(data[foundIdx]["name"], searchVal, 0, \
                dist=0, queryAtIndex=True, count=len(searchVal)) == 0:
            foundIdx -= 1
        foundIdx += 1

        # append forward
        while foundIdx < end and strcmp(data[foundIdx]["name"], searchVal, 0, \
                dist=0, queryAtIndex=True, count=len(searchVal)) == 0:
            queryList.append(data[foundIdx])
            foundIdx+=1
        sort_function(queryList, "pop", dist=1)
    elif diff > 0:
        # go right
        if (end - midIdx) > 1:
            binary_search(data, searchVal, queryList, start=midIdx, end=end, index=index);
    elif diff < 0:
        # go left
        if (midIdx - start) > 1:
            binary_search(data, searchVal, queryList, start=start, end=midIdx, index=index);

def get_obj(data, idVal, start=0, end=-1):
    end = len(data) if end == -1 else end
    end = len(data) if end == -1 else end
    midIdx = int((start + end) / 2)
    obj = data[midIdx]
    diff = int(idVal - obj["id"])
    if diff == 0:
        return obj
    elif diff > 0:
        # go right
        if (end - midIdx) > 1:
            return get_obj(data, idVal, start=midIdx, end=end);
    elif diff < 0:
        # go left
        if (midIdx - start) > 1:
            return get_obj(data, idVal, start=start, end=midIdx);
    return None
    
# use a min heap
def sort_function(data, key, dist=0, query=-1, index=-1):
    numElement = len(data)
    inst = 1 if numElement > 0 and isinstance(data[0][key], int) else 0

    # Time Complexity: O(n + nlog(n)) -> O(n log(n))
    for size in range(numElement):
        element = data[size]
        canContinue = True

        i = size
        while canContinue:
            parent = int((i - 1) / 2)
            canContinue = i != parent and strcmp(data[i][key], data[parent][key], inst, dist=dist, index=index) < 0
            if canContinue:
                swap(data, i, parent)
            i = parent

    # Time Complexity: O(n + query * log(n)) -> O(query * log(n))
    newList = []
    newSize = numElement if query == -1 else query
    for i in range(newSize):
        idx = 0 
        limit = numElement - i - 1
        if query != -1:
            newList.append(data[idx])
        swap(data, idx, limit)

        canContinue = True
        while canContinue:
            # Determine which elements to swap
            left  = 2 * idx + 1
            right = left + 1
            pos = left if left < limit and strcmp(data[idx][key], data[left][key], inst, dist=dist, index=index) > 0 else idx
            pos = right if right < limit and strcmp(data[pos][key], data[right][key], inst,dist=dist, index=index) > 0 else pos
            canContinue = pos != idx  

            # Perform the swap
            if canContinue:
                swap(data, idx, pos)
            idx = pos
    
    return data if len(newList) == 0 else newList

"""
collegeList = {}
with open('../collegeName.txt') as json_file:
    collegeList = json.load(json_file)

collegeList["data"] = sort_function(collegeList["data"], "name")

for item in collegeList["data"]:
    item["ref"] = []

queryList = []
binary_search(collegeList["data"], "purdue", queryList, start=0, end=-1, index=-1)
print(queryList)

with open('collegeName.txt', "w") as json_file:
    json.dump(collegeList, json_file)
"""
