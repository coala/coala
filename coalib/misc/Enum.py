def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    str_dict = enums.copy()
    enums['reverse'] = dict((value, key) for key, value in enums.items())
    enums['str_dict'] = str_dict

    return type('Enum', (), enums)
