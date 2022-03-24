import re
chaine = "123456789112233445566778899ABCDEFAABBCCDDEEFF"
req = re.search(r"[0-9a-f]{32}", chaine, re.I)
print(req.group())

import re
test = 'some text text test'
find = re.findall(r'text|test', test)
print(find)

import base64
print(base64.b64encode(bytes('your string', 'utf-8')))
