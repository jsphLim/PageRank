import requests
import re

websites = []
tmp = []

def dfs(content):
    pattern = re.compile(r'(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')')
    results = pattern.findall(content.decode('ISO-8859-1'))
    for result in results:
        tmp.append(result)


def get_url(url):
    if url in websites:
        return
    try:
        r = requests.get(url)
        print(r.url)
    except:
        print('timout',5)
        return
    else:
        text = r.content
        dfs(text)
        websites.append(url)


if __name__ == '__main__':
    init = 'http://www.jnu.edu.cn/'
    tmp.append(init)
    while len(websites) < 500 and len(tmp) >= 1:
        print(str((len(websites) + 1))+"/500")
        tmp_url = tmp[0]
        del tmp[0]
        get_url(tmp_url)

    print("Finish")
    file = open('result'+'.txt', 'w+')
    for url in websites:
        file.write(url + '\n')
    file.close()
