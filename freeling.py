from lxml import etree
from pyfreeling import Analyzer
from os import path
import subprocess

CONFIG_FOLDER = path.join(path.dirname(__file__), 'freeling/data/config/')
FILE_FOLDER = path.join(path.dirname(__file__), 'freeling/')

inputText=open(path.join(FILE_FOLDER, 'test'))
inputText=inputText.read()

analyzer = Analyzer(config=path.join(CONFIG_FOLDER, 'ru.cfg'))
print('start analyze')
xml = analyzer.run(inputText.encode())
root = xml#etree.parse(xml)
rows = root.findall('sentence')
nlist = {}
exceptions = ''
for s in rows:
    tok = s.findall('token')
    for t in tok:
        tag = t.attrib['tag']
        try:
            if tag[1]!='P' and tag[0] == 'N' and tag[2] == 'N':
                if t.attrib['form'] not in nlist:
                    nlist.update({t.attrib['form']:int(1)})
                else:
                    nlist[t.attrib['form']]+=1
        except:
            exceptions += t.attrib['form']
            exceptions += ' '
defaultNumb=1

result=str()
for key in nlist:
    print ('у слова ', key,' количество вхождений равно',nlist[key])
for key in nlist:
    if int(nlist[key]) > 1:
        result +=str(key.encode('utf-8'))
        result +=' ,'
print ('\nКлючевыми в этом текте являются слова: ')
print (result)
print ('Неизвестные слова:')
print (exceptions)
