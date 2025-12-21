import random,time,math
from tkinter import *
from decimal import Decimal,getcontext
from datetime import *
getcontext().prec=50
pi=Decimal(3.141592653589793238462643383279502884197169399375105820974944592307816406286)
#_____Custom exceptions_____
class LogicalError(Exception):
    """class for errors in logic"""
    def __init__(self, message='', errors=None):            
        super().__init__(message)
        self.errors = errors
class ForError(Exception):
    """
    Error for for cycles
    """
    def __init__(self, message='', errors=None):            
        super().__init__(message)
        self.errors = errors
class HungerError(Exception):
    """class for errors in Cat.hunger and Cat.calculateHunger()"""
    def __init__(self, message='', errors=None):            
        super().__init__(message)
        self.errors = errors
#_____Classes for object creating_____
class Everything:
    def __contains__(self,a):
        return True
    def __str__(self):
        return "Everything" 
class Quenue:
    def __init__(self,lst):
        self.lst=lst
    def enqueue(self,i):
        self.lst.append(i)
    def dequeue(self):
        return self.lst.pop(0)
    def peek(self):
        return self.lst[0]
    def isempty(self):
        return not bool(self.lst)
    def size(self):
        return len(self.lst)
    def __len__(self):
        return len(self.lst)
    def __str__(self):
        return str(self.lst)
class Stack:
    def __init__(self,lst):
        self.lst=lst
    def push(self,i):
        self.lst.insert(0,i)
    def pop(self):
        return self.lst.pop(0)
    def peek(self):
        return self.lst[0]
    def isempty(self):
        return not bool(self.lst)
    def size(self):
        return len(self.lst)
    def __len__(self):
        return len(self.lst)
    def __str__(self):
        return str(self.lst)
class Cat:
    def __init__(self,name):
        self.name=name
        if "dog" in self.name.lower():
            print(LogicalError("a cat is not a dog"))
        self.age=0
        self.hunger=10.0
        self.lastate=datetime.now()
    def __str__(self):
        return f" A_A{"".join([" "]*(len(self.name)+2))}//\n(>-<){"".join(["_"]*(len(self.name)))}//\n|–––{self.name}//\n//{"".join(["–"]*(len(self.name)+3))}\\\\"
    def calculateHunger(self):
        datetime.now()-self.lastate
        self.hunger+=float(str(datetime.now()-self.lastate).split()[-1].split(":")[2])*2
        self.hunger+=float(str(datetime.now()-self.lastate).split()[-1].split(":")[1])*120
        self.hunger+=float(str(datetime.now()-self.lastate).split()[-1].split(":")[0])*7200
        return self.hunger
    def eat(self):
        self.calculateHunger()
        self.hunger-=60
        if self.hunger<=0:
            self.hunger=0
            raise HungerError("")
    def __add__(self,other):
        return Cat(self.rename())
    def __sub__(self,other):
        return random.choice([self,other])
    def __bool__(self):
        return True
    def __len__(self):
        return len(self.name)
    def __call__(self,a):
        c=Cat(str(a))
        c.age+=1
        return c
    def get_older(self):
        self.age+=1
    @staticmethod
    def newname():
        from random import choice
        n0 = choice(["Транс", "Пан", "Пост", "Сверх", "Пред", "Не "])
        n1 = choice(["торт", "рыж", "барс", "угол", "пуш", "прокис", "кис", "кот"])
        if n1[-1] == "ш" or n1[-1] == "щ" or n1[-1] == "ж":
            n2 = choice(["ун", "ыш", "ик", "атина", "ок", "ик", "онак", "ка", "сон", "он"])
        else:
            n2 = choice(["ун", "ыш", "ик", "ятина", "ёк", "чик", "ёнак", "очек", "ка", "сон", "он"])
        return n0 + n1 + n2
    @staticmethod
    def kus():
        root=Tk()
        root.geometry("200x300")
        root.title('Mod')
        Label(text="Kusnul tebya!").pack()
        mainloop()
class List:
    def __init__(self,a=''):
        self.lst=tuple(a)
    def append(self,a):
        self.a=self.lst
        self.lst=self.a+(a,)
    def __getitem__(self,i:int):
        return self.lst[i]
    def __setitem__(self,k:int,w):
        self.lst[:k]+w+self.lst[k+1:]
    def pop(self,k:int):
        t=self.lst[k]
        self.lst=self.lst[:k]+self.lst[k+1:]
        return t
    def clear(self):
        self.lst=[]
    def reverse(self):
        self.lst=self.lst[::-1]
    def count(self,a):
        return self.lst.count(a)
    def insert(self,k:int,w):
        self.lst=self.lst[:k]+(w,)+self.lst[k:]
    def index(self,w):
        if w in self.lst:
            a=0
            while self.lst[a]!=w:
                a+=1
        else:
            raise(IndexError(f" where is no element {w} in this Listtuple"))
        return a
    def __call__(self):
        return self.lst
    def remove(self,w):
        if w in self.lst:
            a=0
            while self.lst[a]!=w:
                a+=1
        else:
            raise(IndexError(f" where is no element {w} in this Listtuple"))
        self.lst=self.lst[:a]+self.lst[a+1:]
    def extend(self,l):
        for i in l:
            self.lst=self.lst+(i,)
    def copy(self):
        return self.lst
    def sort(self):
        self.lst=tuple(sorted(self.lst))
    def __str__(self):
        return str(self.lst)
    def __bool__(self):
        return bool(self.lst)
    def __len__(self):
        return len(self.lst)
    def __eq__(self, value):
        if type(value)==type(List):
            return self.lst == value.lst
        else:
            return self.lst == value
    def __lt__(self,other):
        return len(self)<len(other)
    def __gt__(self,other):
        return len(self)>len(other)
    def __repr__(self):
        return f"lt({self.lst})"
    def __contains__(self,a):
        return a in self.lst    
    def __reversed__(self):
        return list(self.lst[::-1])
    def __sorted__(self):
        return sorted(self.lst)
    def __iter__(self):
        self.iter=0
        return self
    def __next__(self):
        if self.iter<len(self.lst):
            self.a=self.iter
            self.iter+=1
            return self.lst[self.a]
        else:
            raise(StopIteration)
    def __index__(self):
        return self.lst[0]
    def __delitem__(self,k):
        self.lst=self.lst[:k]+self.lst[k+1:]
    def __invert__(self):
        return self.lst[::-1]
class Table:
    def __init__(self):
        self.__lst=[]
    def __getitem__(self,y):
        return self.__lst[y]
    def __setitem__(self,key,val):
        self.__lst[key]=list(val)
    def sett(self,x,y,a):
        self.__lst[y][x]=a
    def insert(self,x,y,a):
        self.__lst[y].insert(x,a)
    def addy(self):
        self.__lst.append([])
    def addx(self,a=None):
        for i in range(len(self.__lst)):
            self.__lst[i].append(a)
    def __str__(self):
        return "-"+"–"*(len(", ".join([str(g) for g in self.__lst[0]])))+"-\n"+"\n".join(["|"+", ".join([str(g) for g in i])+"|" for i in self.__lst])+"\n-"+"–"*(len(", ".join([str(g) for g in self.__lst[0]])))+"-"
    def get(self):
        return self.__lst
    def append(self,k,w=None):
        self.__lst[k].append(w)
    def print(self):
        print("-"+"–"*(len(", ".join([str(g) for g in self.__lst[0]])))+"-")
        for i in self.__lst:
            print("|"+", ".join([str(g) for g in i])+"|")
        print("-"+"–"*(len(", ".join([str(g) for g in self.__lst[0]])))+"-")
    def __len__(self):
        return len(self.__lst)
class Hashlist:
    def __init__(self):
        self.hlist=[None]*10000000
    def __getitem__(self,i):
            return self.hlist[i]
    @staticmethod
    def hash(a):
        return(sum([(ord(a[i])**(i+1))**(3+i) for i in range(len(a))])%10000000)
    def add(self,a,b=None):
            if b==None:
                b=a
            self.hlist[sum([(ord(a[i])**(i+1))**(3+i) for i in range(len(a))])%10000000]=b
    def update(self,a):
        for i in a:
            self.add(i)
    def clear(self):
        self.hlist=[None]*10000000
    def __str__(self):
        return str([i for i in self.hlist if i!=None])
    def __call__(self):
        return [i for i in self.hlist if i!=None]
    def __len__(self):
        return len([i for i in self.hlist if i!=None])
    def __iter__(self):
        self.iter=0
        return self
    def __next__(self):
        if self.iter<len(self.lst):
            self.a=self.iter
            self.iter+=1
            return self.lst[self.a]
        else:
            raise(StopIteration)
#_____Classes for grouping methods_____
class MOD:
    def __str__(self):
        return "Calculator"
    @staticmethod
    def comb(a, b):
        """Combines 2 sorted lists in to a sorted list"""
        c = []
        a1 = 0
        b1 = 0
        while a1 < len(a) and b1 < len(b):
            if a[a1] < b[b1]:
                c.append(a[a1])
                a1 += 1
            else:
                c.append(b[b1])
                b1 += 1
        if b1 < len(b):
            c+=b[b1:]
        else:
            c+=a[a1:]
        return c
    @staticmethod
    def analyse(a):
        a1 = a.count(",")
        a2 = a.count(".")
        a3 = a.count("!")
        a4 = a.count("?")
        if a1 > a2 and a1 > a3 and a1 > a4:
            r1=","+str(a1)
        elif a2 > a1 and a2 > a3 and a2 > a4:
            r1="."+str(a2)
        elif a3 > a1 and a3 > a2 and a3 > a4:
            r1="!"+str(a3)
        elif a4 > a1 and a4 > a2 and a4 > a3:
            r1="?"+str(a4)
        else:
            r1=""
        return ((len(a)) + 1) - (a1 + a2 + a3),r1
    @staticmethod
    def remove(a,removed):
        k=0
        while k in range(len(a)):
            if a[k]==removed:
                a.pop(k)
            else:
                k+=1
        print(a)
    @staticmethod
    def getmrow(l=4):
        return "M"+"".join([random.choice(["a","y","o","w","e","r"]) for _ in range(l-1)])
    @staticmethod
    def factorial(a):
        fact = lambda a3: 1 if a3 == 0 else fact(a3 - 1) * a3
        return fact(a)
    @staticmethod
    def counter(a):
        s = {}
        for i in a.split():
            if i in s:
                s[i] += 1
            else:
                s.setdefault(i, 1)
        return s
    @staticmethod
    def short(a):
        short=a[0]
        w=1
        while w<=len(a)-1 or  not a[w] in ["a","e","u","i","o"]:
            short+=a[w]
            if a[w] in ["a","e","u","i","o"]:
                break
            w+=1
        if len(short) < 3 < len(a):
            return short + "_"+a[-2]+a[-1]
        elif 3 < len(a):
            return short+"_"+a[-1]
        else:
            return a
    @staticmethod
    def timer(f):
        def w(*args,**kwargs):
            st=time.time()
            r=f(*args,**kwargs)
            stt=time.time()
            print(f"{str(f).split()[1]} were executed for {(stt-st):.2f} seconds")
            return r
        return w
    @staticmethod
    def getprogressbar(progress:int,l:int=50,sym1:str='#',sym2:str='='):
        return ''.join([sym1]*math.floor(progress/100*l))+''.join([sym2]*(l-math.floor(progress/100*l)))
def paralel(*args):
    import asyncio,datetime
    print(datetime.datetime.now())
    async def say_after(what):
        exec(str(what))
    async def main(a):
        async with asyncio.TaskGroup() as tg:
            tasks=[tg.create_task(say_after(str(i))) for i in a]
        for i in tasks:
            await i
    print(datetime.datetime.now())
    asyncio.run(main(args))
#_____Functions_____
def consoleclear():
    print("\033c",end="")
