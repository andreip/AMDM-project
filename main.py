import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import pylab as pl

filename = 'tweets_15m.txt'
tweets_max = 1000
read_chunk = 100

tweet_terms = {}
with open(filename) as f:
    read_tweets = 0
    while read_tweets < tweets_max:
        tweets = f.readlines(read_chunk)
        # Tweets are finished.
        if not tweets:
            break
        read_tweets += read_chunk
        for raw_tweet in tweets:
            tweet = raw_tweet.strip('\n').split('\t')
            for word in set(tweet):
                tweet_terms[word] = tweet_terms.get(word, 0) + 1

max_index = 0
terms_in_tweets_count = {}
for (word,n) in tweet_terms.iteritems():
    terms_in_tweets_count[n] = terms_in_tweets_count.get(n, 0) + 1
    max_index = max(max_index, n)

"""omas"""

# First plot with number of terms that appear in k tweets.
def plot1():
    pl.figure(1)
    pl.plot(terms_in_tweets_count.keys(), terms_in_tweets_count.values(), 'rx')
    pl.yscale('log')
    pl.xscale('log')
    pl.xlabel('appears in k tweets')
    pl.show()

# Second plot with cummulative distribution, so number of tweets that appear
# in k or less tweets.
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
    pl.show()

# Third plot which plots number of times a word appears in tweets but in
# descending order by appearances.
def plot3():
    pl.figure(3)
    pl.clf()
    iter_sorted = iter(sorted(tweet_terms.iteritems(), key=lambda x: x[1],
    reverse=True))
    for i, (word, appearances) in enumerate(iter_sorted):
        pl.plot(i+1, appearances, 'rx')
    pl.yscale('log')
    pl.xscale('log')
    pl.ylabel('Appearances of word j in tweets')
    pl.xlabel('j')
    pl.show()

plot1()
plot2()
plot3()
