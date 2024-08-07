class AlchemyDataObject:
    def __init__(self, keys, values):
        for key, value in zip(keys, values):
            setattr(self, key, value)
