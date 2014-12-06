import math
import random
import sys
import time

#from plots import plot1, plot2, plot3
from helpers import timing

filename = 'tweets_15m.txt'
tweets_max = 1000**2 * 15
read_chunk = 1000**2

def process_tweet(tweet):
    if not tweet:
        return None
    return set(tweet.strip('\n').split('\t'))

@timing
def get_terms_appearances(tweets):
    tweet_terms = {}
    for tweet in tweets:
        for word in tweet:
            tweet_terms[word] = tweet_terms.get(word, 0) + 1
    return tweet_terms

@timing
def get_terms_in_k_tweets(tweet_terms):
    print 'Counting terms in k tweets'
    max_index = 0
    terms_in_k_tweets = {}
    for (word,n) in tweet_terms.iteritems():
        terms_in_k_tweets[n] = terms_in_k_tweets.get(n, 0) + 1
        max_index = max(max_index, n)
    return terms_in_k_tweets

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

def angle_dist(x, y, terms=None):
    common_terms = x & y
    if terms:
        n_common_terms = sum([1 if t in terms else 0 for t in common_terms])
        n_x = sum([1 if t in terms else 0 for t in x])
        n_y = sum([1 if t in terms else 0 for t in y])
    else:
        n_common_terms = len(common_terms)
        n_x = len(x)
        n_y = len(y)
    # Edge case, just return pi/2 as it's division by 0.
    if n_x == 0 or n_y == 0:
        return math.pi / 2
    return math.acos(n_common_terms / math.sqrt(n_x * n_y))

@timing
def bf_algorithm(q_tweets, db_tweets):
    # We'll store here all the indexes of the NN
    # of the queries.
    nn_tweets_idx = [-1] * len(q_tweets)
    # Bigger than pi/2 which is the max angle.
    nn_tweets_angles = [4] *  len(q_tweets)
    for j, db_tweet in enumerate(db_tweets):
        #print float(j)/len(db_tweets)*100," percent complete         \r",
        for i, q_tweet in enumerate(q_tweets):
            angle = angle_dist(q_tweet, db_tweet)
            if angle < nn_tweets_angles[i]:
                nn_tweets_angles[i] = angle
                nn_tweets_idx[i] = j
    return nn_tweets_idx

@timing
def construct_term_indexes(tweets):
    print 'Constructing index of terms for %d tweets' % len(tweets)
    term_indexes = {}
    for i, tweet in enumerate(tweets):
        for term in tweet:
            indexes = term_indexes.get(term, [])
            indexes.append(i)
            term_indexes[term] = indexes
    return term_indexes

@timing
def speedy_algorithm(q_tweets, db_tweets):
    # We'll store here all the indexes of the NN
    # of the queries.
    nn_tweets_idx = [-1] * len(q_tweets)
    # We first need to build up an index. The dictionary will have
    # { key : value } = {term : [index_tweet1, index_tweet10, ... ] },
    # storing an array of all indexes where the term appears in the
    # db tweets.
    db_term_index = construct_term_indexes(db_tweets)
    # Now we can go through each query and check which index appears the
    # most in the query's terms by doing a reunion over the query's term's
    # indexes and seeing which index in the db tweets appears the most.
    for i, q_tweet in enumerate(q_tweets):
        indexes = []
        for term in q_tweet:
            indexes += db_term_index.get(term, [])
        # If there are no indexes with at least one term, we just skip
        # the tweet, no NN found for it, leave -1 index.
        if len(indexes) == 0:
            continue
        # Get the element with the smallest angle.
        nn_tweets_idx[i] = min(set(indexes), key=lambda x: angle_dist(db_tweets[x], q_tweet))
    return nn_tweets_idx

@timing
def speedy_algorithm2(q_tweets, db_tweets):
    # We'll store here all the indexes of the NN
    # of the queries.
    nn_tweets_idx = [-1] * len(q_tweets)
    # Sort db tweets by their number of terms.
    time1 = time.time()
    db_tweets_s = sorted(enumerate(db_tweets), key=lambda x: len(x[1]))
    time2 = time.time()
    print '%s function took %0.3f ms' % ('sorting tweets by len', (time2-time1)*1000.0)
    print 'max length of tweet is', len(db_tweets_s[-1][1])

    for i, q_tweet in enumerate(q_tweets):
        print float(i)/len(q_tweets)*100," percent complete         \r"
        best_angle, best_idx, stop_len = None, None, 150
        for j, db_tweet in db_tweets_s:
            # Try stopping early in case going further does not give
            # better results.
            if len(db_tweet) > stop_len:
                print 'stopping early at length', len(db_tweet)
                break
            angle = len(q_tweet & db_tweet) / math.sqrt(len(db_tweet))
            if angle > best_angle or not best_angle:
                best_angle = angle
                best_idx = j
                if best_angle:
                    stop_len = int(len(q_tweet) / best_angle)**2
                    print 'stop len updated to', stop_len
        nn_tweets_idx[i] = best_idx
    return nn_tweets_idx


@timing
def filter_terms(tweets, terms):
    tweets_new = []
    for t in tweets:
        t_new = set(filter(terms.get, t))
        if t_new:
            tweets_new.append(t_new)
    return tweets_new

def main(algorithm):
    random.seed(time.time())

    # Get all tweets in memory first.
    q_tweets, db_tweets = get_tweets(filename)

    # Store the appearances of terms. These will help to
    # get the d-frequest, d-infrequest and d-random.
    tweet_terms = get_terms_appearances(db_tweets)
    print 'Total number of terms are', len(tweet_terms)
    terms_in_k_tweets = get_terms_in_k_tweets(tweet_terms)
    print 'Total number of k tweets are', len(terms_in_k_tweets)
    print 'Sorting tweet terms by appearances.'
    print time.time()
    sorted_terms = sorted(tweet_terms.iteritems(), key=lambda x: x[1],
                          reverse=True)
    print time.time()
    sys.stdout.flush()

    # Plots for task1. Don't need to run again.
    #plot1(terms_in_k_tweets)
    #plot2(terms_in_k_tweets)
    #plot3(tweet_terms)

    print '== with all terms =='
    nn_tweets_idx = algorithm(q_tweets, db_tweets)
    print nn_tweets_idx

    print '== d-frequent =='
    for j in range(0,15,2):
        d = 100 * 2**j
        print 'j=%d, d=%d' % (j, d)
        print time.time()
        terms = dict(sorted_terms[:d])
        print time.time()
        sys.stdout.flush()
        q_tweets_j = filter_terms(q_tweets, terms)
        db_tweets_j = filter_terms(db_tweets, terms)
        algorithm(q_tweets_j, db_tweets_j)

    print '== d-infrequent =='
    for j in range(0,15,2):
        d = 100 * 2**j
        print 'j=%d, d=%d' % (j, d)
        print time.time()
        terms = dict(sorted_terms[-d:])
        print time.time()
        sys.stdout.flush()
        q_tweets_j = filter_terms(q_tweets, terms)
        db_tweets_j = filter_terms(db_tweets, terms)
        algorithm(q_tweets_j, db_tweets_j)

    print '== d-random =='
    for j in range(0,15,2):
        d = 100 * 2**j
        print 'j=%d, d=%d' % (j, d)
        print time.time()
        terms = dict(random.sample(sorted_terms, min(len(sorted_terms), d)))
        print time.time()
        sys.stdout.flush()
        q_tweets_j = filter_terms(q_tweets, terms)
        db_tweets_j = filter_terms(db_tweets, terms)
        algorithm(q_tweets_j, db_tweets_j)

if __name__ == '__main__':
    #main(bf_algorithm)
    #main(speedy_algorithm)
    main(speedy_algorithm2)
