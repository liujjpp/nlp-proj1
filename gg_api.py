'''Version 0.35'''
import json
from collections import Counter
from difflib import SequenceMatcher
from preprocess import *

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

def get_human_names(text):
    '''Extract human names from tweet text.
    Returns a list of strings'''
    names = []

    return names

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
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
    
    src_path = './gg' + str(year) + '.json'
    tweets = tweets_to_words(src_path)
    awards = []

    for tweet in tweets:
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
        if 'best actor' in award:
            new_award = new_award.replace('best actor', 'best performance by an actor')
        if 'best actress' in award:
            new_award = new_award.replace('best actress', 'best performance by an actor')
        if 'actor' in award and not 'actor in a' in award:
            if 'actor in' in award:
                new_award = new_award.replace('actor in', 'actor in a')
            else:
                new_award = new_award.replace('actor', 'actor in a')
        if 'actress' in award and not 'actress in a' in award:
            if 'actress in' in award:
                new_award = new_award.replace('actress in', 'actor in a')
            else:
                new_award = new_award.replace('actress', 'actress in a')
        if 'motion picture' in award:
            if award[-14:] != 'motion picture' and not 'motion picture made' in award:
                new_award = new_award.replace('motion picture', 'motion picture -')
        if new_award != award:
            awards.append(new_award)

    new_awards = []
    filter_words = ['- -', 'tv', 'best actor', 'best actress']
    for award in awards:
        if not any(w in award for w in filter_words):
            if 'actor' in award and not 'actor in a' in award:
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

    with open('./awards.txt', 'w') as fout:
        for key in awards_counter.keys():
            if awards_counter[key] > 5:
                fout.write(key + ' ' + str(awards_counter[key]))
                fout.write('\n')

    awards = []
    for key, val in awards_counter.most_common(35):
        awards.append(key)
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
    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
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
