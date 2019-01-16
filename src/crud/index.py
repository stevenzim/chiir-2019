import config
from src import helper


def get_index():
    '''
    :return: return current global index
    '''
    index_dict = helper.load_json_from_file(config.INDEX_FILE)
    return index_dict[config.INDEX_KEY]


def update_index():
    '''
    :return: None
    Increments the index 1
    '''
    new_index = 1 + get_index()
    index_dict = helper.load_json_from_file(config.INDEX_FILE)
    index_dict[config.INDEX_KEY] = new_index
    return helper.dump_json_to_file(config.INDEX_FILE, index_dict)