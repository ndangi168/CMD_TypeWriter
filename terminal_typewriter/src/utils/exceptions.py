class TypewriterException(Exception):
    pass


class DisplayException(TypewriterException):
    pass


class StorageException(TypewriterException):
    pass


class InputException(TypewriterException):
    pass