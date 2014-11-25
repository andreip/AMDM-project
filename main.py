import matplotlib
matplotlib.use('TkAgg')
import pylab as pl

filename = 'tweets_15m.txt'
tweets_max = 10000
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

terms_in_tweets_count = {}
for (word,n) in tweet_terms.iteritems():
    terms_in_tweets_count[n] = terms_in_tweets_count.get(n, 0) + 1

"""omas"""

pl.plot(terms_in_tweets_count.keys(), terms_in_tweets_count.values(), 'rx')
pl.yscale('log')
pl.xscale('log')
pl.xlabel('appears in k tweets')
pl.show()
