from hashlib import sha1
import pickle


def persistent_hash(obj):
    """
    Calculates a persistent hash of the given object.

    This hash method uses pickle (protocol 4) to serialize the given object and
    hash the byte-stream. The hashing algorithm used is SHA-1.

    :param obj:
        The object to calculate the persistent hash for.
    :return:
        The persistent hash.
    """
    fingerprint_generator = sha1()
    fingerprint_generator.update(pickle.dumps(obj, protocol=4))
    return fingerprint_generator.digest()
