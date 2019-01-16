import json
import datetime

import uuid


def get_uuid():
    return str(uuid.uuid4())


def get_time_stamp():
    """
    :return: Timestamp in format: 2014-10-18 21:31:12
    """
    return '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())



def extract_target_values(sequence, target_field):
    """
    :param sequence: A list or list of dictionaries or other list
    :param target_field: If data nested in listed, then mapping to find the target val 
    e.g. key_name or element number of nested tuple
    :return: return a sequence of numerics to be passed into stats function
    """
    if target_field is None:
        try:
            return sequence
        except ValueError as err:
            print(err)
            raise Exception("Ensure target field is specified OR perhaps your sequence is not a numeric")
    else:
        try:
            return [float(element[target_field]) for element in sequence]
        except ValueError as err:
            print(err)
            raise Exception("Ensure target field occurs in all Elements of Sequence ")


def load_json_from_file(file_name):
    """
    Loads JSON data into list.  Returns a list of dictionaries in [{},{}...{}] format
    fileName is relative to directory where Python is running.
    usage: myListOfDicts = load_json_from_file("FileName") 
    :param file_name: 
    :return: 
    """
    #return json.loads(unicode(open(fileName).read(), "ISO-8859-1"))
    return json.loads(open(file_name).read())

def dump_json_to_file(file_name, data_to_dump):
    """Dumps JSON data from dictionaries in list into output file. This data is pretty printed
    for readability. fileName is relative to directory where Python is running.
    dataToDump should be in [{},{}...{}] format
    usage: dumpJSONtoFile("FileName", myListOfDicts)"""
    with open(file_name, 'w') as outfile:
        json.dump(data_to_dump, outfile, sort_keys=True, indent=4, separators=(',', ': '))



