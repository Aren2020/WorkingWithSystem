import os,dirdiff
blocksize = 1024*1024

def intersect(set1,set2):
    return [item for item in set1 if item in set2]

def comparetrees(dir1,dir2,diffts,verbose = False):
    #сравнить списки с именами файлов 
    print('-'*20)
    names1 = os.listdir(dir1)
    names2 = os.listdir(dir2)
    if not dirdiff.comparedirs(dir1,dir2,names1,names2):
        diffts.append('unique files at %s - %s' % (dir1,dir2))
    
    print('Comparing content...')
    common = intersect(names1,names2)
    missed = common[:]

    #сравнить содержимое файлов с одинаковами именами
    for name in common:
        path1 = os.path.join(dir1,name)
        path2 = os.path.join(dir2,name)
        if os.path.isfile(path1) and os.path.isfile(path2):
            missed.remove(name)
            file1 = open(path1,'rb')
            file2 = open(path2,'rb')
            while True:
                bytes1 = file1.read(blocksize)
                bytes2 = file2.read(blocksize)
                if (not bytes1) and (not bytes2):
                    if verbose:print(name,'matches')
                    break
                if bytes1 != bytes2:
                    diffts.append('files differ at %s - %s' % (path1,path2))
                    print(name,"DIFFERS")
                    break
    #рекурсивно сравнить каталоги с одинаковами именами
    for name in common:
        path1 = os.path.join(dir1,name)
        path2 = os.path.join(dir1,name)
        if os.path.isdir(path1) and os.path.isdir(path2):
            missed.remove(name)
            comparetrees(path1,path2)
    
    #одинаковые имена, но оба не являются одновременно файлами или каталогами?
    for name in missed:
        diffts.append('files missed at %s - %s: %s' % (dir1,dir2,name))
        print(name,'DIFFERS')
if __name__=="__main__":
    dir1,dir2 = dirdiff.getargs()
    diffts = []
    comparetrees(dir1,dir2,diffts,True)
    print('='*40)
    if not diffts:
        print('No diffts found')
    else:
        print('Diffs found',len(diffts))
        for diffs in diffts:print('-',diffs)
