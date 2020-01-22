import json
import nltk
from nltk.tokenize import RegexpTokenizer

def best_filter(src_path='./gg2020.json', dest_path='./gg2020_best.json'):
    with open(src_path, 'r') as fin:
        with open(dest_path, 'w') as fout:
            for tweet in fin.readlines():
                tweet = json.loads(tweet)
                if 'best' in tweet['text'] or 'Best' in tweet['text'] or 'BEST' in tweet['text']:
                    new_tweet = {}
                    new_tweet['text'] = tweet['text']
                    new_tweet['created_at'] = tweet['created_at']
                    new_tweet['user'] = tweet['user']
                    json.dump(new_tweet, fout)
                    fout.write('\n')

def host_filter(src_path='./gg2020.json', dest_path='./gg2020_host.json'):
    with open(src_path, 'r') as fin:
        with open(dest_path, 'w') as fout:
            for tweet in fin.readlines():
                tweet = json.loads(tweet)
                if 'host' in tweet['text'] or 'Host' in tweet['text'] or 'HOST' in tweet['text']:
                    new_tweet = {}
                    new_tweet['text'] = tweet['text']
                    new_tweet['created_at'] = tweet['created_at']
                    new_tweet['user'] = tweet['user']
                    json.dump(new_tweet, fout)
                    fout.write('\n')

def dress_filter(src_path='./gg2020.json', dest_path='./gg2020_dress.json'):
    with open(src_path, 'r') as fin:
        with open(dest_path, 'w') as fout:
            for tweet in fin.readlines():
                tweet = json.loads(tweet)
                if 'dress' in tweet['text'] or 'Dress' in tweet['text'] or 'DRESS' in tweet['text']:
                    new_tweet = {}
                    new_tweet['text'] = tweet['text']
                    new_tweet['created_at'] = tweet['created_at']
                    new_tweet['user'] = tweet['user']
                    json.dump(new_tweet, fout)
                    fout.write('\n')

def tweets_to_words(src_path):
    tokenizer = RegexpTokenizer(r'-|\w+')
    result = []
    with open(src_path, 'r') as fin:
        for tweet in fin.readlines():
            tweet = json.loads(tweet)
            words = tokenizer.tokenize(tweet['text'])
            result.append(words)
    return result


if __name__ == "__main__":
    best_filter()
    host_filter()
    dress_filter()