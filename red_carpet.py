import re
import statistics

simple_case = re.compile(' ([A-Z]\S+ [A-Z]\S+?) ')

rc_hashtags = ["#redcarpet"]
#words that are associated with red carpet
rc_neutral = ["red", "carpet", "dress", "gown", "shoes", "heels",
              "suit", "tuxedo"]
rc_positive = ["stunning", "beautiful", "gorgeous", "ravishing", "handsome"]
rc_negative = ["ugly", "nasty", "poor", "crappy", "rag"]
rc_words = rc_neutral + rc_positive + rc_negative

def tweet_contains(tweet, things):
    for elem in things:
        if elem in tweet['text'].split(" "):
            return True
    return False
            
def relevent_tweet(tweet):
    if tweet_contains(tweet, rc_hashtags) or tweet_contains(tweet, rc_words):
        return True
    return False

#returns a list of names
def loose_person_detection(tweet):
    names = []
    for elem in simple_case.findall(tweet['text']):
        if "Globe" not in elem and "Golden" not in elem and "Awards" not in elem:
            names.append(elem)
    return names

def get_dress_sentiment(tweet):
     return float(int(tweet_contains(tweet, rc_positive)) - int(tweet_contains(tweet, rc_negative)))

def ordered_loose_person_detection(tweets):
    name_data = []
    counts = []
    sentiments = []
    for tweet in tweets:
        names = loose_person_detection(tweet)
        sentiment = get_dress_sentiment(tweet)
        for name in names:
            if name in name_data:
                idx = name_data.index(name)
                counts[idx]+=1
                sentiments[idx]+=[sentiment]
            else:
                name_data.append(name)
                counts.append(1)
                sentiments.append([sentiment])
    avg_sentiment = [1.0*x/y for x,y in sorted(zip([sum(x) for x in sentiments], counts))]
    std_sentiment = [1.0*x/y for x,y in sorted(zip([statistics.stdev(x) if len(x)>1 else 0 for x in sentiments], \
                                                   counts), reverse=True)]
    return [(y,x) for x,y in sorted(zip(counts, name_data), reverse=True)],\
           [(y,x) for x,y in sorted(zip(avg_sentiment, name_data), reverse=True)],\
           [(y,x) for x,y in sorted(zip(std_sentiment, name_data), reverse=True)]

def red_carpet_process(tweets):
    rc_info = {}
    discussion, avg_sentiment, std_sentiment = ordered_loose_person_detection(tweets)
    rc_info['most discussed'] = discussion[0][0]
    rc_info['highest_sentiment'] = avg_sentiment[-1][0]
    rc_info['lowest_sentiment'] = avg_sentiment[0][0]
    rc_info['variant_sentiment'] = std_sentiment[0][0]
    return rc_info

def red_carpet_best_dressed(rc_info):
    return rc_info['highest_sentiment']

def red_carpet_worst_dressed(rc_info):
    return rc_info['lowest_sentiment']

def red_carpet_most_discussed(rc_info):
    return rc_info['most discussed']

def red_carpet_most_controversial(rc_info):
    return rc_info['variant_sentiment']

def red_carpet_image_of_best_dressed(rc_info):
    raise ValueError("NOT IMPLEMENTED")

def red_carpet_image_of_worst_dressed(rc_info):
    raise ValueError("NOT IMPLEMENTED")
