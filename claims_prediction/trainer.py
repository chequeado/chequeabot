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

# SETTINGS
from constants import POS_TAGGED_FOLDER, CLASSIFIERS_FOLDER, TRAIN_PERCENTAGE, TEST_PERCENTAGE, SPACY_FOLDER

sys.path.append(SPACY_FOLDER)  
from feature_extractors import automatic_feature_extractor
from pos_tagger import pos_tag

def get_tagged_sentences(folder):
    # Load all the tagged sentences included in the .pickle files 
    parsed_sentences = []
    for filename in glob.glob(folder + '*.pickle'):
        with open(filename, 'rb') as tagged_file:
            parsed_sentences = parsed_sentences + pickle.load(tagged_file)
    return parsed_sentences 
    
def dump_classifier(folder, classifier,description=""):
    # Once created, it will dump the clasifier into a pickle.
    # Change the name to whatever you see fit
    name = 'classifier-%s.pickle' % date.today() 
    f = open(folder + name, 'wb')
    pickle.dump(classifier, f)
    f.close()    
    #dumps the descriptino in a txt file
    f_desc = open(folder + name.replace("pickle","txt"),"w+")
    f_desc.write(description)
    f_desc.close()
    
def show_metrics(classifier, test_set):    
    description = ""
    # Given a classifier and a set to test it, it will print metrics for the classifier
    description = description + "\n" + "Accuracy: " + str(nltk.classify.accuracy(classifier, test_set))

    # Creates two sets: one with references (correct results) and other with tests (classifier predictions)
    # This sets are divided in fact-checkable and non-fact-checkable sets that contain a unique id (integer)
    # for each sentence
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)
    for i, (feats, label) in enumerate(test_set):
        refsets[label].add(i) # 1, neg
        observed = classifier.classify(feats) #neg
        testsets[observed].add(i) #1, neg

    model_precision =  int(precision(refsets['fact-checkable'], testsets['fact-checkable'])*100)    
    model_recall =  int(recall(refsets['fact-checkable'], testsets['fact-checkable'])*100)
    model_f_measure =  int(f_measure(refsets['fact-checkable'], testsets['fact-checkable'],0.3)*100)
    
    description += "\n" + "PRECISION: Of the sentences predicted fact-checkable, " + str(model_precision) + "% were actually fact-checkable"
    description += "\n" + "RECALL: Of the sentences that were fact-checkable, " + str(model_recall) + "% were predicted correctly"
    description += "\n" + "F-MEASURE (balance between precission and recall): " + str(model_f_measure) + "%"

    # Same for non fact-checkables
    #print('non-fact-checkable precision:', precision(refsets['non-fact-checkable'], testsets['non-fact-checkable']))
    #print('non-fact-checkable recall:', recall(refsets['non-fact-checkable'], testsets['non-fact-checkable']))
    #print('non-fact-checkable F-measure:', f_measure(refsets['non-fact-checkable'], testsets['non-fact-checkable']))

    print(description)

    # informative
    classifier.show_most_informative_features(25)

    return description

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

if __name__ == "__main__":
    # Load the dataset from pickles and extract features
    tagged_sentences = get_tagged_sentences(POS_TAGGED_FOLDER)
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
    description = show_metrics(classifier,test_set)

    # finally train the model with the full dataset
    classifier = nltk.NaiveBayesClassifier.train(dataset)
    dump_classifier(CLASSIFIERS_FOLDER, classifier,description)
