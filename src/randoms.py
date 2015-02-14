'''
Created on 2013-4-28

@author: Tony
'''
import random, string

def random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(length))

def main():
    for l in range(10):
        print random_string(l)

if __name__ == '__main__':
    main()
