import random
import string

def make_random_string(ln):
    return ''.join( [random.choice(string.ascii_letters) for i in range(ln)] )