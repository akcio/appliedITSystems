from lxml import etree
from pyfreeling import Analyzer
from os import path
import subprocess
import bs4

CONFIG_FOLDER = path.join(path.dirname(__file__), 'freeling/data/config/')
FILE_FOLDER = path.join(path.dirname(__file__), 'freeling/')

inputText=open(path.join(FILE_FOLDER, 'test'))
inputText=inputText.read()

p = subprocess.Popen('analyze -f ' + path.join(CONFIG_FOLDER, 'ru.cfg') + ' --output xml < ' + path.join(FILE_FOLDER, 'test'),
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
r = p.communicate()
t = r[0]
doc = bs4.BeautifulSoup(t, 'html.parser')
sen = doc.find_all('sentence')
nlist={}
exceptions=str()
for s in sen:
    tok = s.find_all('token')
    for t in tok:
        tag = t.attrs['tag']
        try:
            if tag[1]!='P' and tag[0] == 'N' and tag[2] == 'N':
                if t.attrs['form'] not in nlist:
                    nlist.update({t.attrs['form']:int(1)})
                else:
                    nlist[t.attrs['form']]+=1
        except:
            exceptions+=t.attrs['form']
            exceptions+=' '
defaultNumb=1

result=str()
for key in nlist:
    print ('у слова ', key,' количество вхождений равно',nlist[key])
for key in nlist:
    if int(nlist[key]) > 1:
        result +=str(key)
        result +=', '
print ('\nКлючевыми в этом текте являются слова: ')
print (result)
print ('Неизвестные слова:')
print (exceptions)
