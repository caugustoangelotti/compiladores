MAKE_TREE = False

class MaqHipo:
    def __init__(self,_codArr) -> None:
        self.codArr = _codArr
        self.dataArr = []
        self.execMemory = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        self.s = 0
        self.i = 0
        self.stripCodArr()

    def stripCodArr(self):
        codeArr = []
        for code in self.codArr:
            codeArr.append(code.strip())
        self.codArr = codeArr

    def inpp(self):
        if MAKE_TREE:
            print('INPP')
        self.s = -1
        self.i += 1

    def crct(self, const):
        if MAKE_TREE:
            print('CRCT')
        self.s += 1
        self.execMemory[self.s] = float(const)
        #self.execMemory.append(const)
        self.i += 1

    def crvl(self, addr):
        if MAKE_TREE:
            print('CRVL')
        self.s += 1
        self.execMemory[self.s] = self.execMemory[addr]
        #self.execMemory[self.s] = self.dataArr[addr]
        self.i += 1

    def soma(self):
        if MAKE_TREE:
            print('SOMA')
        self.execMemory[self.s - 1]  = self.execMemory[self.s - 1] + self.execMemory[self.s]
        self.execMemory.pop(self.s)
        self.execMemory.pop(self.s - 1)
        self.s -= 1
        self.i += 1
    
    def subt(self):
        if MAKE_TREE:
            print('SUBT')
        self.execMemory[self.s - 1] = self.execMemory[self.s-1] - self.execMemory[self.s]
        self.s -= 1
        self.i += 1
    
    def mult(self):
        if MAKE_TREE:
            print('MULT')
        self.execMemory[self.s - 1] = self.execMemory[self.s-1] * self.execMemory[self.s]
        self.s -= 1
        self.i += 1

    def div(self):
        if MAKE_TREE:
            print('DIV')
        self.execMemory[self.s - 1] = self.execMemory[self.s-1] / self.execMemory[self.s]
        self.s -= 1
        self.i += 1
    
    def inve(self):
        if MAKE_TREE:
            print('INVE')
        self.execMemory[self.s] = - self.execMemory[self.s]
        self.i += 1
    
    def cpme(self):
        if MAKE_TREE:
            print('CPME')
        if self.execMemory[self.s - 1] < self.execMemory[self.s]:
            self.execMemory[self.s - 1] = 1.0
        else:
            self.execMemory[self.s - 1] = 0.0
        self.s -= 1
        self.i += 1
    
    def cpma(self):
        if MAKE_TREE:
            print('CPMA')
        if self.execMemory[self.s - 1] > self.execMemory[self.s]:
            self.execMemory[self.s - 1] = 1.0
        else:
            self.execMemory[self.s - 1] = 0.0
        self.s -= 1
        self.i += 1
    
    def cpig(self):
        if MAKE_TREE:
            print('CPIG')
        if self.execMemory[self.s - 1] == self.execMemory[self.s]:
            self.execMemory[self.s - 1] = 1.0
        else:
            self.execMemory[self.s - 1] = 0.0
        self.s -= 1
        self.i += 1
    
    def cdes(self):
        if MAKE_TREE:
            print('CDES')
        if self.execMemory[self.s - 1] != self.execMemory[self.s]:
            self.execMemory[self.s - 1] = 1.0
        else:
            self.execMemory[self.s - 1] = 0.0
        self.s -= 1
        self.i += 1
    
    def cpmi(self):
        if MAKE_TREE:
            print('CPMI')
        if self.execMemory[self.s - 1] <= self.execMemory[self.s]:
            self.execMemory[self.s - 1] = 1.0
        else:
            self.execMemory[self.s - 1] = 0.0
        self.s -= 1
        self.i += 1
    
    def cmai(self):
        if MAKE_TREE:
            print('CMAI')
        if self.execMemory[self.s - 1] >= self.execMemory[self.s]:
            self.execMemory[self.s - 1] = 1.0
        else:
            self.execMemory[self.s - 1] = 0.0
        self.s -= 1
        self.i += 1
    
    def armz(self, addr):
        if MAKE_TREE:
            print('ARMZ')
        #self.dataArr[addr] = self.execMemory[self.s]
        self.execMemory[addr] = self.execMemory[self.s]
        self.s -= 1
        self.i += 1
    
    def dsvi(self,addr):
        if MAKE_TREE:
            print('DSVI')
        self.i = addr
    
    def dsvf(self,addr):
        if MAKE_TREE:
            print('DSVF')
        if self.execMemory[self.s] == 0.0:
            self.i = addr
            self.s -= 1
        else:
            self.i += 1
    
    def leit(self):
        if MAKE_TREE:
            print('LEIT')
        self.s += 1
        #self.execMemory.append(float(input()))
        self.execMemory[self.s] = float(input())
        self.i += 1

    def impr(self):
        if MAKE_TREE:
            print('IMPR')
        print(self.execMemory[self.s])
        self.s -= 1
        self.i += 1
    
    def alme(self):
        if MAKE_TREE:
            print('ALME')
        self.s += 1
        self.execMemory.append(0.0)
        self.dataArr.append(0.0)
        self.i += 1
    
    def para(self):
        if MAKE_TREE:
            print('PARA')
        exit()
    
    def getNextInstruction(self):
        return self.codArr[self.i]

    def getCurrentInstruction(self):
        return self.codArr[self.i]

    def getInstructionByAddr(self,addr):
        return self.codArr[addr]

    def execCode(self):
        while not self.getNextInstruction() == 'PARA':
            if ' ' in self.getCurrentInstruction():
                instruction, arg = self.getCurrentInstruction().split(' ')
                if not arg == '0.0':
                    arg = int(arg)
            else:
                instruction = self.getCurrentInstruction()

            if instruction == 'INPP':
                self.i += 1
            elif instruction == 'CRCT':
                self.crct(arg)
            elif instruction == 'CRVL':
                self.crvl(arg)
            elif instruction == 'SOMA':
                self.soma()
            elif instruction == 'SUBT':
                self.subt()
            elif instruction == 'MULT':
                self.mult()
            elif instruction == 'DIV':
                self.div()
            elif instruction == 'INVE':
                self.inve()
            elif instruction == 'CPME':
                self.cpme()
            elif instruction == 'CPMA':
                self.cpma()
            elif instruction == 'CPIG':
                self.cpig()
            elif instruction == 'CDES':
                self.cdes()
            elif instruction == 'CPMI':
                self.cpmi()
            elif instruction == 'CMAI':
                self.cmai()
            elif instruction == 'ARMZ':
                self.armz(arg)
            elif instruction == 'DSVI':
                self.dsvi(arg)
            elif instruction == 'DSVF':
                self.dsvf(arg)
            elif instruction == 'LEIT':
                self.leit()
            elif instruction == 'IMPR':
                self.impr()
            elif instruction == 'ALME':
                self.alme()