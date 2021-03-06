import re
import os
    
def parse_jes_output(spool):
    output_message = ''
           
    error_regex = [
        ('Data set {} not found:',                                           '(?<=DATA SET )(\S+)(?= NOT FOUND)'),
        ('Wrong permissions on data set {}',                                 '(?<=DATA SET: )(.*)(?= WITH RETURN CODE 08)'),
        ('Missimng DD Statement for {}',                                     '(\S*)(?= DD STATEMENT MISSING)'),
        ('Symbol not used: {} ',                                             '(?<=THE SYMBOL )(.*)(?= WAS NOT USED)'),
        ('Undefined or unusable host variable: {}',                          '(?<=UNDEFINED OR UNUSABLE HOST VARIABLE ")(.*)"'),
        ('Open Error - DDNAME: {}',                                          '(?<=OPEN ERROR - DDNAME )(\S){3,}'),
        ('DGP1 not available (trying to connect to prod db',                 'DGP1 NOT AVAILABLE'),
        ('SQLCODE -206 (probably forgot \':\' in sql query) {}',             '(?<=DSN2 BIND SQL ERROR)[\s\S]*(?<=SQLCODE=-206)[\s\S]*TOKENS=(\S*)'),
        ('Invalid comparison of {} to {}',                                   '"(.*)" was compared with "(.*)"'),
        ('{} was used in a arithmetic statement but is {}',                  '"(\S+) \((\S+)\)" was not numeric, but was a sender in an arithmetic expression'),
        ('SQLCODE -811 (SELECT statement recieved more than one records)',   '\*\*SQL RETURN CODE =        -811'),
        ('SQLCODE -991 (MOVE "UTLWKRRS" TO UTLWKSTG)',                       '\*\*SQL RETURN CODE =        -991'),
        ('SQLCODE -805 (SELECT returned multiple rows without cursor)',      '\*\*SQL RETURN CODE =        -991'),
        ]

    for message, regex in error_regex:
        found_errors = re.findall(regex, spool)
        found_errors = list(set(found_errors))
        while(found_errors.count('')):
            found_errors.remove('')
        if len(found_errors) > 0:
            for error in found_errors:
                if(type(error) == str):
                    output_message += message.format(error) + '\n'
                else:
                    output_message += message.format(*error) + '\n'
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
