val_char = dict(enumerate([' ','X', 'R', 'L', 'o', 'g', 'd', 'K', '[', ']', '0', '1', '2', '3','A','Z','E','Y','H','N','+','{','}','v','^','C','B','M','I']))
char_val = dict((v, k) for k, v in val_char.items())

print(val_char)
print(1 in val_char)

print(char_val)
print('X' in char_val)
# with open("test","wb") as f :
#     a = 5
#     f.write(a.to_bytes(2,"big"))
#     # f.write(bytes(b'\xFF'))
#     # f.write(bytes(b'\x25'))
#     # f.write(bytes(b'\x68'))
#
# with open("test","rb") as f :
#     b = bytes(f.read())
#
#     print(int.from_bytes(b,"big"))

