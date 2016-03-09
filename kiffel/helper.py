from random import randint

class EAN8:
    def get_random():
        code = str(randint(1000000, 9999999))
        weighed_sum = int(code[0])*3 + int(code[1])*1 + int(code[2])*3 + \
            int(code[3])*1 + int(code[4])*3 + int(code[5])*1 + int(code[6])*3
        checksum = (10 - (weighed_sum % 10)) % 10
        code = code + str(checksum)
        return code
