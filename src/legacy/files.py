'''
Created on 2013-4-28

@author: Tony
'''

def touch_open(filename, *args, **kwargs):
    open(filename, "a").close()
    return open(filename, *args, **kwargs)
