class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def dict_to_lower(dict):
    new_dict = {}
    for key, value in dict.iteritems():
        new_key = key[0].lower() + key[1:]
        new_dict[new_key] = value
    return new_dict