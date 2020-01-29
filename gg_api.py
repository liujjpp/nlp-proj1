'''Version 0.35'''
import json
import spacy
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from nltk.tokenize import RegexpTokenizer
from preprocess import *

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']
OFFICIAL_AWARDS = []
AWARD_CATEGORIES = {'animated': [], 'foreign': [], 'screenplay': [], 'director': [], 'song': [], 
                    'score': [], 'actor-drama': [], 'actress-drama': [], 'other-drama': [], 'actor-comedy': [], 
                    'actress-comedy': [], 'other-comedy': [], 'actor-other': [], 'actress-other': [], 'other-other': []}
YEAR = 2020
NLP = spacy.load('en_core_web_sm')

def get_human_names(text):
    '''Extract human names from tweet text.
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
    src_path = './gg' + str(year) + '.json'
    tweets = tweets_to_words(src_path)
    hosts = []
    all_names = []
    stop_words = ['Golden', 'golden', 'Hollywood', 'hollywood']

    for tweet in tweets:
        if not ('host' in tweet or 'Host' in tweet):
            continue
        if 'next' in tweet or 'Next' in tweet:
            continue
        names = get_human_names(' '.join(tweet))
        for name in names:
            name_list = name.split()
            if name_list[0] == 'RT':
                continue
            if len(name_list) > 1 and len(name_list) < 3 and not any(w in name for w in stop_words):
                all_names.append(name.lower())

    name_counter = Counter(all_names)
    top2 = name_counter.most_common(2):
    hosts.append(top2[0[0]])
    if top2[1][1] > top2[0][1] * 0.4:
        hosts.append(top2[1][0])
    
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    best_words = ['Best', 'best', 'BEST']
    award_words1 = ['actor', 'actress', 'animated', 'comedy', 'director', 'drama', 'feature', 'film', 'language', 'mini-series', 
                    'motion', 'musical', 'performance', 'picture', 'role', 'score', 'screenplay', 'series', 'song', 'television',
                    'Actor', 'Actress', 'Animated', 'Comedy', 'Director', 'Drama', 'Feature', 'Film', 'Language', 'Mini-series',
                    'Motion', 'Musical', 'Performance', 'Picture', 'Role', 'Score', 'Screenplay', 'Series', 'Song', 'Television',
                    'miniseries', 'Miniseries']
    award_words2 = ['-', 'a', 'an', 'any', 'best', 'by', 'for', 'foreign', 'in', 'limited',
                    'made', 'or', 'original', 'supporting', 'A', 'An', 'Any', 'Best', 'By', 'For',
                    'Foreign', 'In', 'Limited', 'Made', 'Or', 'Original', 'Supporting', 'mini', 'Mini']
    characters = [' B ', ' C ', ' D ', ' E ', ' F ', ' G ', ' H ', ' I ', ' J ', ' K ', ' L ', ' M ',
                  ' N ', ' O ', ' P ', ' Q ', ' R ', ' S ', ' T ', ' U ', ' V ', ' W ', ' X ', ' Y ', ' Z ',
                  ' b ', ' c ', ' d ', ' e ', ' f ', ' g ', ' h ', ' i ', ' j ', ' k ', ' l ', ' m ',
                  ' n ', ' o ', ' p ', ' q ', ' r ', ' s ', ' t ', ' u ', ' v ', ' w ', ' x ', ' y ', ' z ']
    
    src_path = './gg' + str(year) + '_award.json'
    tweets = tweets_to_words(src_path)
    awards = []
    award_contains_human_name = []

    for tweet in tweets:
        if 'Award' in tweet or 'award' in tweet:
            text = ' '.join(tweet)
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

        if 'Best' in tweet:
            first_index = tweet.index('Best')
        elif 'best' in tweet:
            first_index = tweet.index('best')
        elif 'BEST' in tweet:
            first_index = tweet.index('BEST')
        else:
            continue

        award_name = ['best']
        for i in range(first_index + 1, len(tweet)):
            if tweet[i] in award_words1 or tweet[i] in award_words2:
                award_name.append(tweet[i].lower())
            elif tweet[i] in best_words:
                if len(award_name) > 3 and len(award_name) < 20 and not award_name[-1] in award_words2:
                    awards.append(' '.join(award_name))
                award_name = ['best']
            else:
                break
        if len(award_name) > 3 and len(award_name) < 20 and not award_name[-1] in award_words2:
            awards.append(' '.join(award_name))
    
    # make names closer to official names
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
        if 'best actor' in award:
            new_award = new_award.replace('best actor', 'best performance by an actor')
        if 'best actress' in award:
            new_award = new_award.replace('best actress', 'best performance by an actress')
        if 'actor' in award and not 'actor in a' in award:
            if 'actor in' in award:
                new_award = new_award.replace('actor in', 'actor in a')
            else:
                new_award = new_award.replace('actor', 'actor in a')
        if 'actress' in award and not 'actress in a' in award:
            if 'actress in' in award:
                new_award = new_award.replace('actress in', 'actress in a')
            else:
                new_award = new_award.replace('actress', 'actress in a')
        if 'motion picture' in award:
            if award[-14:] != 'motion picture' and not 'motion picture made' in award:
                new_award = new_award.replace('motion picture', 'motion picture -')
        if new_award != award:
            awards.append(new_award)

    new_awards = []
    filter_words = ['- -', 'tv', 'best actor', 'best actress', 'in a -']
    for award in awards:
        if not any(w in award for w in filter_words):
            if 'actor' in award and not 'actor in a' in award:
                continue
            if 'actress' in award and not 'actress in a' in award:
                continue
            if ('actor' in award or 'actress' in award) and not '-' in award and not 'motion picture' in award:
                continue
            if award.count('best') > 1:
                continue
            if 'motion picture' in award and award[-14:] != 'motion picture':
                if not ('motion picture -' in award or 'motion picture m' in award):
                    continue
            if 'picture' in award and not 'motion picture' in award:
                new_word = award.replace('picture', 'motion picture')
                new_awards.append(new_word)
            else:
                new_awards.append(award)
    # for i in range(len(new_awards)):
    #     if new_awards[i].count('-') > 1:
    #         new_word = new_awards[i][::-1]
    #         new_awards[i] = new_word.replace('-', '', 1).replace('  ', ' ')
    #         new_awards[i] = new_awards[i][::-1]
    
    awards_counter = Counter(new_awards)
    award_contains_human_name_counter = Counter(award_contains_human_name)
    # print(len(awards_counter))

    # merge similar award names
    for key in awards_counter.keys():
        if '-' in key:
            similar = key.replace(' - ', ' ')
            if similar in awards_counter.keys():
                awards_counter[key] += awards_counter[similar]
                awards_counter[similar] = 0
        if ' or ' in key:
            similar = key.replace(' or ', ' ')
            if similar in awards_counter.keys():
                awards_counter[key] += awards_counter[similar]
                awards_counter[similar] = 0

    # with open('./awards.txt', 'w') as fout:
    #     for key in awards_counter.keys():
    #         if awards_counter[key] > 5:
    #             fout.write(key + ' ' + str(awards_counter[key]))
    #             fout.write('\n')

    awards = []
    for key, val in awards_counter.most_common(26):
        awards.append(key)
    award_contains_name = award_contains_human_name_counter.most_common(1)
    awards.append(award_contains_name[0][0])
    # print(len(awards))
    
    # visited = []
    # for i in range(len(awards)):
    #     if awards[i] in visited:
    #         continue
    #     flag = False
    #     for j in range(i + 1, len(awards)):
    #         if SequenceMatcher(None, awards[i], awards[j]).ratio() >= 0.9:
    #             flag = True
    #             visited.append(awards[j])
    #             print(awards[j])
    #     if flag:
    #         print(awards[i])
    #         print('-------------')

    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    official_awards = OFFICIAL_AWARDS_1819 if year > 2016 else OFFICIAL_AWARDS_1315
    tokenizer = RegexpTokenizer(r'-|[A-Za-z]+')
    
    presenters_sets = dict().fromkeys(official_awards, None)
    for key in presenters_sets:
        presenters_sets[key] = set()
    
    src_path = './gg' + str(year) + '_categories.json'
    with open(src_path, 'r') as fin:
        for tweet in fin.readlines():
            tweet = json.loads(tweet)
            words = tokenizer.tokenize(tweet['text'])
            text = ' '.join(words)
            if not ('present' in text or 'Present' in text):
                continue
            names = get_human_names(text)
            stop_words = ['golden', 'globes', 'oscar', 'hollywood', 'represent', 'didn', 'comedy']
            for name in names:
                name_lower = name.lower()
                if not any(w in name_lower for w in stop_words) and len(name.split()) < 3:
                    presenters_sets[tweet['category']].add(name_lower)

    presenters = dict().fromkeys(official_awards, None)
    for key in presenters:
        presenters[key] = []
        for name1 in presenters_sets[key]:
            for name2 in presenters_sets[key]:
                if name1 in name2 and name1 != name2:
                    break
            else:
                presenters[key].append(name1)
    
    return presenters

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
    YEAR = int(input('Which year: '))

    categories_init(YEAR)

    award_filter(YEAR)
    src_path = './gg' + str(YEAR) + '_award.json'
    dest_path = './gg' + str(YEAR) + '_categories.json'
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
    return

if __name__ == '__main__':
    main()
