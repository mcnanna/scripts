import sys
from time import sleep

def bar(counter, end, length=50):
    fraction = float(counter)/float(end)
    if counter == end:
        fraction = 1 # Avoid any floating point fuzziness near 1.0
    percent = int(fraction*100) # Rounds down
    
    equals = int(fraction*length)
    spaces = length - equals
    sys.stdout.write('\r')
    sys.stdout.write("[{}{}] {}%".format('='*equals, ' '*spaces, percent))
    sys.stdout.flush()
    if counter == end:
        print
