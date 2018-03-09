# -*- coding: utf-8 -*-
'''
create counter class


'''
class bgcol:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def saveHtml(text, fileName):
    with open(fileName, 'w') as f:
        f.write(text.encode('utf-8'))
    return

