class CommonUtils:

    @staticmethod
    def tryFetch(jsonelement, attrlist:list):
        pointer = jsonelement
        for i in range(0, len(attrlist)):
            attr = attrlist[i]
            if pointer is None or len(pointer) == 0:
                return ''
            pointer = pointer[attr]
        return pointer
        pass
    pass