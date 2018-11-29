 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import collections
import pickle 
import glob
import re
import nltk
from nltk.metrics.scores import precision, recall, f_measure
from datetime import date
from random import shuffle
import sys

sys.path.append('../spacy_utils')  
from feature_extractors import automatic_feature_extractor
from pos_tagger import pos_tag

def get_tagged_sentences(folder):
    # Load all the tagged sentences included in the .pickle files 
    parsed_sentences = []
    for filename in glob.glob(folder + '*.pickle'):
        with open(filename, 'rb') as tagged_file:
            parsed_sentences = parsed_sentences + pickle.load(tagged_file)
    return parsed_sentences 
    
def dump_classifier(folder, classifier):
    # Once created, it will dump the clasifier into a pickle.
    # Change the name to whatever you see fit
    name = 'classifier-%s.pickle' % date.today() 
    f = open(folder + name, 'wb')
    pickle.dump(classifier, f)
    f.close()    
    
def show_metrics(classifier, test_set):    
    # Given a classifier and a set to test it, it will print metrics for the classifier

    print("Accuracy: " + str(nltk.classify.accuracy(classifier, test_set)))

    # Creates two sets: one with references (correct results) and other with tests (classifier predictions)
    # This sets are divided in fact-checkable and non-fact-checkable sets that contain a unique id (integer)
    # for each sentence
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)
    for i, (feats, label) in enumerate(test_set):
        refsets[label].add(i) # 1, neg
        observed = classifier.classify(feats) #neg
        testsets[observed].add(i) #1, neg

    # Of the sentences predicted fact-checkable, how many were acctually fact-checkable
    print('fact-checkable precision:', precision(refsets['fact-checkable'], testsets['fact-checkable']))
    # Of the sentences that were fact-checkable, how many were predicted correctly
    print('fact-checkable recall:', recall(refsets['fact-checkable'], testsets['fact-checkable']))
    # Balance between precision and recall, giving more importance to recall because we dont want to let any 
    # fact-checkable sentence escape
    print('fact-checkable F-measure:', f_measure(refsets['fact-checkable'], testsets['fact-checkable'],0.3))

    # Same for non fact-checkables
    #print('non-fact-checkable precision:', precision(refsets['non-fact-checkable'], testsets['non-fact-checkable']))
    #print('non-fact-checkable recall:', recall(refsets['non-fact-checkable'], testsets['non-fact-checkable']))
    #print('non-fact-checkable F-measure:', f_measure(refsets['non-fact-checkable'], testsets['non-fact-checkable']))

    # informative
    classifier.show_most_informative_features(25)

def split_dataset(dataset):
    # Given a dataset, it will split it according to test and train percentage
    # Before that, it shuffles the dataset so each time you get different train and test sets

    corpus_size = len(dataset)
    train_limit = int(corpus_size*TRAIN_PERCENTAGE)
    test_limit = int(corpus_size*TEST_PERCENTAGE)

    shuffle(dataset)

    train_values = dataset[:train_limit]
    test_values = dataset[train_limit:train_limit+test_limit]

    return train_values,test_values

# CONSTANTS
TRAIN_PERCENTAGE = 0.7
TEST_PERCENTAGE = 0.3
TAGGED_SENTENCES_FOLDER ="data/pos_sentences/"
CLASSIFIERS_FOLDER = "data/classifiers/" 

if __name__ == "__main__":
    # Load the dataset from pickles and extract features
    tagged_sentences = get_tagged_sentences(TAGGED_SENTENCES_FOLDER)
    dataset = [(automatic_feature_extractor(sent['pos_tag'], pos_ngrams=True), sent['classification']) for sent in tagged_sentences]
    
    # Train the classifier on "n" folds and establish an average accuracy
    # This process is to get ony that accuracy number
    accuracys = []
    folds = 10
    for i in range(folds):
        train_set, test_set = split_dataset(dataset)
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        accuracys.append(nltk.classify.accuracy(classifier, test_set))
    accuracy = sum(accuracys)/len(accuracys)
    print("Accuracy after " + str(folds) + " folds: " + str(accuracy))

    # Train again a model for specific metrics
    train_set, test_set = split_dataset(dataset)
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    show_metrics(classifier,test_set)

    # finally train the model with the full dataset
    classifier = nltk.NaiveBayesClassifier.train(dataset)
    dump_classifier(CLASSIFIERS_FOLDER, classifier)
