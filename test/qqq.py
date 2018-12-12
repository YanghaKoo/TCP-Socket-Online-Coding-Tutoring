import re
 
regex = re.compile(r'a-z|A-Z|0-9')
print(regex.match('a'))
print(regex.match('b'))
print(regex.match('qsd'))