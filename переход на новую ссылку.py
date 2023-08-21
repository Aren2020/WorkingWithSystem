'''
Создает страницы со ссылками переадресации на перемещенный веб-сайт.
Генерирует по одной странице для каждого существующего на сайте файла html; 
сгенерированные файлы нужно выгрузить на ваш старый веб-сайт.Html файл мы не имеем поэтому 
интерпретатор вызвет ошибку чтобы рассматреть Html кщд можно открыт
Программируем на питоне том 1 стр 405
'''
import os,sys

servername = 'learning-python.com' #новый адрес страницы
homedir = 'books' #корневой каталог сайта
sitefiledirs =  r'C:temp\public_html' #локальный каталог с файлами сайта
uploaddir = r'C:temp\isp-forward' #где сохранить файлы
templatename = 'template.html' #временный html файл которая в себе имеет 
                               #<a href="”http://$server$/$home$/$file$">”http://$server$/$home$/$file$</a> 
try:
    os.mkdir(uploaddir)
except OSError:
    pass

template = open(templatename).read()
sitefiles = os.listdir(sitefiledirs)

count = 0
for filename in sitefiles:
    if filename.endswith('.html') or filename.endswith('.htm'):
        fwdname = os.path.join(uploaddir,filename)
        print('creating',filename,'as',fwdname)
        filetext = template.replace('$server$',servername)
        filetext = filetext.replace('$home$',homedir)
        filetext = filetext.replace('file',filename)
        open(fwdname,'w').write(filetext)
        count+=1

print('Last file',filetext)
print('Done',count,'forward file creating')