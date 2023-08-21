import glob,os,sys
#сортировка по байтам в указоным каталоге
'''
dirname = r'C:Users\\User' if len(sys.argv)==1 else sys.argv[1] #если в этом пути будут файлы с расширение .py
                                                                #то тогда булет работать
allsizes = []
apply = glob.glob(dirname+os.sep+'*py') 
for file in apply:
    filesize = os.path.getsize(file) #получить размер файла в байтах
    allsizes.append(filesize,file)
allsizes.sort()
print(allsizes[:2]) #[0,1]
print(allsizes[-2:]) #[-2,-1]
'''
#самый большой выше указаного каталога
'''
import pprint #pretty print
trace = False
dirname = 'C:Users\\User\\Documents\\pyhton' if len(sys.argv)==1 else sys.argv[1]

allsize = []
for (dirpath,dirfiles,filenames) in os.walk('..'): #в этом случае это то же что и искать все в предодушем каталоге
    if trace:print('...',dirpath)                  #можно также использовать dirname но в этом примере не хочет заработать
    for filename in filenames:
        if filename.endswith('.py'):
            if trace: print('   ...',filename)
            fullname = os.path.join(dirpath,filename)
            fullsize = os.path.getsize(fullname)
            allsize.append([fullsize,fullname])
allsize.sort()
pprint.pprint(allsize[:2])
pprint.pprint(allsize[-2:])
'''
#самый большой во всей системе
'''
import pprint
trace = 0 #1=показать каталоги 2=показать и файлы

visited = {}
allsizes = []
for srcdir in sys.path:
    print(srcdir)
    for (dirpath,dirfiles,filenames) in os.walk(srcdir):
        if trace>0:print(dirpath)
        dirpath = os.path.normpath(dirpath)
        fixcase = os.path.normcase(dirpath)
        if fixcase in visited:
            continue
        else:
            visited[fixcase]=True
        for filename in filenames:
            if filename.endswith('.py'):
                if trace>1:print('   ...',filename)
                pypath = os.path.join(dirpath,filename)
                try:
                    pysize = os.path.getsize(pypath)
                except os.error:
                    print('skipping',pypath,sys.exc_info()[0])
                else:
                    pylines = len(open(pypath,'rb').readlines())
                    allsizes.append([pysize,pylines,pypath])
allsizes.sort()
pprint.pprint(allsizes[:3])
pprint.pprint(allsizes[-3:])
'''
