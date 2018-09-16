import requests
import urllib


class QueryLoader():
    def __init__(self, language = 'ru'):
        self._language = language
        self._apiLink = 'https://'+ language + '.wikipedia.org/w/api.php'

    def generateQueryLink(self, action, actionParams = {}):
        params = dict()
        params.update({'action' : action})
        params.update(actionParams)
        query = self._apiLink + '?' + urllib.parse.urlencode(params)
        return  query

    def searchQuery(self, text : str):
        req = requests.get(self.generateQueryLink('opensearch', {'search': text, 'limit': 1, 'format': 'json'}))
        data = req.json()
        if len(data) < 3:
            return 'Ничего не найдено, измените запрос.'
        if len(data[2]) > 0:
            return data[2][0]
        else:
            return 'Неверный формат ответа'


if __name__ == '__main__':
    q = QueryLoader()
    # Work only for query without errros
    # print(q.generateQueryLink('opensearch', {'search' : 'Бальшой андронный коллайдер', 'limit' : 3, 'format' : 'json'}))
    # print(q.generateQueryLink('query', {'list' : 'search', 'srwhat' : 'nearmatch', 'srsearch' : 'большой андронный коллайдер', 'format' : 'json'}))

    print(q.searchQuery('Мыло'))
