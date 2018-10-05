from lxml import etree
from pyfreeling import Analyzer
from os import path
import subprocess
import bs4

CONFIG_FOLDER = path.join(path.dirname(__file__), 'freeling/data/config/')
FILE_FOLDER = path.join(path.dirname(__file__), 'freeling/')

inputText=open(path.join(FILE_FOLDER, 'test'))
inputText=inputText.read()

p = subprocess.Popen('analyze -f ' + path.join(CONFIG_FOLDER, 'ru.cfg') + ' --output xml < ' + path.join(FILE_FOLDER, 'test4.txt'),
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
                # elif len(tag) > 2:
                #     print(tag)
                #     nouns.append({'gen' : tag[2], 'num' : -1, 'form' : t.attrs['form'].lower(), 'lemma' : t.attrs['lemma'].lower()})
                else:
                    # print(tag, t.attrs['lemma'])
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
            if noun['gen'] == 'N' and (noun['gen'] == verb['gen'] or noun['gen'] == -1) and (noun['num'] == verb['num'] or noun['num'] == -1):
                if verb['lemma'] not in localSentences:
                    localSentences.update({verb['lemma'] : {'verb' : verb['form'], 'noun' : [noun['form']]}})
                else:
                    if noun['form'] not in localSentences[verb['lemma']]['noun']:
                        localSentences[verb['lemma']]['noun'].append(noun['lemma'])
    # print(localSentences)
    for key in localSentences:
        print(",".join(localSentences[key]['noun']) + " " + localSentences[key]['verb'])
        for noun in localSentences[key]['noun']:
            if noun.lower() not in nlist:
                nlist.update({noun.lower() : {'count' : 1, 'verbs': {localSentences[key]['verb'] : 1}}})
            else:
                if localSentences[key]['verb'] not in nlist[noun.lower()]['verbs']:
                    nlist[noun.lower()]['verbs'].update({localSentences[key]['verb'] : 1})
                else:
                    nlist[noun.lower()]['verbs'][localSentences[key]['verb']] += 1
                nlist[noun.lower()]['count'] += 1
defaultNumb=1

result=str()
superVerbs = {}

for key in nlist:
    nlist[key]['average'] = sum([ nlist[key]['verbs'][x] for x in nlist[key]['verbs']]) / len(nlist[key]['verbs'])
    for item in nlist[key]['verbs']:
        if item not in superVerbs:
            superVerbs.update({item: nlist[key]['verbs'][item]})
        else:
            superVerbs[item] += 1
    print ('у слова ', key,' количество вхождений равно', nlist[key]['count'], 'среднее по существительному:', nlist[key]['average'])
isFirst = True

averageVervs = sum([superVerbs[x] for x in superVerbs]) / len(superVerbs)
# trashhold = sum([nlist[x]['count'] for x in nlist]) / sum([[]])

sortedNList = sorted(nlist.items(), key=lambda kv:kv[1]['count'], reverse=True)[:4]

for key, nlist[key] in sortedNList:
    if nlist[key]['count'] > 1:
        if not isFirst:
            result += ", "
        sort = sorted(nlist[key]['verbs'].items(), key=lambda kv:kv[1], reverse=True)[:2]
        # print(sort)
        result += str(key) + " " + ",".join([verb + ":" + str(verb_count) for verb, verb_count in sort if verb_count > 1]) + '\n'
    # for verb in nlist[key]['verbs']:
    #     item = nlist[key]['verbs'][verb]
    #     if int(item) > 1:
    #         if not isFirst:
    #             result += ", "
    #         result +=str(key) + " " + str(verb)
    #         isFirst = False

print ('\nКлючевыми в этом текте являются слова: ')
print (result)
print ('Неизвестные слова:')
print(', '.join(exceptions))