class Character:
    def __init__(self,Hp,MaxHp,Sp,MaxSp,Str,Def,Lvl,Exp,Money,Fights):
        self.__Hp=Hp
        self.__Sp=Sp
        self.__MaxHp=MaxHp
        self.__MaxSp=MaxSp
        self.__Str=Str
        self.__Def=Def
        self.__Lvl=Lvl
        self.__Exp=Exp
        self.__Money=Money
        self.__Fights=Fights
        
        
    def getHp(self):
        return self.__Hp  
    def setHp(self,Hp):
        self.__Hp=Hp
        
        
    def getSp(self):
        return self.__Sp   
    def setSp(self,Sp):
        self.__Sp=Sp
        
        
    def getMaxHp(self):
        return self.__MaxHp   
    def setMaxHp(self,MaxHp):
        self.__MaxHp=MaxHp
        
        
    def getMaxSp(self):
        return self.__MaxSp    
    def setMaxSp(self,MaxSp):
        self.__MaxSp=MaxSp
        
        
    def getStr(self):
        return self.__Str    
    def setStr(self,Str):
        self.__Str=Str
        
        
    def getDef(self):
        return self.__Def    
    def setDef(self,Def):
        self.__Def=Def
        
        
    def getLvl(self):
        return self.__Lvl   
    def setLvl(self,Lvl):
        self.__Lvl=Lvl
        
        
    def getExp(self):
        return self.__Exp   
    def setExp(self,Exp):
        self.__Exp=Exp

    def getMoney(self):
        return self.__Money   
    def setMoney(self,Money):
        self.__Money=Money        
        

    def getFights(self):
        return self.__Fights
    def setFights(self,Fights):
        self.__Fights=Fights
    def fight(self):
        self.__Fights -= 1
    
        
    
    def restore(self):
        self.__Hp = self.__MaxHp
        self.__Sp = self.__MaxSp
        self.__Fights = 20
        
        
        
class Enemy:
    def __init__(self,Name,Hp,MaxHp,Str,Def,Exp,Money,AIType):
        self.__Name=Name
        self.__Hp=Hp
        self.__MaxHp=MaxHp
        self.__Str=Str
        self.__Def=Def
        self.__Exp=Exp
        self.__Money=Money
        self.__AIType=AIType
        
        
    def getHp(self):
        return self.__Hp
    def setHp(self,Hp):
        self.__Hp=Hp

        
    def getMaxHp(self):
        return self.__MaxHp   
    def setMaxHp(self,MaxHp):
        self.__MaxHp=MaxHp

        
    def getName(self):
        return self.__Name
    def setName(self,Name):
        self.__Name=Name
        
        
    def getStr(self):
        return self.__Str
    def setStr(self,Str):
        self.__Str=Str
        
        
    def getDef(self):
        return self.__Def
    def setDef(self,Def):
        self.__Def=Def
        
        
    def getExp(self):
        return self.__Exp
    def setExp(self,Exp):
        self.__Exp=Exp
        
        
    def getMoney(self):
        return self.__Money   
    def setMoney(self,Money):
        self.__Money=Money  
        
    def getAIType(self):
        return self.__AIType
    def setAIType(self,AIType):
        self.__AIType=AIType
        
        
        
class Item:
    def __init__(self, name, value):
        self.__value=value
        self.__name=name
        
    def getName(self):
        return self.__name
    def setName(self,Name):
        self.__name=name
        
    def getValue(self):
        return self.__value
    def setValue(self,value):
        self.__value=value
        
    def getEffIndex(self):
        return 0
        
    def dumpInfo(self):
        dumpString = "Item\n" + self.getName() + "\n" + str(self.getValue()) + "\n"
        return dumpString
    
        
class Weapon(Item):
    def __init__(self,name,value,mod):
        Item.__init__(self,name,value)
        self.__mod=mod
        
    def getMod(self):
        return self.__mod 
    def setMod(self,mod):
        self.__mod=mod
        
    def dumpInfo(self):
        dumpString = "Weapon\n" + self.getName() + "\n" + str(self.getValue()) + \
                   "\n" + str(self.__mod) + "\n"
        return dumpString
        

        
class Armor(Item):
    def __init__(self,name,value,mod):
        Item.__init__(self,name,value)
        self.__mod=mod
        
    def getMod(self):
        return self.__mod
    def setMod(self,mod):
        self.__mod=mod
        
    def dumpInfo(self):
        dumpString = "Armor\n" + self.getName() + "\n" + str(self.getValue()) + \
                   "\n" + str(self.__mod) + "\n"
        return dumpString


class Consumable(Item):
    def __init__(self,name,value,effIndex):
        Item.__init__(self,name,value)
        self.__effIndex=effIndex
        
    def getEffIndex(self):
        return self.__effIndex
    def setEffIndex(self,effIndex):
        self.__effIndex=effIndex
        
    def dumpInfo(self):
        dumpString = "Consumable\n" + self.getName() + "\n" + str(self.getValue()) + \
                   "\n" + str(self.__effIndex) + "\n"
        return dumpString

class Drug:
    def __init__(self,name,price,desc):
        self.__name=name
        self.__price=price
        self.__desc=desc
        
    def getName(self):
        return self.__name
    def setName(self,name):
        self.__name=name
        
    def getPrice(self):
        return self.__price
    def setPrice(self,price):
        self.__price=price
        
    def getDesc(self):
        return self.__desc
    def setDesc(self,desc):
        self.__desc=desc