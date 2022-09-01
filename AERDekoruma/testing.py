import re
tmp_additional_description = '1kg'
res = re.search(r'([\d.,]+)\s?(kg|g)',tmp_additional_description)

print(res.group(2))