# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import os
import sys
import sys
reload(sys)
sys.setdefaultencoding('utf8')


'''
First Use Java Library 'PKUSUMSUM' to Implement
Two Basic Summary Algorithms:
Submodular1, Submodular2
We Run It by Cmd...But It Produce Nothing.
'''

JAR_PATH = "/Volumes/YOUNG/Summary-Projects/PKUSUMSUM/PKUSUMSUM.jar"

if __name__ == "__main__":
    # Print Args
    args = ''
    for i in range(1, len(sys.argv)):
        print(sys.argv[i])
        args += sys.argv[i] + ' '
    print("java -jar " + JAR_PATH + " " + args)
    os.system("java -jar " + JAR_PATH + " " + args)
