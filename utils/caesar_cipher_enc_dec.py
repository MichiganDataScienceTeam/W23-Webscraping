def decode(string, key):
    if len(string) != len(key):
        print(string)
        print(key)
        raise 'Key not of correct length'
    
    new_string = ''
    for x, k in zip(string, str(key)):
        new_string += chr(ord(x)+int(k))
        
    return new_string

def encode(string, key):
    if len(string) != len(key):
        print(string)
        print(key)
        raise 'Key not of correct length'
    
    new_string = ''
    for x, k in zip(string, str(key)):
        new_string += chr(ord(x)-int(k))
        
    return new_string


# with open('static/caesar.txt', 'r') as f:
#     lines = f.readlines()
#     for line, k in zip(lines[:len(lines)//2], lines[len(lines)//2:]):
#         line = line.strip()
#         k = k.strip()
#         print(line, encode(line, k), decode(encode(line, k), k), '_', sep='\n')
        
