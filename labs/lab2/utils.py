
class Utils:
    @staticmethod
    def dict_is_empty(dictionary: dict):
        for values in dictionary.values():
            if values:
                return False
        return True
