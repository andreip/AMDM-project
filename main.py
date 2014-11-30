import numpy as np
import random
import time

from plots import plot1, plot2, plot3
from helpers import timing

filename = 'tweets_15m.txt'
tweets_max = 1000**2 * 15
read_chunk = 1000**2

def process_tweet(tweet):
    if not tweet:
        return None
    return set(tweet.strip('\n').split('\t'))

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
                for word in process_tweet(raw_tweet):
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

@timing
def get_tweets(filename):
    query_length = 1000
    count = 0
    q_tweets = []
    db_tweets = []
    with open(filename) as f:
        while count < query_length:
            count += 1
            tweet = process_tweet(f.readline())
            q_tweets.append(tweet)
        while True:
            tweet = process_tweet(f.readline())
            if not tweet:
                break
            db_tweets.append(tweet)
    return q_tweets, db_tweets

q_tweets, db_tweets = get_tweets(filename)

def get_db_tweets(filename):
    query_length = 1000
    count = 0
    query_tweets = []
    db_tweets = None
    with open(filename) as f:
        while count < query_length:
            count += 1
            f.readline()
        while True:
            tweet = process_tweet(f.readline())
            if not tweet:
                break
            yield tweet

def angle_dist(x, y, terms):
    common_terms = set(x) & set(y)
    n_common_terms = sum([1 if t in terms else 0 for t in common_terms])
    n_x = sum([1 if t in terms else 0 for t in x])
    n_y = sum([1 if t in terms else 0 for t in y])
    # Edge case, just return pi/2 as it's division by 0.
    if n_x == 0 or n_y == 0:
        return np.pi / 2
    return np.arccos(n_common_terms / np.sqrt(n_x * n_y))

def bf_nearest_neigbors(q, db_tweets, terms):
    """Find the NN of a query q."""
    best_angle = np.pi / 2
    best_nn = None
    for db_tweet in db_tweets:
        angle = angle_dist(q, db_tweet, terms)
        if angle < best_angle:
            best_angle = angle
            best_nn = db_tweet
    return best_nn, best_angle

@timing
def bf_algorithm(terms):
    for q_tweet in q_tweets:
        nn_tweet, nn_angle = bf_nearest_neigbors(q_tweet, db_tweets, terms)

def main():
    random.seed(time.time())

    tweet_terms = get_words_appearances()
    print 'Total number of words are', len(tweet_terms)
    terms_in_tweets_count = get_terms_in_k_tweets(tweet_terms)
    print 'Total number of counts are', len(terms_in_tweets_count)
    print 'Sorting tweet terms by appearances.'
    sorted_terms = sorted(tweet_terms.iteritems(), key=lambda x: x[1],
                          reverse=True)

    # Plots for task1. Don't need to run again.
    #plot1(terms_in_tweets_count)
    #plot2(terms_in_tweets_count)
    #plot3(tweet_terms)

    print 'Full NN search with all terms.'
    bf_algorithm(tweet_terms)
    print '== d-frequent =='
    for j in range(0,15,2):
        d = 100 * 2**j
        print 'j=%d, d=%d' % (j, d)
        terms = dict(sorted_terms[:d])
        bf_algorithm(terms)
    print '== d-infrequent =='
    for j in range(0,15,2):
        d = 100 * 2**j
        print 'j=%d, d=%d' % (j, d)
        terms = dict(sorted_terms[-d:])
        bf_algorithm(terms)
    print '== d-random =='
    for j in range(0,15,2):
        d = 100 * 2**j
        print 'j=%d, d=%d' % (j, d)
        terms = dict(random.sample(sorted_terms, d))
        bf_algorithm(terms)

if __name__ == '__main__':
    main()
