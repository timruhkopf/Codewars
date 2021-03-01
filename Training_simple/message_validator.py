import re

def is_a_valid_message(message):
    return all(n and int(n) == len(s) for n, s in re.findall("(\d*)(\D*)", message)[:-1])

if __name__ == '__main__':
    assert (is_a_valid_message("code4hello5") == False)
    assert (is_a_valid_message("3hey5hello2hi5") == False)
    assert (is_a_valid_message("3hey5hello2hi") == True)
    assert (is_a_valid_message("4code13hellocodewars") == True)
    assert (is_a_valid_message("code4hello5") == False)



