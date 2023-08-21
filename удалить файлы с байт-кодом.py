'''
Удаляет все файлы с байт кодом 
Это те что с разрешением .pyc
'''
import sys,os
findonly = False
rootdir = os.getcwd() if len(sys.argv)==1 else sys.argv()[1] #получает верхин каталог,если нет то испольет нынещный

found = removed = 0
for (thisDir,subsHere,filesHere) in os.walk(rootdir):
    for file in filesHere:
        if file.endswith('.pyc'):
            fullpath = os.path.join(thisDir,file)
            print('=>',fullpath)
            found+=1
            if not findonly:
                try:
                    os.remove(fullpath)
                except:
                    print('Error')
                    print(sys.exc_info()[0],sys.exc_info()[1])
                else:
                    removed+=1 
print('Found',found,'\n','files, removed',removed)

#еще для простоты можно использовать модуль find которую мы написали и сделать намного короче
'''
import find
for file in find.find('*pyc',rootdir): 
    print('=>',file)
    os.remove(file)
    count+=1
'''