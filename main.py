#!/usr/bin/python3

import requests
import argparse
import threading

from bottle import run, get, request
from textblob import TextBlob
from bs4 import BeautifulSoup


def request_sender(urls: list[str], slave_url: str, words: dict[str, int]):
    request_result = requests.get(slave_url, json={'urls': urls})
    if request_result.status_code == 200:
        for word_k, word_v in request_result.json().items():
            if words.get(word_k) is None:
                words.setdefault(word_k, word_v)
            else:
                words[word_k] = words[word_k] + word_v


@get('/words')
def get_words():
    words: dict[str, int] = dict()

    if request.json is None or request.json['urls'] is None:
        return 'no data'

    urls = request.json['urls']
    middle = int(len(urls) / 2)

    t1 = threading.Thread(target=request_sender, args=[urls[:middle], 'http://0.0.0.0:8081/count', words])
    t2 = threading.Thread(target=request_sender, args=[urls[middle:], 'http://0.0.0.0:8082/count', words])

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    result_word = {}
    for word in reversed(sorted(words.items(), key=lambda item: item[1])):
        if len(result_word) >= 10:
            break
        result_word.setdefault(word[0], word[1])

    return result_word


@get('/count')
def words_count():
    urls: list[str] = request.json['urls']
    words: dict[str, int] = dict()
    for url_to_parse in urls:
        request_result = requests.get(url_to_parse)
        if request_result.status_code == 200:
            page = BeautifulSoup(request_result.text, 'html.parser')
            wiki_content = page.find('div', id='mw-content-text')
            if wiki_content is not None:
                text_to_parse = wiki_content.get_text().lower()
                for word in TextBlob(text_to_parse).words:
                    if words.get(word) is None:
                        words.setdefault(word, 1)
                    else:
                        words[word] = words[word] + 1
    return words


parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, required=True)
parser.add_argument('--port', type=int, required=True)

args = parser.parse_args()

run(host=args.host, port=args.port, debug=False)
