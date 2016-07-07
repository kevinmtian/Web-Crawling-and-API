'''
For this part, you will compute the sentiment of each tweet based on the sentiment scores of the terms in the tweet. The sentiment of a tweet is equivalent to the sum of the sentiment scores for each term in the tweet.
'''

import sys
import json


def hw():
    print 'Hello, world!'


def lines(fp):
    print str(len(fp.readlines()))


def create_sent_dictionary(afinnfile):
    scores = {}
    for line in afinnfile:
        term, score = line.split("\t")
        scores[term] = int(score)
    return scores


def calculate_single_tweet_sent(tweet, sentiments):
    total = 0
    tweet = tweet.split(' ')
    for word in tweet:
        if word in sentiments:
            total += sentiments[word]
    return total


def stream_sent(tweets, sentiments):
    score = 0
    for line in tweets:
        tweet = json.loads(line)
        if 'text' in tweet:
            text = tweet['text']
            score = calculate_single_tweet_sent(text, sentiments)
        print score


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    sentiments = create_sent_dictionary(sent_file)
    stream_sent(tweet_file, sentiments)


if __name__ == '__main__':
    main()