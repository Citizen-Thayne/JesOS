import re
import os

def get_latest_spool():
    with open('output_dir','r') as output_dir
        os.chdir(output_dir)
        files = os.listdir()
        return max(files, key=os.path.getctime)

f = open(get_latest_spool(),'r', encoding="utf8")
spool =  f.read()
f.close()

message = ''
       
error_regex = [
    ('Data sets not found:',                                             '(?<=DATA SET )(.*)(?= NOT FOUND)'),
    ('Wrong permissions (Probably looking at prod when should be test)', '(?<=DATA SET: )(.*)(?= WITH RETURN CODE 08)'),
    ('Missimng DD Statement:',                                           '(\S*)(?= DD STATEMENT MISSING)'),
    ('The following symbols were not used: ',                            '(?<=THE SYMBOL )(.*)(?= WAS NOT USED)'),
    ('Undefined or unusable host variable',                              '(?<=UNDEFINED OR UNUSABLE HOST VARIABLE ")(.*)"'),
    ('Open Error - DDNAME:',                                             '(?<=OPEN ERROR - DDNAME )(\S*)'),
    ('DGP1 not available (trying to connect to prod db',                 'DGP1 NOT AVAILABLE'),
    ('SQLCODE -206, probably forgot \':\' on sql quuery',                '(?<=DSN2 BIND SQL ERROR)[\s\S]*(?<=SQLCODE=-206)[\s\S]*TOKENS=(\S*)')
    ]

for message, regex in error_regex:
    found_errors = re.findall(regex, spool)
    found_errors = list(set(found_errors))
    while(found_errors.count('')):
        found_errors.remove('')
    if len(found_errors) > 0:
        print(message)
        for error in found_errors:
            print(error)
        print('')
input()
