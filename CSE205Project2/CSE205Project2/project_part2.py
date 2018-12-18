from multiprocessing import Process
import threading
import time
import os
import re
import socket
import sys
def clientsever(x,i,G):                          
    host="127.0.0.1"
    port=i+1998
    string1=''
    for w in G:
        string1=string1+str(w)+' '
    string1=string1+' '+str(x)
    nodeclient=socket.socket()
    nodeclient.connect((host,port))
    result=nodeclient.recv(1024).decode()
    #print('client: '+str(x)+'   '+result+'\n')
    nodeclient.sendall(string1.encode())
    file=open('Node '+str(x)+'.txt','a+')
    file.write(result+'\n')
    file.close()
    nodeclient.close()
def sever(x):
    host="127.0.0.1"
    port=x+1998
    node=socket.socket()
    node.bind((host,port))
    node.listen(50)
    while True:
        file1=open('Node final'+str(x)+'.txt','r')
        temp=file1.readlines()
        for i in temp:
            i=i.strip()
            string=i
        file1.close()
        connectionSocket,addr=node.accept()
        connectionSocket.sendall(string.encode())
        result=connectionSocket.recv(1024).decode()
        #print('sever:  '+str(x)+ '  '+string+'\n')
        file=open('Node '+str(x)+'.txt','a+')
        file.write(result+'\n')
        file.close()
        connectionSocket.close()
    
def Node(x,s):
    file=open('Node '+str(x)+'.txt','a')
    file.close()
    file1=open('Node final'+str(x)+'.txt','w')
    thread=[]
    Neb=[]
    string=''
    const=len(s)
    #print(const)
    S=s[x-1]
    for i in S:
        string=string+str(i)+' '
        if (i!=0)&(i!=50000):
            temp=S.index(i)+1
            Neb.append(temp)
    string=string+' '+str(x)
    file1.write(string)
    file1.close()
    P1=threading.Thread(target= sever, args=(x,))
    P1.start()
    time.sleep(1)
    DV=[]
    b=0
    while b<const:
        time.sleep(2)
        if s[x-1]==DV:
            print('Node '+str(x)+' is done' )
        if s[x-1]!=DV:
            #print(str(x)+'     true')
            DV=[]
            for i in s[x-1]:
                DV.append(i)
            for i in Neb:
                if x>0:
                    p1=threading.Thread(target=clientsever, args=(x,i,DV))
                    thread.append(p1)
            for i in thread:
                i.start()
            for i in thread:
                i.join()
        flie=open('Node '+str(x)+'.txt','r')
        flash=flie.readlines()
        total=[]
        for i in flash:
            i=i.strip()
            temp=[]
            temp=i.split()
            total.append(temp)
        for i in total:
            temp1=[]
            for w in i:
                temp1.append(int(w))
            ls=len(temp1)
            identy1=temp1[ls-1]
            temp1.pop()
            s[identy1-1]=temp1
                #if x==1:
                  #print(identy1)
                  #print(s[identy1-1])
                  #print(s[x-1])
            copy=[]
            for h in s[x-1]:
                copy.append(h)
            for f in copy:
                fuck=copy.index(f)
                copy[fuck]=0
                #if x==1:
                    #print('index:   '+str(fuck))
                distance=s[identy1-1][fuck]+s[x-1][identy1-1]
                if f>distance:
                    s[x-1][fuck]=distance
        file2=open('Node final'+str(x)+'.txt','w')
        string2=''
        for i in S:
            string2=string2+str(i)+' '
        string2=string2+' '+str(x)
        file2.write(string2)
        file2.close()
        thread=[]
        b+=1
        time.sleep(3)
        print(str(x)+' :    ',s[x-1])
        time.sleep(0.2)
if __name__ == '__main__':
    temp0=[]
    tempx=[]
    file=open(sys.argv[1],'r')
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
    G = [[50000] * const for _ in range(const)]
    for i in range(n):
            G[i][i]=0
    file1=open(sys.argv[1],'r')
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
    t=[]
    for i in range(len(G)):
        A = [[50000] * const for _ in range(const)]
        A[i]=G[i]
        p1=Process(target=Node, args=(i+1,A))
        t.append(p1)
    for i in t:
        i.start()

    
    
