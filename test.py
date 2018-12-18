import os
import re
import sys
def linkstate(filename):
    temp0=[]
    tempx=[]
    file=open(filename,'r')
    temp=file.readlines()
    for i in temp:
        i=i.strip()
        matchtemp=re.findall('Node',i)
        if len(matchtemp):
            temp1=i.split()
            temp0.append(temp1[1])
        else:
            temp2=i.split()
            temp0.append(temp2[0])
    file.close()
    temp3=list(set(temp0))
    n=len(temp3)
    const=n
    temp4=n+1
    G = [[50000] * n for _ in range(n)]
    for i in range(n):
        G[i][i]=0
    n=0
    file1=open(filename,'r')
    temp5=file1.readlines()
    for i in temp5:
        i=i.strip()
        matchtemp=re.findall('Node',i)
        if len(matchtemp):
            temp1=i.split()
            n=int(temp1[1])-1
        else:
            temp2=i.split()
            a=int(temp2[0])-1
            b=int(temp2[1])
            G[n][a]=b
            G[a][n]=b
    file1.close()
    print('The adjacent matrix is: \n')
    print(G)
    print('\n')
    for h in range(const):
        sourcecode=h+1
        path={sourcecode:str(sourcecode)+'->'+str(sourcecode)}
        presentco={sourcecode:0}
        temppresentco={sourcecode:0}
        S=[]
        Nodes=[i+1 for i in range(const)]
        Nodes.remove(sourcecode)
        S.append(sourcecode)
        for i in Nodes:
            temppresentco[i]=G[sourcecode-1][i-1]
            presentco[i]=G[sourcecode-1][i-1]
            path[i]=str(sourcecode)+'->'+str(i)
        del temppresentco[sourcecode]
        while Nodes:
            q=min(temppresentco, key=temppresentco.get)
            del temppresentco[q]
            S.append(q)
            Nodes.remove(q)
            for i in Nodes:
                temp=presentco[q]+G[q-1][i-1]
                if presentco[i]>temp:
                    presentco[i]=temp
                    temppresentco[i]=temp
                    path[i]=path[q]+'->'+str(i)
        file=open('result.txt','a')
        file.write('The minimum cost form '+str(sourcecode)+' to each point are shown blow\n')
        for i in S:
            file.write('From '+str(sourcecode)+' to '+str(i)+' :'+str(presentco[i])+'      The path is:'+path[i]+'\n')
        file.write('\n')
        file.close()
        print('The minimum cost from source node ' +str(sourcecode)+' is found')
# linkstate('nodeExample1.txt')

linkstate(sys.argv[1])



