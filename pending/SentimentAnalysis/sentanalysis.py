from nltk.corpus import movie_reviews
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy


neg_ids = movie_reviews.fileids('neg')
pos_ids = movie_reviews.fileids('pos')

neg_rev = [ movie_reviews.words(fileids = [r]) for r in neg_ids]
pos_rev = [ movie_reviews.words(fileids = [r]) for r in pos_ids]


neg_cf = len(neg_rev) * 7 / 10
pos_cf = len(pos_rev) * 7 / 10

train = (neg_rev[:neg_cf], pos_rev[:pos_cf])
test = (neg_rev[neg_cf:], pos_rev[pos_cf:])

def extract(review):
    return {word : 1 for word in review }

train_feat = [(extract(review), 'neg') for review in train[0]]
train_feat += [(extract(review), 'neg') for review in train[1]]

test_feat = [(extract(review), 'neg') for review in test[0]]
test_feat += [(extract(review), 'neg') for review in test[1]]

classifier = NaiveBayesClassifier.train(train_feat)

ac = accuracy(classifer, test_feat)
print 'accuracy:' , ac

classifier.show_most_informative_features()
             
            
