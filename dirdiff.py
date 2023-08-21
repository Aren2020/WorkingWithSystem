'''Поиск расхождений между каталогами'''
import os,sys

def reportdiffs(unique1,unique2,dir1,dir2):
    if not (unique1 or unique2):
        print('Directions are indefical')
    else:
        if unique1:
            print('Files unique to',dir1)
            for file in unique1:
                print('...',file)
        if unique2:
            print('Files unique to',dir2)
            for file in unique2:
                print('...',file)

def diference(set1,set2):
    return [item for item in set1 if item not in set2]

def comparedirs(dir1,dir2,files1 = None,files2 = None):
    print('Comparing',dir1,'to',dir2)
    files1 = os.listdir(dir1) if files1 is None else files1
    files2 = os.listdir(dir2) if files2 is None else files2
    unique1 = diference(files1,files2)
    unique2 = diference(files2,files1)
    reportdiffs(unique1,unique2,dir1,dir2)
    return not (unique1 or unique2) #True если нет различий

def getargs():
    try:
        dir1,dir2 = sys.argv[1:]
    except:
        print('Usage Error: file.py dir1 dir2')
        sys.exit(1)
    else:
        return (dir1,dir2)

if __name__=='__main__':
    dir1,dir2 = getargs()
    comparedirs(dir1,dir2)
