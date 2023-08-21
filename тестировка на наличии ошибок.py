import os,sys,time,glob
from subprocess import PIPE,Popen

#конфирогуционые аргументы
testdir = sys.argv[1] if len(sys.argv)>1 else os.curdir
forcegen = len(sys.argv)>2
print('Start tester in ',time.asctime())
print('in',os.path.abspath(testdir))

def verbose(*args):
    print('-'*80)
    for arg in args:print(arg)
def quite(*args):pass
trace = quite #можно написать здесь verbose чтобы все было по нагладнее

#отбор сценариев для тестирования
testpatt = os.path.join(testdir,'Scripts','*py')
testfiles = glob.glob(testpatt)
testfiles.sort()
trace(os.getcwd(),*testfiles)

numfile = 0
for testpath in testfiles:
    testname = os.path.basename(testpath)

    infile = testname.replace('.py','.in') #если не понимаеш это открой стр 413 
    inpath = os.path.join(testdir,'Input',infile)
    indata = open(inpath).read() if os.path.exists(inpath) else b''

    argfile = testname.replace('.py','.args')
    argpath = os.path.join(testdir,'Args',argfile)
    argdata = open(argpath).read() if os.path.exists(argpath) else ''

    outfile = testname.replace('.py','.out')
    outpath = os.path.join(testdir,'Output',outfile)
    outpathbad = outfile+'.bad'
    if os.path.exists(outpathbad):os.remove(outpathbad)

    errfile = testname.replace('.py','err')
    errpath = os.path.join(testdir,'Error',errfile)
    if os.path.exists(errpath):os.remove(errpath)

    pypath = sys.executable
    command = '%s %s %s' % (pypath, testpath, argdata)
    process = Popen(command,shell = True,stdout=PIPE,stderr = PIPE,stdin = PIPE)
    process.stdin.write(indata)
    process.stdin.close()
    outdata = process.stdout.read()
    errdata = process.stderr.read()
    exitstatus = process.wait()
    trace(outdata,errdata,exitstatus)

    #анализ данных
    if exitstatus !=0:
        print('Error status: ',testname, exitstatus) #если не ровно 0 значит ошибка было в коде
    if errdata:
        print('Error stream: ',testname, errdata)
        open('errpath','wb').write(errdata)
    
    if exitstatus or errdata:
        numfile+=1
        open(outpathbad,'wb').write(errdata)
    elif not os.path.exists(outpath) or forcegen:
        print('generation:',outpath)
        open(outpath,'wb').write(outdata)
    else:
        priout = open(outpath,'rb').read()
        if priout==outdata:
            print('passed: ',testname)
        else:
            numfile+=1
            print('Failed output:',testname,outpathbad)
    print('Finish in',time.asctime())
    print(f'{len(testfiles)} tests were run,{numfile} tests failed')

