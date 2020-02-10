'''Version 0.35'''
import imdb
import json
import re
import spacy
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from nltk.tokenize import RegexpTokenizer
from preprocess import *
from red_carpet import *

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']
OFFICIAL_AWARDS = []
AWARD_CATEGORIES = {'animated': [], 'foreign': [], 'screenplay': [], 'director': [], 'song': [], 
                    'score': [], 'actor-drama': [], 'actress-drama': [], 'other-drama': [], 'actor-comedy': [], 
                    'actress-comedy': [], 'other-comedy': [], 'actor-other': [], 'actress-other': [], 'other-other': []}
YEAR = None
NLP = spacy.load('en_core_web_sm')
DB = imdb.IMDb()

def get_human_names(text):
    '''Extracts human names from tweet text.
    Returns a list of strings.'''
    names = []
    doc = NLP(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    for ent in entities:
        if ent[1] == 'PERSON':
            names.append(ent[0])
    return names

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    src_path = './gg' + str(year) + '_host.json'
    tweets = tweets_to_words(src_path)
    if len(tweets) > 5000:
        tweets = tweets[:5000]
    hosts = []
    all_names = []
    stop_words = ['Golden', 'golden', 'Hollywood', 'hollywood']

    for tweet in tweets:
        names = get_human_names(' '.join(tweet))
        for name in names:
            name_list = name.split()
            if name_list[0] == 'RT':
                continue
            if len(name_list) > 1 and len(name_list) < 3 and not any(w in name for w in stop_words):
                all_names.append(name.lower())

    name_counter = Counter(all_names)
    top2 = name_counter.most_common(2)
    hosts.append(top2[0][0])
    if top2[1][1] > top2[0][1] * 0.4:
        hosts.append(top2[1][0])
    
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    keywords = ['Win', 'win', 'won', 'nail', 'Goes To', 'Goes to', 'goes to', 'Named', 'named', 'takes home', 'taken home']
    best_words = ['Best', 'BEST']
    helper_words = ['a', 'an', 'any', 'by', 'for', 'in', 'or', '-']
    characters = [' B ', ' C ', ' D ', ' E ', ' F ', ' G ', ' H ', ' I ', ' J ', ' K ', ' L ', ' M ',
                  ' N ', ' O ', ' P ', ' Q ', ' R ', ' S ', ' T ', ' U ', ' V ', ' W ', ' X ', ' Y ', ' Z ',
                  ' b ', ' c ', ' d ', ' e ', ' f ', ' g ', ' h ', ' i ', ' j ', ' k ', ' l ', ' m ',
                  ' n ', ' o ', ' p ', ' q ', ' r ', ' s ', ' t ', ' u ', ' v ', ' w ', ' x ', ' y ', ' z ']
    awards = []
    award_contains_human_name = []

    src_path = './gg' + str(year) + '_award.json'
    # round 1
    with open(src_path, 'r') as fin:
        for tweet in fin.readlines():
            tweet = json.loads(tweet)
            
            if 'Award' in tweet['text'] or 'award' in tweet['text']:
                text = tweet['text']
                for ch in characters:
                    if ch in text:
                        text = text.replace(ch, ' ' + ch[1] + '. ')
                names = get_human_names(text)
                for name in names:
                    if 'Golden' in name or 'golden' in name or name[-1] != 'd' or len(name.split()) < 4:
                        continue
                    if 'award' in name or 'Award' in name:
                        award_contains_human_name.append(name.lower())
                    elif (name + 'award') in name or (name + 'Award') in name:
                        award_contains_human_name.append(name.lower() + 'award')

            if not any(w in tweet['text'] for w in keywords):
                continue

            first_index = -1
            if 'Best' in tweet['text']:
                first_index = tweet['text'].index('Best')
            elif 'BEST' in tweet['text']:
                first_index = tweet['text'].index('BEST')
            else:
                continue
            text = tweet['text'][first_index:]
            text = text.split()

            noise_words = ['Golden', 'Globe', 'Hollywood', 'Oscar', 'Nomin', 'Win', 'At', 'The']
            award_name = ['best']
            for word in text[1:]:
                if (65 <= ord(word[0]) <= 90) or word in helper_words:
                    if any(w in word for w in noise_words):
                        break

                    if word.lower() == 'for' and award_name[-1] != 'made':
                        break

                    if word in helper_words:
                        if word == '-':
                            noise_words.append(word)
                        award_name.append(word)
                        continue
                    
                    if not (97 <= ord(word[-1]) <= 122 or 65 <= ord(word[-1]) <= 90 or word[-1] == ','):
                        new_word = word
                        while len(new_word) > 0 and not (97 <= ord(new_word[-1]) <= 122 or 65 <= ord(new_word[-1]) <= 90):
                            new_word = new_word[:-1]
                        if len(new_word) > 0:
                            award_name.append(new_word.lower())
                        break
                    
                    if word in best_words:
                        if award_name[-1] in helper_words:
                            while award_name[-1] in helper_words:
                                award_name = award_name[:-1]
                        if len(award_name) > 4 and len(award_name) < 20:
                            name = ' '.join(award_name)
                            while not (97 <= ord(name[-1]) <= 122 or 65 <= ord(name[-1]) <= 90):
                                name = name[:-1]
                            if 4 < len(name.split()) < 20:
                                awards.append(name)
                        award_name = ['best']
                        continue
                    
                    award_name.append(word.lower())
            
            if award_name[-1] in helper_words:
                while award_name[-1] in helper_words:
                    award_name = award_name[:-1]
            if 4 < len(award_name) < 20:
                awards.append(' '.join(award_name))

    awards_counter = Counter(awards)
    top150 = awards_counter.most_common(150)
    potential_awards = [key for key, val in top150]
    awards = []
    # round 2
    with open(src_path, 'r') as fin:
        for tweet in fin.readlines():
            tweet = json.loads(tweet)
            text = tweet['text'].lower()
            for award in potential_awards:
                if award in text:
                    awards.append(award)
    
    # synonym replacement
    for award in awards:
        new_award = award
        if '- -' in award:
            new_award = new_award.replace('- -', '-')
        if 'tv' in award:
            new_award = new_award.replace('tv', 'television')
        if 'miniseries' in award:
            new_award = new_award.replace('miniseries', 'mini-series')
        if 'mini series' in award:
            new_award = new_award.replace('mini series', 'mini-series')
        if new_award != award:
            awards.append(new_award)

    new_awards = []
    filter_words = ['- -', 'tv', 'miniseries', 'mini series']
    for award in awards:
        if not any(w in award for w in filter_words):
            new_awards.append(award)
    
    awards_counter = Counter(new_awards)
    award_contains_human_name_counter = Counter(award_contains_human_name)

    # merge similar award names
    for key in awards_counter.keys():
        if '-' in key:
            similar = key.replace(' - ', ' ')
            if similar in awards_counter.keys():
                awards_counter[key] += awards_counter[similar]
                awards_counter[similar] = 0
            similar = key.replace(' - ', ', ')
            if similar in awards_counter.keys():
                awards_counter[key] += awards_counter[similar]
                awards_counter[similar] = 0
        if ' or ' in key:
            similar = key.replace(' or ', ' ')
            if similar in awards_counter.keys():
                awards_counter[key] += awards_counter[similar]
                awards_counter[similar] = 0
            similar = key.replace(' or ', '/')
            if similar in awards_counter.keys():
                awards_counter[key] += awards_counter[similar]
                awards_counter[similar] = 0
        if ' any ' in key:
            similar = key.replace(' any ', ' a ')
            if similar in awards_counter.keys():
                awards_counter[key] += awards_counter[similar]
                awards_counter[similar] = 0
    
    top100 = awards_counter.most_common(100)
    awards = []
    top_n, count = 25, 0
    for key, val in top100:
        if val == 0:
            break
        if count <= top_n:
            if '-' in key:
                awards.append(key)
                count += 1
    top_n, count = 10, 0
    for key, val in top100:
        if val == 0:
            break
        if count <= top_n:
            if len(key.split()) >= 10 and not '-' in key:
                awards.append(key)
                count += 1
    award_contains_name = award_contains_human_name_counter.most_common(1)
    awards.append(award_contains_name[0][0])

    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    official_awards = OFFICIAL_AWARDS_1819 if year > 2016 else OFFICIAL_AWARDS_1315
    nominees_all = dict().fromkeys(official_awards, None)
    for key in nominees_all:
        nominees_all[key] = []
    
    tokenizer_for_person = RegexpTokenizer(r'[A-Za-z-]+')
    tokenizer_for_movie = RegexpTokenizer(r'-|&|[A-Za-z0-9:,]+')

    person_award_keywords = ['actor', 'actress', 'director', 'award']
    nominee_keywords = ['nomin', 'beat', 'will win', 'would win', 'not win', 'should have won']
    noise_words = ['why ', 'info ']

    src_path = './gg' + str(year) + '_classified.json'
    with open(src_path, 'r') as fin:
        for tweet in fin.readlines():
            tweet = json.loads(tweet)
            if not any(w in tweet['text'].lower() for w in nominee_keywords):
                continue
            if 'award' in tweet['category']:
                continue
            if any(w in tweet['category'] for w in person_award_keywords):
                words = tokenizer_for_person.tokenize(tweet['text'])
                text = ' '.join(words)
                names = get_human_names(text)
                stop_words = ['golden', 'globes', 'oscar', 'hollywood', 'congrats', 'represent', 'didn', 'comedy', 'hbo', 'would', 'deadline', 'rt']
                for name in names:
                    name_lower = name.lower()
                    if not any(w in name_lower for w in stop_words) and len(name.split()) < 4:
                        nominees_all[tweet['category']].append(name_lower)
            else:
                words = tokenizer_for_movie.tokenize(tweet['text'])
                text = ' '.join(words)
                names = re.findall('((?:[0-9]+|[A-Z][a-z]+|[A-Z]+)[:,]?(?:\s(?:&\s)?(?:-\s)?(?:in\s)?(?:on\s)?(?:and\s)?(?:for\s)?(?:to\s)?(?:a\s)?(?:[0-9]+|[A-Z][a-z]+|[A-Z]+)[:,]?)*)', text)
                stop_words = ['golden', 'globes', 'oscar', 'congrats', 'best', 'award', 'netflix', 'http', 'hbo', 'nigger', 'rt', 'tv']
                for name in names:
                    if not len(name) > 1:
                        continue
                    name_lower = name.lower()
                    for w in noise_words:
                        if w in name_lower:
                            name_lower = name_lower.replace(w, '')
                    if not any(w in name_lower for w in stop_words):
                        if not name_lower.count(',') > 1:
                            nominees_all[tweet['category']].append(name_lower)
                        else:
                            name_lower = name_lower.replace(' and', ',')
                            movies = name_lower.split(', ')
                            for movie in movies:
                                nominees_all[tweet['category']].append(movie)
    
    nominees = dict().fromkeys(official_awards, None)
    for key in nominees:
        nominees_counter = Counter(nominees_all[key])
        top5 = nominees_counter.most_common(5)
        nominees[key] = []
        if len(top5) > 0:
            for k, v in top5:
                nominees[key].append(k)

    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    official_awards = OFFICIAL_AWARDS_1819 if year > 2016 else OFFICIAL_AWARDS_1315
    winners_all = dict().fromkeys(official_awards, None)
    for key in winners_all:
        winners_all[key] = []
    
    tokenizer_for_person = RegexpTokenizer(r'[A-Za-z-]+')
    tokenizer_for_movie = RegexpTokenizer(r'-|&|[A-Za-z0-9:,]+')

    person_award_keywords = ['actor', 'actress', 'director', 'award']
    winner_keywords = ['win', 'won', 'receives', 'accepts', 'scoop']
    not_winner_words = ['would win', 'will win']

    src_path = './gg' + str(year) + '_classified.json'
    with open(src_path, 'r') as fin:
        for tweet in fin.readlines():
            tweet = json.loads(tweet)
            if not any(w in tweet['text'].lower() for w in winner_keywords):
                continue
            if any (w in tweet['text'].lower() for w in not_winner_words):
                continue
            if any(w in tweet['category'] for w in person_award_keywords):
                words = tokenizer_for_person.tokenize(tweet['text'])
                text = ' '.join(words)
                names = get_human_names(text)
                stop_words = ['golden', 'globes', 'oscar', 'hollywood', 'congrats', 'represent', 'didn', 'comedy', 'hbo', 'would', 'deadline', 'rt', 'award', 'win']
                for name in names:
                    name_lower = name.lower()
                    if not any(w in name_lower for w in stop_words) and len(name.split()) < 4:
                        winners_all[tweet['category']].append(name_lower)
            else:
                words = tokenizer_for_movie.tokenize(tweet['text'])
                text = ' '.join(words)
                names = re.findall('((?:[0-9]+|[A-Z][a-z]+|[A-Z]+)[:,]?(?:\s(?:&\s)?(?:-\s)?(?:in\s)?(?:for\s)?(?:a\s)?(?:[0-9]+|[A-Z][a-z]+|[A-Z]+)[:,]?)*)', text)
                stop_words = ['golden', 'globes', 'oscar', 'congrats', 'best', 'award', 'netflix', 'http', 'hbo', 'nigger', 'rt', 'tv']
                for name in names:
                    if not len(name) > 1:
                        continue
                    name_lower = name.lower()
                    if not any(w in name_lower for w in stop_words):
                        winners_all[tweet['category']].append(name_lower)
    
    winners = dict().fromkeys(official_awards, None)
    for key in winners:
        winner_counter = Counter(winners_all[key])
        top1 = winner_counter.most_common(1)
        if len(top1) > 0:
            winners[key] = top1[0][0]
        else:
            winners[key] = ''

    for key in winners:
        if any(w in key for w in person_award_keywords):
            if len(winners[key].split()) < 2 and winners[key] != '':
                print('Searching %s ...' % winners[key])
                query = DB.search_person(winners[key])
                for person in query:
                    official_name = person['name']
                    flag = False
                    if len(official_name.split()) > 1:
                        name_lower = official_name.lower()
                        for name in winners_all[key]:
                            if name == name_lower:
                                winners[key] = name_lower
                                flag = True
                                break
                    if flag:
                        break

    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    official_awards = OFFICIAL_AWARDS_1819 if year > 2016 else OFFICIAL_AWARDS_1315
    tokenizer = RegexpTokenizer(r'-|[A-Za-z]+')

    presenters_all = dict().fromkeys(official_awards, None)
    for key in presenters_all:
        presenters_all[key] = []
    
    src_path = './gg' + str(year) + '_classified.json'
    with open(src_path, 'r') as fin:
        for tweet in fin.readlines():
            tweet = json.loads(tweet)
            words = tokenizer.tokenize(tweet['text'])
            text = ' '.join(words)
            if not ('present' in text or 'Present' in text):
                continue
            names = get_human_names(text)
            stop_words = ['golden', 'globes', 'oscar', 'hollywood', 'congrats', 'represent', 'didn', 'comedy', 'hbo', 'would', 'deadline', 'rt', 'award', 'win']
            for name in names:
                name_lower = name.lower()
                if not any(w in name_lower for w in stop_words) and len(name.split()) < 4:
                    presenters_all[tweet['category']].append(name_lower)

    presenters = dict().fromkeys(official_awards, None)
    for key in presenters:
        presenter_counter = Counter(presenters_all[key])
        top10 = presenter_counter.most_common(10)
        presenters[key] = []
        if len(top10) > 0:
            for k, v in top10:
                presenters[key].append(k)
    
    return presenters

def get_best_dressed(year):
    src_path = './gg' + str(year) + '_dress.json'
    tweets = tweets_to_words(src_path)
    keywords = ['best', 'best-dressed', 'great', 'good', 'amazing', 'beautiful', 'gorgeous']
    stop_words = ['Golden', 'golden', 'Globes', 'globes', 'Dress', 'dress', 'Best', 'best']
    all_names = []

    for tweet in tweets:
        text = ' '.join(tweet)
        text_lower = text.lower()
        if not any(w in text_lower for w in keywords):
            continue
        names = get_human_names(text)
        for name in names:
            if any(w in name for w in stop_words):
                continue
            if len(name.split()) < 4:
                all_names.append(name)

    names_counter = Counter(all_names)
    top1 = names_counter.most_common(1)
    return top1[0][0]

def get_worst_dressed(year):
    src_path = './gg' + str(year) + '_dress.json'
    tweets = tweets_to_words(src_path)
    keywords = ['worst', 'worst-dressed', 'bad', 'weird', 'terrible', 'gross']
    stop_words = ['Golden', 'golden', 'Globes', 'globes', 'Dress', 'dress', 'Worst', 'worst']
    all_names = []

    for tweet in tweets:
        text = ' '.join(tweet)
        text_lower = text.lower()
        if not any(w in text_lower for w in keywords):
            continue
        names = get_human_names(text)
        for name in names:
            if any(w in name for w in stop_words):
                continue
            if len(name.split()) < 4:
                all_names.append(name)

    names_counter = Counter(all_names)
    top1 = names_counter.most_common(1)
    return top1[0][0]

def get_most_humorous(year):
    src_path = './gg' + str(year) + '_all.json'
    tweets = tweets_to_words(src_path)
    if len(tweets) > 200000:
        tweets = tweets[:200000]
    keywords = ['funny', 'joke', 'haha', 'hilarious']
    stop_words = ['Golden', 'golden', 'Globes', 'globes', 'Didn', 'didn']
    all_names = []

    for tweet in tweets:
        text = ' '.join(tweet)
        text_lower = text.lower()
        if not any(w in text_lower for w in keywords):
            continue
        names = get_human_names(text)
        for name in names:
            if any(w in name for w in stop_words):
                continue
            if len(name.split()) < 4:
                all_names.append(name)

    names_counter = Counter(all_names)
    most_humorous = []
    for key, val in names_counter.most_common(3):
        most_humorous.append(key)
    return most_humorous

def categories_init(year):
    if year > 2016:
        official_awards = OFFICIAL_AWARDS_1819
    else:
        official_awards = OFFICIAL_AWARDS_1315

    for award in official_awards:
        if 'award' in award:
            award_words = award.split()
            AWARD_CATEGORIES[award_words[-2]] = [award]
            continue
        if 'animated' in award:
            AWARD_CATEGORIES['animated'].append(award)
            continue
        if 'foreign' in award:
            AWARD_CATEGORIES['foreign'].append(award)
            continue
        if 'screenplay' in award:
            AWARD_CATEGORIES['screenplay'].append(award)
            continue
        if 'director' in award:
            AWARD_CATEGORIES['director'].append(award)
            continue
        if 'song' in award:
            AWARD_CATEGORIES['song'].append(award)
            continue
        if 'score' in award:
            AWARD_CATEGORIES['score'].append(award)
            continue
        category = ''
        if 'actor' in award:
            category = 'actor'
        elif 'actress' in award:
            category = 'actress'
        else:
            category = 'other'
        if 'drama' in award:
            category += '-drama'
        elif 'comedy' in award:
            category += '-comedy'
        else:
            category += '-other'
        AWARD_CATEGORIES[category].append(award)

def recognize_award(text):
    text = text.lower()
    if 'tv' in text:
        text.replace('tv', 'television')
    if 'miniseries' in text:
        text.replace('miniseries', 'mini-series')
    if 'mini series' in text:
        text.replace('mini series', 'mini-series')
    words = text.split()
    category = ''

    for key in AWARD_CATEGORIES:
        if (not '-' in key) and (key in words):
            category = key
            break
    else:
        if 'actor' in words:
            category = 'actor'
        elif 'actress' in words:
            category = 'actress'
        else:
            category = 'other'
        if 'drama' in words:
            category += '-drama'
        elif 'comedy' in words:
            category += '-comedy'
        else:
            category += '-other'
        
    if category == 'other-other' and not 'television' in words:
        return 'none'

    if len(AWARD_CATEGORIES[category]) == 1:
        return AWARD_CATEGORIES[category][0]
    
    tweet_words = set()
    stop_words = ['-', 'a', 'an', 'by', 'for', 'in', 'or']
    for w in words:
        if not w in stop_words:
            tweet_words.add(w)

    closet_award, max_len, award_len = '', 0, 99
    for award in AWARD_CATEGORIES[category]:
        award_words = set()
        temp = award.split()
        for w in temp:
            if not w in stop_words:
                award_words.add(w)
        shared_words = award_words.intersection(tweet_words)
        if len(shared_words) > max_len:
            max_len = len(shared_words)
            closet_award = award
            award_len = len(award_words)
        elif len(shared_words) == max_len:
            if award_len > len(award_words):
                award_len = len(award_words)
                closet_award = award
    
    return closet_award

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    global YEAR
    YEAR = int(input('Which year: '))

    categories_init(YEAR)
    extract_text(YEAR)
    award_filter(YEAR)

    src_path = './gg' + str(YEAR) + '_award.json'
    dest_path = './gg' + str(YEAR) + '_classified.json'
    with open(src_path, 'r') as fin:
        with open(dest_path, 'w') as fout:
            for tweet in fin.readlines():
                tweet = json.loads(tweet)
                category = recognize_award(tweet['text'])
                if category != 'none':
                    new_tweet = {}
                    new_tweet['text'] = tweet['text']
                    new_tweet['category'] = category
                    json.dump(new_tweet, fout)
                    fout.write('\n')

    host_filter(YEAR)
    dress_filter(YEAR)

    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    pre_ceremony()

    results = {}

    print('Getting winners ...')
    winners = get_winner(YEAR)
    print('Getting winners complete.')

    print('Getting nominees ...')
    nominees = get_nominees(YEAR)
    print('Getting nominees complete.')

    print('Getting presenters ...')
    presenters = get_presenters(YEAR)
    print('Getting presenters complete.')

    print('Getting hosts ...')
    hosts = get_hosts(YEAR)
    print('Getting hosts complete.')

    results['hosts'] = hosts
    official_awards = OFFICIAL_AWARDS_1819 if YEAR > 2016 else OFFICIAL_AWARDS_1315
    award_data = dict().fromkeys(official_awards, None)
    for key in award_data:
        award_data[key] = {}
        award_data[key]['nominees'] = nominees[key]
        temp = []
        for presenter in presenters[key]:
            if presenter != winners[key]:
                temp.append(presenter)
        award_data[key]['presenters'] = temp
        award_data[key]['winner'] = winners[key]
    results['award_data'] = award_data

    dest_path = './gg' + str(YEAR) + 'results.json'
    with open(dest_path, 'w') as fout:
        json.dump(results, fout)
    
    src_path = './gg' + str(YEAR) + '_dress.json'
    tweets = tweets_to_list(src_path)
    if len(tweets) > 5000:
        tweets = tweets[:5000]
    rc_info = red_carpet_process(tweets)
    rc_out = readable_red_carpet(rc_info)
    most_humorous = get_most_humorous(YEAR)

    dest_path = './gg' + str(YEAR) + 'results.txt'
    with open(dest_path, 'w') as fout:
        fout.write('Host: ')
        is_first = True
        for host in hosts:
            if is_first:
                fout.write(host)
                is_first = False
            else:
                fout.write(', ' + host)
        fout.write('\n')

        for key in award_data:
            fout.write('\nAward: ' + key)
            fout.write('\nPresenters: ')
            is_first = True
            for presenter in award_data[key]['presenters']:
                if is_first:
                    fout.write(presenter)
                    is_first = False
                else:
                    fout.write(', ' + presenter)

            fout.write('\nNominees: ')
            is_first = True
            for nominee in award_data[key]['nominees']:
                if is_first:
                    fout.write('"' + nominee + '"')
                    is_first = False
                else:
                    fout.write(', "' + nominee + '"')

            fout.write('\nWinner: "' + award_data[key]['winner'] + '"')
            fout.write('\n')
        fout.write('\n')

        fout.write(rc_out)

        fout.write('\nTop 3 Most Humorous People: ')
        is_first = True
        for person in most_humorous:
            if is_first:
                fout.write(person)
                is_first = False
            else:
                fout.write(', ' + person)

    print('\nResults generated.', '\nJSON format: gg%dresults.json' % YEAR, '\nHuman-readable format: gg%dresults.txt' % YEAR)

    return

if __name__ == '__main__':
    main()
