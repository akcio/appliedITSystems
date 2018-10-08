from lxml import etree
from pyfreeling import Analyzer
from os import path
import subprocess
import bs4

class FreeLingKeyWordSearcher():

    def __init__(self, pathToTextFile, config_folder = path.join(path.dirname(__file__), 'freeling/data/config/'), language='ru'):
        self._configFolder = config_folder
        self._pathToTextFile = pathToTextFile
        self._language = language
        if not path.exists(self._pathToTextFile):
            print('No file in', self._pathToTextFile)
            raise FileNotFoundError

        self._xml = self.runFreeling()
        self._notRecognizedWords = []
        self._dictKeyStruct = {}
        self._dictAllVerbs = {}
        self._averageVerbs = None
        self._averageNouns = None
        self._keyPhrases = []

        self.parseXML()

    def runFreeling(self):
        print('Run freeling')
        p = subprocess.Popen(
            'analyze -f ' + path.join(self._configFolder, self._language + '.cfg') + ' --output xml < ' + self._pathToTextFile,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        r = p.communicate()
        return r[0]

    def getXML(self):
        return self._xml

    def getDictKeyStruct(self):
        return self._dictKeyStruct

    def getNotRecognizedWords(self):
        return self._notRecognizedWords

    def getAverageVerbs(self):
        if self._averageVerbs == None:
            self.calculateAverageVerbs()
        return self._averageVerbs

    def calculateAverageVerbs(self):
        if len(self._dictAllVerbs) != 0:
            self._averageVerbs = sum([self._dictAllVerbs[x] for x in self._dictAllVerbs]) / len(self._dictAllVerbs)
        else:
            raise ZeroDivisionError("No verbs")
        return self._averageVerbs

    def parseXML(self):
        doc = bs4.BeautifulSoup(self._xml, 'html.parser')
        sen = doc.find_all('sentence')

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
                        else:
                            pass
                    elif tag[0] == 'V':
                        verbs.append({'gen' : tag[6], 'num' : tag[2], 'form' : t.attrs['form'].lower(), 'lemma' : t.attrs['lemma'].lower()})
                    elif tag[0] == 'E':
                        nouns.append({'gen': tag[1], 'num': tag[2], 'form': t.attrs['form'].lower(), 'lemma' : t.attrs['lemma'].lower()})
                except:
                    self._notRecognizedWords.append(t.attrs['form'])

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
                    if noun.lower() not in self._dictKeyStruct:
                        self._dictKeyStruct.update({noun.lower() : {'count' : 1, 'verbs': {localSentences[key]['verb'] : 1}}})
                    else:
                        if localSentences[key]['verb'] not in self._dictKeyStruct[noun.lower()]['verbs']:
                            self._dictKeyStruct[noun.lower()]['verbs'].update({localSentences[key]['verb'] : 1})
                        else:
                            self._dictKeyStruct[noun.lower()]['verbs'][localSentences[key]['verb']] += 1
                        self._dictKeyStruct[noun.lower()]['count'] += 1

    def calculateSomeStatistic(self):
        for key in self._dictKeyStruct:
            self._dictKeyStruct[key]['average'] = sum([self._dictKeyStruct[key]['verbs'][x] for x in self._dictKeyStruct[key]['verbs']]) \
                                                  / len(self._dictKeyStruct[key]['verbs'])
            for item in self._dictKeyStruct[key]['verbs']:
                if item not in self._dictAllVerbs:
                    self._dictAllVerbs.update({item: self._dictKeyStruct[key]['verbs'][item]})
                else:
                    self._dictAllVerbs[item] += self._dictKeyStruct[key]['verbs'][item]
            print('у слова ', key, ' количество вхождений равно', self._dictKeyStruct[key]['count'], 'среднее по существительному:',
                  self._dictKeyStruct[key]['average'])
        # trashhold = sum([nlist[x]['count'] for x in nlist]) / sum([[]])

    def calculateAverageNouns(self):
        if len(self._dictKeyStruct) > 0:
            self._averageNouns = sum([self._dictKeyStruct[x]['count'] for x in self._dictKeyStruct]) / len(self._dictKeyStruct)
        else:
            raise ZeroDivisionError("No nouns")
        return self._averageNouns

    def prepareNouns(self, maxCountElems):
        sortedDictKeyStruct = sorted(self._dictKeyStruct.items(), key=lambda kv:kv[1]['count'], reverse=True)
        if maxCountElems < len(sortedDictKeyStruct):
            sortedDictKeyStruct = sortedDictKeyStruct[:maxCountElems]
        return sortedDictKeyStruct

    def prepareVerbsByNoun(self, noun, maxCountElems):
        sortedVerbs = sorted(self._dictKeyStruct[noun]['verbs'].items(), key=lambda kv: kv[1], reverse=True)[:2]
        if len(sortedVerbs) > maxCountElems:
            sortedVerbs = sortedVerbs[:maxCountElems]
        return sortedVerbs

    def getKeyPhrases(self, tresholdNoun = 1, tresholdVerb = 1):
        self._keyPhrases.clear()
        for key, value in self.prepareNouns(4):
            if value['count'] > tresholdNoun:
                currentVerbs = self.prepareVerbsByNoun(key, 2)
                self._keyPhrases.append(str(key) + " " + ",".join(
                    [verb + ":" + str(verb_count) for verb, verb_count in currentVerbs if verb_count > tresholdVerb]))
        return self._keyPhrases

    def printResult(self):
        print("-----------------------")
        print('Key phrases in', self._pathToTextFile, 'are:')
        print('\n'.join(self._keyPhrases))
        if len(self._notRecognizedWords) > 0:
            print('Words with errors:', ', '.join(self._notRecognizedWords))
        else:
            print('All words recognized')

if __name__ == '__main__':
    a = FreeLingKeyWordSearcher(path.join(path.dirname(__file__), 'freeling/test4.txt'))
    a.getKeyPhrases()
    a.printResult()