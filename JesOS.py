import re
import os
    
def parse_jes_output(spool):
    output_message = ''
           
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
        print(found_errors)
        while(found_errors.count('')):
            found_errors.remove('')
        if len(found_errors) > 0:
            output_message += message + '\n'
            for error in found_errors:
                output_message += error + '\n'
            output_message += '\n'
    return output_message

try:
    with open('output_dir.txt','r') as infile:
        output_dir = infile.read()
    os.chdir(output_dir)
    files = os.listdir()
    latest_output = max(files, key=os.path.getctime)
    with open(latest_output, 'r', encoding='utf8') as current_output:
        spool = current_output.read()
    print(parse_jes_output(spool))
except EnvironmentError as e:
    print (e)


input()
