#! python
# -*- coding: utf-8 -*-
""" The program receives the name of the csv file from the startup parameters
or from the input line, and normalizes the description of the screws in 
accordance with the rule described in the task
"""

# for use the startup parameters
import sys
# for use the regular expressions
import re

def get_file_path():
    """ The function receives the file path from the startup parameters
        or from the input line if it's necessary
    """
    if len (sys.argv) == 1:
        inp=input('Press "Enter" to exit or enter a file path:')
        if inp:
            file_path = inp
        else : 
            exit()
    else:
        file_path = sys.argv[1]
    return file_path

def size_define_parser(line):
    """ The function receives a string at the input and tries to find the 
    linear dimensions of the self-tapping screw in it. The output value is
    a tuple consisting of two strings. The first string contains the length 
    value in the second diameter value.
    """
    # Create a regular expression that finds linear dimensions in a string.
    size_match=re.search(r'\b[0-9\\/().,м]+\s?[xXхХ*\\/]\s?[0-9\\/().,м]+\b', line)
    if size_match:
        size_string = size_match[0].replace(',','.')
        size_list=[float(i) for i in re.findall(r'\d{1,3}\.?\d?',size_string)]
        size_list.sort()
        return (str(size_list[-1]), str(size_list[-2]))
    # Previous regex does not catch cases where the size of the numbers stick
    # to the words. I didn't undarstood how to correctly modify it, and create 
    # additional regex which fix it.
    size_match=re.search(r'[0-9.,]{1,3}\s?[xXхХ*]\s?[0-9.,]{1,3}', line)
    if size_match:
        size_string = size_match[0].replace(',','.')
        size_list=[float(i) for i in re.findall(r'\d{1,3}\.?\d?',size_string)]
        size_list.sort()
        return (str(size_list[-1]), str(size_list[-2]))
    # The last regular expression catches those cases when there is only one
    # explicit size (indicating the dimension mm). I assumed that the only 
    # size is long.
    size_match=re.search(r'[0-9.,]{1,5}\s?мм', line)
    if size_match:
        size_string = size_match[0].replace(',','.')
        long=float(re.search(r'[0-9.]{1,5}',size_string)[0])
        return (str(long), 'None')
    return ('None', 'None')   

def color_define_parser(line):
    """ The function receives a string at the input and tries to find the 
    color of the self-tapping screw in it. The output value is
    a string which contain normalize value of color. Since the task does not
    directly indicate the way to normalize the text, I chose the following 
    method. If the description refers to a color according to the RAL catalog,
    it is used, otherwise the names of simple colors are used.
    """
    # find RAL color
    color_match=re.search(r'[Rr][Aa][Ll]\s?-?\s?\d{4}', line)
    if color_match:
        return 'RAL-'+color_match[0][-4:]
    # find sky blue
    color_match=re.search(r'небесно-голубой', line)
    if color_match:
        return 'RAL - 5009'
    # find yello color
    color_match=re.search(r'[Жж][ЕеЁёEe][Лл]', line)
    if color_match:
        return 'Желтый'
    # find red color
    color_match=re.search(r'[КкKk][РрPp][АаAa][СсCc][НнH]', line)
    if color_match:
        return 'Красный'
    # find green color
    color_match=re.search(r'[Зз][ЕеEe][Лл]', line)
    if color_match:
        return 'Зеленый'
    # find blue color
    color_match=re.search(r'[СсCc][Ии][НнH]', line)
    if color_match:
        return 'Синий'
    # find white color
    color_match=re.search(r'[Бб][ЕеEe][Лл]', line)
    if color_match:
        return 'Белый'
    # find grey color
    color_match=re.search(r'[СсCc][ЕеEe][РрPp]', line)
    if color_match:
        return 'Серый'
    # find brown color
    color_match=re.search(r'[КкKk][ОоOo][РрPp]', line)
    if color_match:
        return 'Коричневый'
    # find black color
    color_match=re.search(r'[Чч][ЕеEeЁё][РрPp]', line)
    if color_match:
        return 'Черный'
    # find black color in English
    color_match=re.search(r'[Bb][Ll][Aa][Cc][Kk]', line)
    if color_match:
        return 'Черный'
    # find black color ( Assume that the oxidized screws is black)
    color_match=re.search(r'[ОоOo][КкKk][СсCc][Ии][Дд]', line)
    if color_match:
        return 'Черный'
    # find black color ( Assume that the oxidized screws is black) in English
    color_match=re.search(r'[ОоOo][XxХх][Ii][Dd]', line)
    if color_match:
        return 'Черный'
     # find black color ( Assume that the phosphated screws is black)
    color_match=re.search(r'[Фф][ОоOo][СсCc][Фф]', line)
    if color_match:
        return 'Черный'
    # find zink color
    color_match=re.search(r'[Цц][Ии][НнH]', line)
    if color_match:
        return 'Цинк'
    # find zink color in English
    color_match=re.search(r'[Zz][Ii]?[Nn]', line)
    if color_match:
        return 'Цинк'
    return 'None'

def create_output_string(line):
    """ The function receives an arbitrary string as input, and returns a 
    formatted one according to the requirements of the task.
    """
    size=size_define_parser(line[18:])
    return ','.join([line[:17], size[0], size[1], color_define_parser(line[18:]) + '\n'])
if __name__ == "__main__":
    # Getting the path to the file with information about the screws.
    input_file = get_file_path()
    # We will write the results to the out-attributes.csv file located in the
    # same folder as the original csv file with information about self-tapping
    # screws (samorezy.csv).
    output_file = sys.argv[0][:-10]+'out-attributes.csv'
    with open(input_file, encoding='utf-8') as f_input, open(output_file, mode='w', encoding='utf-8') as f_output:
        # Marking the columns of the output csv file
        f_output.write('id,Длинна,Диаметр,Цвет\n')
        for line in f_input:
            # This check was made to exclude from consideration the first line
            # of the input file "id,title".
            if len(line) < 17:
                continue
            f_output.write(create_output_string(line))
            
    