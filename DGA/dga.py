import sys,os
import random
import base64
import random
import socket
import string


'''OrionImprovementBusinessLayer.CryptoHelper.Base64Decode-decode'''
def Decode(string):
	text = "rq3gsalt6u1iyfzop572d49bnx8cvmkewhj"
	text2 = "0_-."
	retstring = ""
	flag = False
	for i in range(len(string)):
		ch = string[i]
		tx_index = -1
		tx2_index = -1
		if flag:
			t1i = text.find(ch)
			x = t1i - ((random.randint(0,8) % (len(text) / len(text2))) * len(text2))
			retstring = retstring+text2[int(x % len(text2))]
			flag = False
			continue
		if ch in text2:
			tx2_index = text2.find(ch)
			flag = True
			pass
		else:
			tx_index = text.find(ch)
			oindex = tx_index - 4
			retstring = retstring+text[oindex % len(text)]

		pass
	return retstring


def Base32Decode(string):
	text = "ph2eifo3n5utg1j8d94qrvbmk0sal76c"
	restring = ""
	datalen = len(string) / 8 * 5
	num = 0
	ib = 0;
	if len(string) < 3:
		restring = chr(text.find(string[0]) | text.find(string[1]) << 5 & 255)
		return restring

	k = text.find(string[0]) | (text.find(string[1]) << 5)
	j = 10
	index = 2
	for i in range(int(datalen)):
		restring += chr(k & 255)
		k = k >> 8
		j -= 8
		while( j < 8 and index < len(string)):
			k |= (text.find(string[index]) << j)
			index += 1
			j += 5

	return restring

def decodage(string):
    string2 = string.rstrip().split(".")[0][14:]
    if "00" in string:
        string3 = string[2:]
        comp = Base32Decode(string3)
    else:

        comp = Decode(string2)
    return comp


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

    # letters = string.ascii_lowercase + string.digits
    # guid = ''.join(random.choice(letters) for i in range(15))

    # random_byte = random.choice(letters)
    # domain_name = guid + random_byte

    if os.environ.get("USERNAME") is not None:
        hostname = os.environ.get("USERNAME")
    else:
        hostname = socket.gethostname()

    normal_encoding = True
    hostname = hostname.lower()

    for letter in hostname:
        if letter not in "0123456789abcdefghijklmnopqrstuvwxyz-_.":
            normal_encoding = False

    if normal_encoding:
        domain_name = Encode(hostname)

    else:
        domain_name = Base32Encode(hostname, False)

    domain_name += f"{domain_name}.appsync-api.us-east-{random.randint(1,2)}.avsvmcloud.com"

    print(f"encodage : {domain_name}")
    print(f"décodage : {decodage(domain_name)}")