import os,sys

kilobytes = 1024
megabytes = 1024*1000
chunksize = (1.4*megabytes)

def split(fromfile,todir,chunksize = chunksize):
    if not os.path.exists(todir): #если путь не существует
        os.mkdir(todir) #создать такой файл с путем todir
    else:
        for fname in os.listdir(todir):
            os.remove(os.path.join(todir,fname)) #удалить все элементы этой пути
    partnum = 0
    input = open(fromfile,'rb')

    while True:
        chunk = input.read(chunksize)
        if not chunk: break
        partnum+=1
        filename = os.path.join(os.path.join('part%04d' % partnum))
        fileobj = open(filename,'wb')
        fileobj.write(chunk)
        fileobj.close()
    input.close()
    assert partnum<=9999
    return partnum #сколько кусков получилось

if __name__=='__main__':
    if len(sys.argv) == 2 and sys.argv[1]=='-help':
        print('use: split.py [file-to-split target-dir [chunksize]]')
    else:
        if len(sys.argv)<3:
            interactive = True
            fromfile = input('File to split?')
            todir = input('Directory to store  part files')
        else:
            interactive = False
            fromfile,todir = sys.argv[1:3]
            if len(sys.argv)==4:chunksize = sys.argv[3]
        absfrom,absto = map(os.path.abspath,[fromfile,todir]) #абсолютный путь к файлу
        print('Spliting',absfrom,'to',absto,'by',chunksize)

    try:
        parts = split(fromfile,todir,chunksize)
    except:
        print('Error')
        print(sys.exc_info()[0],sys.exc_info()[1])
    else:
        print('Split finished:',parts,'parts are in',absto)
if interactive:input('Press Enter key')
