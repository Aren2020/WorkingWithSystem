'''найти файлы с определьеным расширением и узнать есть ли в этом файле строка которую мы передим'''
import sys,os
listonly = False
textexts = ['.py','.pyw','.c','.d','.txt']

def searcher(startdir,searchkey):
    global fcount,vcount
    fcount = vcount = 0
    for (thisDir,subsHere,filesHere) in os.walk(startdir):
        for file in filesHere:
            if not listonly:
                try:
                    fullpath = os.path.join(thisDir,file)
                    if os.path.splitext(fullpath)[1] not in textexts:
                        print('Passed',fullpath)
                    elif searchkey in open(fullpath).read():
                        print('Find',searchkey,'in',fullpath)
                        fcount+=1
                except:
                    print('Error',fullpath,sys.exc_info()[0])
            vcount+=1
if __name__ == '__main__':
    startdir,searchkey = sys.argv()[1],sys.argv()[2]
    searcher(startdir,searchkey)
    print('Searched {} found matches in {}'.format(vcount,fcount))

                    