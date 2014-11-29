import numpy as np
import time

from plots import plot1, plot2, plot3
from helpers import timing

filename = 'tweets_15m.txt'
tweets_max = 1000**2 * 15
read_chunk = 1000**2

@timing
def get_words_appearances():
    print 'Going through all words in file'
    tweet_terms = {}
    with open(filename) as f:
        read_tweets = 0
        while read_tweets < tweets_max:
            tweets = f.readlines(read_chunk)
            # Tweets are finished.
            if not tweets:
                print 'exit as no more tweets to read'
                break
            read_tweets += len(tweets)
            for raw_tweet in tweets:
                tweet = raw_tweet.strip('\n').split('\t')
                for word in set(tweet):
                    tweet_terms[word] = tweet_terms.get(word, 0) + 1
    return tweet_terms

@timing
def get_terms_in_k_tweets(tweet_terms):
    print 'Counting terms in k tweets'
    max_index = 0
    terms_in_tweets_count = {}
    for (word,n) in tweet_terms.iteritems():
        terms_in_tweets_count[n] = terms_in_tweets_count.get(n, 0) + 1
        max_index = max(max_index, n)
    return terms_in_tweets_count

tweet_terms = get_words_appearances()
print 'Total number of words are', len(tweet_terms)
terms_in_tweets_count = get_terms_in_k_tweets(tweet_terms)
print 'Total number of counts are', len(terms_in_tweets_count)

plot1(terms_in_tweets_count)
plot2(terms_in_tweets_count)
plot3(tweet_terms)
