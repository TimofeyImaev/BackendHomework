class Super:
    publicData = "Public Data Member"
    _protectedData = "Protected Data Member"
    __privateData = "Private Data Member"

    def accessPrivateMembers(self):
        print("Accessing inside class:", self.__privateData)


class Sub(Super):
    def accessProtectedMembers(self):
        print("Accessing inside subclass:", self._protectedData)

obj = Sub()

# Public → Direct Access
print(obj.publicData)

# Protected → Accessible (but discouraged)
print(obj._protectedData)

# Private → Not directly accessible
# print(obj.__privateData) AttributeError
obj.accessPrivateMembers()

# Using Name Mangling
print(obj._Super__privateData)

