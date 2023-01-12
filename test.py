class A:
    def name(self):
        return self.__class__.__name__

class B(A):
    pass

b = B()

a = A()

print(b.name())
print(a.name())