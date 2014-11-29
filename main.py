import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import pylab as pl
import time

filename = 'tweets_15m.txt'
#filename = 'tweets_small.txt'
tweets_max = 1000**2 * 15
read_chunk = 1000**2

print time.time()
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

print time.time()
print 'Done. Counting terms in k tweets'
max_index = 0
terms_in_tweets_count = {}
for (word,n) in tweet_terms.iteritems():
    terms_in_tweets_count[n] = terms_in_tweets_count.get(n, 0) + 1
    max_index = max(max_index, n)

print time.time()
print 'Done.'

"""omas"""
def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap


# First plot with number of terms that appear in k tweets.
@timing
def plot1():
    pl.figure(1)
    pl.plot(terms_in_tweets_count.keys(), terms_in_tweets_count.values(), 'rx')
    pl.yscale('log')
    pl.xscale('log')
    pl.xlabel('appears in k tweets')
    pl.savefig('fig1.png', bbox_inches='tight')

# Second plot with cummulative distribution, so number of tweets that appear
# in k or less tweets.
@timing
def plot2():
    pl.figure(2)
    pl.clf()
    accumulator = 0
    for (n, appearances) in iter(sorted(terms_in_tweets_count.iteritems())):
        accumulator += appearances
        pl.plot(n, accumulator, 'rx')
    pl.yscale('log')
    pl.xscale('log')
    pl.xlabel('appears in k or less tweets')
    pl.savefig('fig2.png', bbox_inches='tight')

# Third plot which plots number of times a word appears in tweets but in
# descending order by appearances.
@timing
def plot3():
    pl.figure(3)
    pl.clf()
    print time.time()
    iter_sorted = iter(sorted(tweet_terms.values(), reverse=True))
    print time.time()
    map(lambda x,y: pl.plot(x,y,'rx'), xrange(len(tweet_terms)), iter_sorted)
    pl.yscale('log')
    pl.xscale('log')
    pl.ylabel('Appearances of word j in tweets')
    pl.xlabel('j')
    pl.savefig('fig3.png', bbox_inches='tight')

plot1()
plot2()
plot3()
