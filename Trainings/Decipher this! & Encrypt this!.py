import re


def decipher_this(text):
    def switch(matchobj):
        slice = matchobj.group(0)
        return ''.join([slice[-1], slice[1:-1], slice[0]])

    new = re.sub('[A-z][A-z]+', switch, text)
    return re.sub(r'\d+', lambda x: chr(int(x.group(0))), new)


def encrypt_this(text):
    def switch(matchobj):
        slice = matchobj.group(0)
        return ''.join([slice[-1], slice[1:-1], slice[0]])

    new = re.sub(r'\b\w', lambda x: str(ord(x.group(0))), text)
    return re.sub('[A-z][A-z]+', switch, new)


if __name__ == '__main__':
    decipher_this("104olle 119drlo")
    encrypt_this("hello world")