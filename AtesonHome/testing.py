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


# string = '500 g'
# res = re.search(r'(\d+)\s?([a-z]+)',string)
# weight = res.group(1)
# weight_unit = res.group(2)

# print(weight)
# print(weight_unit)

# def replace_text_in_between(text,start,end,replace_with=''):
#     idx_start = text.index(start) if start in text else None
#     idx_end = text.index(end) + len(end) if end in text else None
    
#     if idx_start == None or idx_end == None:
#         return text
#     return str(text[0:idx_start]) + replace_with + str(text[idx_end:])

# a = 'abcdefghijkl'

# res = remove_text_in_between(a,'c','g','#')
# print(res)

