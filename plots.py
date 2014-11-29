import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import pylab as pl
import time

from helpers import timing

# First plot with number of terms that appear in k tweets.
@timing
def plot1(terms):
    pl.figure(1)
    pl.plot(terms.keys(), terms.values(), 'rx')
    pl.yscale('log')
    pl.xscale('log')
    pl.xlabel('appears in k tweets')
    pl.savefig('fig1.png', bbox_inches='tight')

# Second plot with cummulative distribution, so number of tweets that appear
# in k or less tweets.
@timing
def plot2(terms):
    pl.figure(2)
    pl.clf()
    accumulator = 0
    for (n, appearances) in iter(sorted(terms.iteritems())):
        accumulator += appearances
        pl.plot(n, accumulator, 'rx')
    pl.yscale('log')
    pl.xscale('log')
    pl.xlabel('appears in k or less tweets')
    pl.savefig('fig2.png', bbox_inches='tight')

# Third plot which plots number of times a word appears in tweets but in
# descending order by appearances.
@timing
def plot3(tweet_terms):
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
