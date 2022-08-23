# material = 'Materials Metal, Sungkai Wood'
# def replace_multiple_char(text, char_to_replace):
#     for key, value in char_to_replace.items():
#         text = text.replace(key, value)

#     return text
# char_to_replace = {
#     'bahan':'',
#     'materials':'',
#     'material':'',
# }
# material = material.lower()
# print(material)
# material = replace_multiple_char(material,char_to_replace)
# material = material.strip()
# material = material.split(',')

# print(material)
# a = ['(aaaaa)','bbbbbb','ccccc']
# b = a
# for co,data in enumerate(a):
#     if '(' or ')' in data:
#         b[co] = data.replace('(','').replace(')','')

# print(b)
# import re


# string = 'rattan, metal, copper(20%), jati (teakwood), anjuing (50%),(asdsad, asdasd)'
# string = re.sub(r'[^a-z(),\s]*','',string)
# print('====')
# print(string)
# string = re.sub(r'(?:\(|\)|\(\)|\(\w+\)|\(\w+|\w+\))','',string)
# print('====')
# print(string)
# string = string.split(',')
# string = [x.strip() for x in string if x.strip()]
# # re.

# print('====')
# print(string)

# import os
# dirname = os.path.dirname(__file__)
# print(dirname)
a = 'aa'
b = 'aa'
c= 'aa'

if a == b == c:
    print(a)