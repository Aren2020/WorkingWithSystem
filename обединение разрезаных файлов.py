import os,sys

readsize = 1024

def join(fromdir,tofile):
    output = open(tofile,'wb')
    parts = os.listdir(fromdir)
    parts.sort()
    for filename in parts:
        filepath = os.path.join(fromdir,filename)
        fileobj = open(filepath,'rb')
        while True:
            data = fileobj.read(readsize)
            if not data: break
            output.write(data)
        fileobj.close()
    output.close()

if __name__=="__main__":
    if len(sys.argv)==2 and sys.argv[1]=='-help':
        print('use: join.py [from-dir-name to-file-name]')
    else:
        if len(sys.argv)<2:
            interactive = True
            fromdir = input('Directory contains part files')
            tofile = input('Name of file to be recreated')
        else:
            interactive = False
            formdir,tofile = sys.argv[1:]
        absfrom,absto = map(os.path.abspath,[fromdir,tofile])
        print('Join',absfrom,'to',absto)

        try:
            join(fromdir,tofile)
        except:
            print('Error')
            print(sys.exc_info()[0],sys.exc_info()[1])
        else:
            print('Join complete:see ',tofile)
        if interactive:input('Press Enter key')



