

#hashtags commonly used
rc_hashtags = [""]
#words that are associated with red carpet
rc_words = ["red", "carpet", 
            "stunning", "beautiful", "gorgeous", "ravishing", 
            "dress", "gown", "shoes", "heels",
            "suit", "tuxedo"]
            
def tweet_contains(tweet, things):
    if isinstance(tweet, things):
        for elem in things:
            if elem in tweet.text:
                return true
    else:
        return things in tweet.text
    return false
            
def relevent_tweet(tweet):
    if tweet_contains(tweet, rc_hashtags) or tweet_contains(tweet, rc_words):
        return true
    return false


        
