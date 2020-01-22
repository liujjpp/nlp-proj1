from collections import Counter
from difflib import SequenceMatcher
from preprocess import *

def get_awards(src_path='./gg2020_best.json'):
    best_words = ['Best', 'best', 'BEST']
    award_words1 = ['Picture', 'picture', 'Drama', 'drama', 'Musical', 'musical', 'Movie', 'movie',
                    'Film', 'film', 'Comedy', 'comedy', 'Language', 'language', 'Animated', 'animated']
    award_words2 = ['Motion', 'motion', 'Foreign', 'foreign', 'Director', 'director', 'Actor', 'actor', 'Actress', 'actress', 
                    'Supporting', 'supporting', 'Screenplay', 'screenplay', 'Original', 'original', 'Score', 'score', 'Song', 'song', 
                    'Television', 'television', 'Series', 'series', 'Miniseries', 'miniseries', 'Limited', 'limited', 'TV', 'tv', 
                    'Or', 'or', 'In', 'in', 'A', 'a', 'An', 'an', '-']
    
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
                if len(award_name) > 3 and len(award_name) < 13 and not award_name[-1] in award_words2:
                    awards.append(' '.join(award_name))
                award_name = ['best']
            else:
                break
        if len(award_name) > 3 and len(award_name) < 13 and not award_name[-1] in award_words2:
            awards.append(' '.join(award_name))
    
    # make names closer to standard names
    for award in awards:
        if 'in a' in award:
            awards.append(award.replace('in a', '-'))
        if '- -' in award:
            awards.append(award.replace('- -', '-'))
        if 'tv' in award:
            awards.append(award.replace('tv', 'television'))
        if 'movie' in award:
            awards.append(award.replace('movie', 'film'))
        if 'limited series' in award:
            awards.append(award.replace('limited series', 'miniseries'))
        elif 'limited television series' in award:
            awards.append(award.replace('limited television series', 'miniseries'))
        if 'musical comedy' in award:
            awards.append(award.replace('musical comedy', 'musical or comedy'))
        elif 'comedy musical' in award:
            awards.append(award.replace('comedy musical', 'musical or comedy'))
        elif 'comedy or musical' in award:
            awards.append(award.replace('comedy or musical', 'musical or comedy'))

    new_awards = []
    filter_words = ['in a', '- -', 'tv', 'movie', 'limited series', 'limited television series', 
                    'musical comedy', 'comedy musical', 'comedy or musical']
    for award in awards:
        if not any(w in award for w in filter_words):
            if 'film' in award and not 'television film' in award:
                new_word = award.replace('film', 'motion picture')
                new_awards.append(new_word)
            elif 'picture' in award and not 'motion picture' in award:
                new_word = award.replace('picture', 'motion picture')
                new_awards.append(new_word)
            else:
                new_awards.append(award)
    for i in range(len(new_awards)):
        if new_awards[i].count('-') > 1:
            new_word = new_awards[i][::-1]
            new_awards[i] = new_word.replace('-', '', 1).replace('  ', ' ')
            new_awards[i] = new_awards[i][::-1]
    
    awards = Counter(new_awards)
    print(len(awards))

    # merge similar award names
    for key in awards.keys():
        if '-' in key:
            similar = key.replace('-', '').replace('  ', ' ')
            if similar in awards.keys():
                awards[key] += awards[similar]
                awards[similar] = 0
        if ' or ' in key:
            similar = key.replace(' or ', ' ')
            if similar in awards.keys():
                awards[key] += awards[similar]
                awards[similar] = 0
        if 'limited series' in key:
            similar = key.replace('limited series', 'miniseries')
            if similar in awards.keys():
                awards[similar] += awards[key]
                awards[key] = 0

    # with open('./awards.txt', 'w') as fout:
    #     for key in awards.keys():
    #         if awards[key] > 5:
    #             fout.write(key + ' ' + str(awards[key]))
    #             fout.write('\n')

    result = []
    for key in awards.keys():
        if awards[key] > 5:
            result.append(key)
    
    # visited = []
    # for i in range(len(result)):
    #     if result[i] in visited:
    #         continue
    #     flag = False
    #     for j in range(i + 1, len(result)):
    #         if SequenceMatcher(None, result[i], result[j]).ratio() >= 0.9:
    #             flag = True
    #             visited.append(result[j])
    #             print(result[j])
    #     if flag:
    #         print(result[i])
    #         print('-------------')

    return result


if __name__ == "__main__":
    # get_awards()