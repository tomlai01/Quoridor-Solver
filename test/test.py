from src.Exceptions import IllegalPlayException
from src.SmartPlayer import SmartPlayer
from src.State import State
from copy import copy

class A:

    def __init__(self):
        self.n = 1
        self.l = [1, 2]
        self.s = set()
        self.t = [(1,2)]

    def __copy__(self):
        copy = A()
        copy.l = self.l
        copy.s = self.s
        copy.t = self.t
        copy.n = self.n
        return copy


    def __str__(self):
        return str(self.n)+str(self.l)+str(self.s)+str(self.t)

a = A()
copy = copy(a)
copy.n=0
copy.l[0] = 0
copy.s.add((3,4))
copy.t[0] = (3,4)

print(a)
print(copy)


