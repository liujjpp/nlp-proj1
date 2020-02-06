import json
import nltk
from nltk.tokenize import RegexpTokenizer

AWARD_WORDS = ['best', 'Best', 'BEST', 'award', 'Award']

def award_filter(year):
    src_path = './gg' + str(year) + '.json'
    dest_path = './gg' + str(year) + '_award.json'

    with open(src_path, 'r') as fin:
        with open(dest_path, 'w') as fout:
            for tweet in fin.readlines():
                tweet = json.loads(tweet)
                if isinstance(tweet, list):
                    for t in tweet:
                        if any(w in tweet['text'] for w in AWARD_WORDS):
                            new_tweet = {}
                            new_tweet['text'] = t['text']
                            json.dump(new_tweet, fout)
                            fout.write('\n')
                    continue
                if any(w in tweet['text'] for w in AWARD_WORDS):
                    new_tweet = {}
                    new_tweet['text'] = tweet['text']
                    # new_tweet['created_at'] = tweet['created_at']
                    # new_tweet['user'] = tweet['user']
                    json.dump(new_tweet, fout)
                    fout.write('\n')

def host_filter(year):
    src_path = './gg' + str(year) + '.json'
    dest_path = './gg' + str(year) + '_host.json'

    with open(src_path, 'r') as fin:
        with open(dest_path, 'w') as fout:
            for tweet in fin.readlines():
                tweet = json.loads(tweet)
                if isinstance(tweet, list):
                    for t in tweet:
                        if ('host' in t['text'] or 'Host' in t['text']) and not ('next' in t['text'] or 'Next' in t['text']):
                            new_tweet = {}
                            new_tweet['text'] = t['text']
                            json.dump(new_tweet, fout)
                            fout.write('\n')
                    continue
                if ('host' in t['text'] or 'Host' in t['text']) and not ('next' in t['text'] or 'Next' in t['text']):
                    new_tweet = {}
                    new_tweet['text'] = tweet['text']
                    # new_tweet['created_at'] = tweet['created_at']
                    # new_tweet['user'] = tweet['user']
                    json.dump(new_tweet, fout)
                    fout.write('\n')

def dress_filter(year):
    src_path = './gg' + str(year) + '.json'
    dest_path = './gg' + str(year) + '_dress.json'

    with open(src_path, 'r') as fin:
        with open(dest_path, 'w') as fout:
            for tweet in fin.readlines():
                tweet = json.loads(tweet)
                if isinstance(tweet, list):
                    for t in tweet:
                        if 'dress' in tweet['text'] or 'Dress' in tweet['text'] or 'DRESS' in tweet['text']:
                            new_tweet = {}
                            new_tweet['text'] = t['text']
                            json.dump(new_tweet, fout)
                            fout.write('\n')
                    continue
                if 'dress' in tweet['text'] or 'Dress' in tweet['text'] or 'DRESS' in tweet['text']:
                    new_tweet = {}
                    new_tweet['text'] = tweet['text']
                    # new_tweet['created_at'] = tweet['created_at']
                    # new_tweet['user'] = tweet['user']
                    json.dump(new_tweet, fout)
                    fout.write('\n')

# for json files like gg2020_award.json/gg2020_host.json/gg2020_dress.json
# NOT for tokenizing tweets in gg2013.json or gg2015.json
def tweets_to_words(src_path):
    tokenizer = RegexpTokenizer(r'-|[A-Za-z-]+')
    result = []
    with open(src_path, 'r') as fin:
        for tweet in fin.readlines():
            tweet = json.loads(tweet)
            words = tokenizer.tokenize(tweet['text'])
            result.append(words)
    return result


if __name__ == "__main__":
    pass
    # award_filter()
    # host_filter()
    # dress_filter()