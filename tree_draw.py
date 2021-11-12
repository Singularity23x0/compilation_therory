class Node:
    def __init__(self,value,leafs):
        self.value = value
        self.leafs = leafs

    def draw(self,file=""):
        if file!="":
            f = open(file,"wb")
        s,T = self.getLower()
        for x in T:
            if file != "":
                f.write(x.encode("utf8"))
                f.write("\n".encode("utf8"))
            else:
                print(x)
        if file!="":
            f.close()

    def getLower(self):
        if self.leafs is None:
            connect = ""
            return len(str(self.value)),[str(self.value)]
        else:
            connect = "╠"
            LR=[]
            st=0
            ls=0
            for l in self.leafs:
                s,T = l.getLower()
                st+=s
                ls=s
                LR.append(T)
                connect+="═"*s+"╦"
            connect=connect[:-ls-2]
            if len(self.leafs)==1:
                connect += "║" + " " * (ls - 1)
            else:
                connect+="╗"+" "*(ls-1)
            st+=len(self.leafs)-1
            if len(connect)<len(str(self.value)):
                connect+=" "*(len(str(self.value))-len(connect))
            T = [str(self.value)+" "*(st-len(str(self.value))),connect]
            k=0
            if st<len(str(self.value)):
                k=len(str(self.value))-st
            T+=self.merge(LR,k)
            return max(st,len(str(self.value))),T

    def merge(self,T,k):
        m=0
        for x in T:
            m=max(m,len(x))
        for x in T:
            if len(x)<m:
                x+=([" "*len(x[0])]*(m-len(x)))
        T2=[""]*m
        for i in range(m):
            for x in T:
                T2[i]+=x[i]+" "
            T2[i]=T2[i][:-1]+" "*k
        return T2


def main():
    tree=Node("100",[Node("200",[Node("01",[Node("0",None)]),Node("0",None),Node("3",[Node("2",[Node("1",[Node("2",[Node("2",None),Node("3",[Node("2",None)])]),Node("3",[Node("2",None)])])])])]),Node("3",[Node("2",None)])])
    tree.draw()


if __name__ == "__main__":
    main()

