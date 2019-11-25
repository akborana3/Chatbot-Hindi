import sys
import re
import requests
import bs4 as bs
import urllib.request
import urllib.parse
import nltk

sentences = []
roots = []
pos_tags = []


def lemmatize(line):
    cur_root = ""
    cur_pos = ""
    cur_sentence = ""
    arr_words = re.split("\.[0-9]\\\\t", line)

    for i in range(1, len(arr_words)):
        words = re.split('\\\\t', arr_words[i])

        cur_sentence = cur_sentence + (words[0] + ' ')
        cur_pos = cur_pos + (words[1] + ' ')
        temp = arr_words[i].split('\'')

        cur_root = cur_root + (temp[1].split(',')[0] + ' ')

    sentences.append(cur_sentence)
    roots.append(cur_root)
    pos_tags.append(cur_pos)


def parse():
    name = query + ".txt"
    with open(name, 'r') as f:
        for line in f:

            headers = {'Content-Type': 'application/json'}

            data = '{"text":"' + line.strip() + '"}'
            response = requests.post('http://10.2.6.249:8010/shallow_parse_hin', headers=headers, data=data.encode('utf-8'))

            lemmatize(response.text)

    sentence = open("data_sentences.txt", 'w', encoding='utf-8')
    root = open("data_roots.txt", 'w', encoding='utf-8')
    pos_tag = open("data_pos_tags.txt", 'w', encoding='utf-8')

    for i in range(0, len(sentences)):
        sentence.write(sentences[i] + '\n')
        pos_tag.write(pos_tags[i] + '\n')
        root.write(roots[i] + '\n')

    sentence.close()
    root.close()
    pos_tag.close()


query = 'भारत'
url_path = urllib.parse.quote(query)
raw_html = urllib.request.urlopen("https://hi.wikipedia.org/wiki/" + url_path)
raw_html = raw_html.read()

html = bs.BeautifulSoup(raw_html, 'lxml')

paragraphs = html.find_all('p')

data = ''

for para in paragraphs:
    data += para.text

data = re.sub(r'\[[0-9]*\]', ' ', data)
data = re.sub(r'\s+', ' ', data)
data = re.sub(r'<.*>', '', data)
data = data.replace('। ', '।\n')
data = re.sub(r'।.', '।\n', data)
data = data.replace('"', '$')
data = data.split("\n")
print(data)

sent = open(query + ".txt", 'w', encoding='utf-8')

for i in range(0, len(data)):
    sent.write(data[i] + '\n')
