import logging
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from coalib.bearlib import aspects

VALID_ROOT_ASPECTS = ['Formatting', 'Metadata', 'Redundancy', 'Security',
                      'Smell', 'Spelling']


def find_leaf_aspect(capabilities, message):
    leaf_aspect = None
    root_aspects = get_valid_aspects(capabilities)
    for aspect in root_aspects:
        leaf_aspect = get_leaf_aspect_for(aspect, message)
        if leaf_aspect is not None:
            break
    return leaf_aspect


def get_valid_aspects(capabilities):
    invalid_aspects = []
    valid_capabilities = list(capabilities)
    for capability in capabilities:
        if capability not in VALID_ROOT_ASPECTS:
            invalid_aspects.append(capability)
            valid_capabilities.remove(capability)
    if invalid_aspects.__len__() > 0:
        logging.warning('Invalid aspects provided - {}'
                        .format(', '.join(invalid_aspects)))
        if len(valid_capabilities) == 0:
            logging.warning('No valid aspects found. Setting aspect=None')
        return valid_capabilities
    return valid_capabilities


def get_leaf_aspect_for(root_aspect, message):
    # Lemmatize words in message
    lemmatizer = WordNetLemmatizer()
    message = message.lower()
    message = message.replace('.', '')
    message = message.split()
    lem_message = [lemmatizer.lemmatize(word)
                   for word in message
                   if word not in set(stopwords.words('english'))]
    # Find leaf-aspect
    aspect_instance = aspects[root_aspect]
    leaf_aspects = (aspect_instance
                    .get_leaf_aspects
                    .func
                    .__call__(aspect_instance))
    possible = []
    for leaf in leaf_aspects:
        lem_message_word = []
        class_name = str(leaf).split('.')[-1].replace('\'>', '')
        split_class_name = re.findall('[A-Z][a-z]+', class_name)
        split_class_name = [_.lower() for _ in split_class_name]
        for word in lem_message:
            if word in split_class_name and word not in lem_message_word:
                lem_message_word.append(word)
        if (len(lem_message_word) >= len(split_class_name) / 2 and
                leaf not in possible):
            possible.append(class_name)

    if len(possible) > 0:
        return (aspects[possible[0]])('Unknown')
    return None
