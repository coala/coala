def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    enums['reverse'] = dict((value, key) for key, value in enums.items())

    return type('Enum', (), enums)
