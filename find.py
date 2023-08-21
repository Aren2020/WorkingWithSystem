'''
Эквивалент удаленныго модуля find
Этот модул дает все файлы которые соотвесвуют особому типу 
например текстовые файлы *txt
'''
import sys,os,fnmatch
def find(pattern,startdir = os.curdir):
    for (thisDir,subsHere,filesHere) in os.walk(startdir):
        for name in subsHere+filesHere:
            if fnmatch.fnmatch(name,pattern): #похож на модуль re
                fullpath = os.path.join(thisDir,name)
                yield fullpath #если еще не забыл то это генератор

def findlist(pattern,startdir = os.curdir,dosort = False):
    matches = list(find(pattern,startdir))
    if dosort:matches.sort() #do sort
    return matches

if __name__=="__main__":
    pattern,startdir = sys.argv()[0],sys.argv()[1]
    for name in find(pattern,startdir):
        print(name)
    
