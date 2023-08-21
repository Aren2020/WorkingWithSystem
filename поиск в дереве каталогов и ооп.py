import os,sys
from copytree import copyfile

testexts = ['.txt', '.py', '.pyw', '.html', '.c', 'h']

class FileVisitor:
    def __init__(self,context = None,trace = 2):
        self.context = context
        self.trace = trace
        self.dcount = 0
        self.fcount = 0
    
    def run(self,startDir = os.curdir,reset = True):
        if reset:self.reset()
        for (thisDir,subsHere,filesHere) in os.walk(startDir):
            self.visitdir(thisDir)
            for file in filesHere:
                fpath = os.path.join(thisDir,file)
                os.visitfile(fpath)
        
    def reset(self):
        self.dcount = 0
        self.fcount = 0

    def visitdir(self,thisDir):
        self.dcount+=1
        if self.trace>1: print('dir =>',thisDir)

    def visitfile(self,fpath):
        self.fcount+=1 
        if self.trace>1: print('file =>',fpath)
        
class SearchVisitor:
    def __init__(self,context=None,trace=2):
        FileVisitor.__init__(self,context,trace)
        self.scount = 0
    def run(self,startDir,reset = True):
        for (thisDir,subsHere,filesHere) in os.walk(startDir):
            FileVisitor.visitdir(thisDir)
            for file in filesHere:
                fpath = os.path.join(thisDir,file)
                FileVisitor.visitfile(fpath)
                self.search(fpath)
    
    def search(self,fpath):
        if not self.candidate(fpath):
            if self.trace > 0:print('skipping',fpath)
        else:
            filebytes = open(fpath).read()
            if self.context in filebytes:
                self.visitmatch(fpath,filebytes)
                self.scount+=1
    
    def candidate(self,fpath):
        return os.path.splitext(fpath)[1] in testexts
    
    def visitmatch(self,fpath,filebytes):
        if self.trace>0:print('{} has {}'.format(fpath,filebytes))

class ReplaceVisitor(SearchVisitor):
    '''
    Заменяет fromStr на toStr в файлах в каталоге startDir и ниже;
    имена изменившихся файлов сохраняются в списке obj.changed
    '''
    def __init__(self,fromStr,toStr,listOnly = False,trace = 0):
        self.changed = []
        self.toStr = toStr
        self.listOnly = listOnly
        SearchVisitor.__init__(self,fromStr,trace)
    
    def visitmatch(self,fpath,text):
        self.changed.append(fpath)
        if not self.listOnly:
            fromStr,toStr = self.context,self.toStr
            text = text.replace(fromStr,toStr)
            open(fpath,'w').write(text)

class LinesByType(FileVisitor):
    srcExts = []

    def __init__(self,trace=1):
        FileVisitor.__init__(self,trace)
        self.srclines = self.srcfiles = 0
        self.extSums = {ext:dict(files = 0,lines = 0) for ext in self.srcExts}
    
    def visitsource(self,fpath,ext):
        lines = open(fpath,'rb').readlines()
        self.srclines+=lines
        self.srcfiles+=1
        self.extSums[ext]['lines']+=lines
        self.extSums[ext]['files']+=1
    
    def visitfile(self,filepath):
        FileVisitor.visitfile(self,filepath)
        for ext in self.srcExts:
            if filepath.endswith(ext):
                self.visitsource(filepath,ext)
                break
class PyLines(LinesByType):
    srcExts = ['.py','pyc']
class SourceLines(LinesByType):
    srcExts = ['.py','.pyw','.cgi','.html','.c','.cxx','.h','.i']

class CpallVisitor(FileVisitor):
    def __init__(self,fromDir,toDir,trace = 0):
        self.fromDirLen = len(fromDir)+1
        self.toDir = toDir
        FileVisitor.__init__(self,trace = trace)
    
    def visitdir(self,dirpath):
        toPath = os.path.join(self.toDir,dirpath[self.fromDirLen:]) #.../..-toDir ; dowload/hello/-dirpath ; dowload/-fromdir
        if self.trace>0:print('d',dirpath,'=>',toPath)
        os.mkdir(toPath)
        self.dcount+=1
    
    def visitfile(self,filepath):
        toPath = os.path.join(self.toDir,filepath[self.fromDirLen:])
        if self.trace>0: print('f',filepath,'=>',toPath)
        copyfile(filepath,toPath)
        self.fcount+=1
    
    