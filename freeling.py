from lxml import etree
from pyfreeling import Analyzer
from os import path
import subprocess
import bs4

CONFIG_FOLDER = path.join(path.dirname(__file__), 'freeling/data/config/')
FILE_FOLDER = path.join(path.dirname(__file__), 'freeling/')

inputText=open(path.join(FILE_FOLDER, 'test'))
inputText=inputText.read()

p = subprocess.Popen('analyze -f ' + path.join(CONFIG_FOLDER, 'ru.cfg') + ' --output xml < ' + path.join(FILE_FOLDER, 'test2'),
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
r = p.communicate()
t = r[0]
doc = bs4.BeautifulSoup(t, 'html.parser')
sen = doc.find_all('sentence')
nlist={}
exceptions=[]
for s in sen:
    tok = s.find_all('token')
    nouns = []
    verbs = []
    localSentences = {}
    for t in tok:
        tag = t.attrs['tag']
        try:
            if tag[0] == 'N':
                if len(tag) > 3:
                    nouns.append({'gen' : tag[2], 'num' : tag[3], 'form' : t.attrs['form'].lower(), 'lemma' : t.attrs['lemma'].lower()})
                elif len(tag) > 2:
                    nouns.append({'gen' : tag[2], 'num' : -1, 'form' : t.attrs['form'].lower(), 'lemma' : t.attrs['lemma'].lower()})
                else:
                    pass
                    #nouns.append({'gen' : tag[2], 'num' : -1, 'form' : t.attrs['form']})
            elif tag[0] == 'V':
                verbs.append({'gen' : tag[6], 'num' : tag[2], 'form' : t.attrs['form'].lower(), 'lemma' : t.attrs['lemma'].lower()})
            elif tag[0] == 'E':
                nouns.append({'gen': tag[1], 'num': tag[2], 'form': t.attrs['form'].lower(), 'lemma' : t.attrs['lemma'].lower()})
        except:
            exceptions.append(t.attrs['form'])
        # try:
        #     if tag[1] != 'P' and tag[0] == 'N' and tag[2] == 'N':
        #         if t.attrs['form'] not in nlist:
        #             nlist.update({t.attrs['form']: 1})
        #         else:
        #             nlist[t.attrs['form']] += 1
        # except:
        #     exceptions.append(t.attrs['form'])
    for verb in verbs:
        for noun in nouns:
            if (noun['gen'] == verb['gen'] or noun['gen'] == -1) and (noun['num'] == verb['num'] or noun['num'] == -1):
                if verb['lemma'] not in localSentences:
                    localSentences.update({verb['lemma'] : {'verb' : verb['form'], 'noun' : [noun['form']]}})
                else:
                    if noun['form'] not in localSentences[verb['lemma']]['noun']:
                        localSentences[verb['lemma']]['noun'].append(noun['form'])
    # print(localSentences)
    for key in localSentences:
        print(",".join(localSentences[key]['noun']) + " " + localSentences[key]['verb'])
        for noun in localSentences[key]['noun']:
            if noun.lower() not in nlist:
                nlist.update({noun.lower() : 1})
            else:
                nlist[noun.lower()] += 1
defaultNumb=1

result=str()
for key in nlist:
    print ('у слова ', key,' количество вхождений равно', nlist[key])
for key in nlist:
    if int(nlist[key]) > 1:
        result +=str(key)
        result +=', '
print ('\nКлючевыми в этом текте являются слова: ')
print (result)
print ('Неизвестные слова:')
print(', '.join(exceptions))