


class ClientNumber():

    class __OnlyOne:
        def __init__(self):
            pass

    _instance = None
    def __init__(self):
        self.contNumber = 0
        if not self._instance:
            self._instance = ClientNumber.__OnlyOne()

    def getNumber(self):
        self.contNumber += 1
        return self.contNumber


