from lxml import etree
from pyfreeling import Analyzer
from os import path
import subprocess
CONFIG_FOLDER = path.join(path.dirname(__file__), 'freeling/data/config/')
FILE_FOLDER = path.join(path.dirname(__file__), 'freeling/')
inputText=open(path.join(FILE_FOLDER, 'test'))
inputText=inputText.read()
print(inputText)
analyzer = Analyzer(config=path.join(CONFIG_FOLDER, 'ru.cfg'))
print('start analyze')
xml = analyzer.run(inputText.encode())
print(type(xml))
root = xml #etree.parse(xml)
rows = root.findall('sentence')
nlist = {}
for s in rows:
    tok = s.findall('token')
    for t in tok:
        if t.attrib['form'] not in nlist:
            nlist.update({t.attrib['form']:1})
        else:
            nlist[t.attrib['form']]+=1
   
result=''
for key in nlist:
    
    print ('у слова ', type(key), key,' количество вхождений равно',nlist[key])
