import sys
import pandas as pd


def hex_to_text(octet: str) -> str:
    """ Converts an octet-string into a string.

    NHot sure whether this is the correct method.

    Args:
        octet (str): octet string to convert

    Returns:
        str: converted string
    """
    s = ''
    i = 0
    while i < len(octet) - 1:
        # get a hexadecimal byte (two chars)
        hex_byte = octet[i:i+2]

        # convert to decimal
        t = 16 * int(hex_byte[0]) + int(hex_byte[1])
        
        # convert to character and add to string
        s += chr(t)

        # increase hex byte window by two
        i += 2

    # while

    return s

### hex_to_text ###


def read_p1_standard(filename: str) -> pd.DataFrame:
    """ Read a csv file with codes and descriptions into a pandas DataFrame.

    Args:
        filename (str): Namme of the csv file

    Returns:
        pd.DataFrame: DataFrame to be returned
    """
    df = pd.read_csv(filename, sep=';', keep_default_na=False, na_filter=False)
    
    return df

### read_p1_standard ###


def read_data(filename: str) -> list:
    """ read all lines of data file into a list of lines

    Args:
        filename (str): name of file to read

    Returns:
        list: list of lines
    """
    lines = open(filename, 'r').readlines()

    return lines

### read_data ###


def process_p1_log(devices: dict, lines: list, tst: str) -> dict:
    """ Process all lines into data messages

    Each data message starts with / and end with a !<crc code>. 
    This function puts each data message into a separate dictionary
    entry. The only guranteed unique identifier for a message is the time, 
    hence it is used as a unique identifier for a data message.

    Args:
        devices (dict): dictionary with device codes and other info
        lines (list): lines of the data file
        tst (str): time stamp (unique id)

    Returns:
        dict: dictionary of data messages
    """
    chunks = {}
    blok = []
    header_info = ''

    for line in lines:
        # each data message start with slash, initialize the datamessage
        if line[0] == '/':
            header_info = line[1:-1]
            blok = []
            id = ''

        # end of data message, create a new entry in the dictionary
        elif line[0] == '!':
            if len(id) > 0:
                chunks[id] = {}
                chunks[id]['header'] = header_info
                chunks[id]['time'] = id
                chunks[id]['data'] = convert_data_to_message(blok)
                chunks[id]['crc'] = line[1:-1]
                
                # zero blok and id
                blok = []
                id = ''

            else:
                print('*** couldn''t find valid ID for blok\n', blok)

            # if

        # None of the above, then it is a data line, append to blok
        else:
            blok.append(line)

        # if

        try:
            # if code is timestamp, find the stamo and assign to id
            code, data = line.split('(', 1)
            if code == tst:
                id = data.split(')')[0]

                # debug print id
                print(id)

        # ignore all other cases (usually empty line)
        except:
            pass

        # if
    # for

    return chunks

### process_p1_log ###


def convert_data_to_message(lines: list) -> list:
    """ convert lines of data into a list with (code, data) tuples

    Each line of data consists of some weird code followed by (data). hence
    '(' is used to check whether a line is data or not.

    Args:
        lines (list): lines of data

    Returns:
        list: list of tuples
    """
    data = []
    for line in lines:
        # is it data?
        if '(' in line:
            # split at first '('
            code, line = line.split('(', 1)

            # when there is string left a closing bracket must exist. remove
            if len(line) > 0:
                line = line[0:-2]

            # if

            # Add (code, data) tuple to data list
            data.append((code, line))

        # if

    # for

    return data

### process_data ###


if __name__ == "__main__":
    # main: mainly test code
    filename = "ini/p1-standard.csv"
    dataname = "data/ttylog.log"
    timestamp = '0-0:1.0.0'

    # read devices
    devices = read_p1_standard(filename)

    # and data
    data = read_data(dataname)

    # get data messages
    data_messages = process_p1_log(devices, data, timestamp)
    print(len(data_messages), 'data messages')

    # pick the first data message for further analysis
    key = list(data_messages.keys())[0]
    print(data_messages[key])

    # get the data and iterate over it
    data = data_messages[key]['data']
    for code, value in data:
        # test if code is device identification
        if code in['0-0:96.1.1', '0-1:96.1.0']:
            # if so, value is octet-string, convert it
            s = hex_to_text(value)

            # and print converted value
            print(code, '-->', s)
            
        # just print code and value
        else:
            print(code, value)

        # if

    # for

# if
