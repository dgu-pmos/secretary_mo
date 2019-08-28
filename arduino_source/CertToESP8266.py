import binascii
filename = 'gudah.crt'
with open(filename, 'rb') as f:
    content = f.read()

hexData = binascii.hexlify(content)
hexList = list(''.join(hexData))
print('// '+filename)
print('const unsigned char caCert[] PROGMEM = {\n')
outString = ''
caCertLen = 0


x = len(hexList)
for i in range(0, (x-1), 2):
    first = hexList[i]
    second = hexList[i+1]
    outString = outString+ '0x' + first + second + ', '
    caCertLen = caCertLen + 1
    if i%24 > 20 :
        outString = outString + '\n'

outString = outString[:-2] #remove last comma and space

print(outString+'};\n')
print('const unsigned int caCertLen = ' + str(caCertLen) + ';')
