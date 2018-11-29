# -*- coding: utf-8 -*-
import pickle
import sys
sys.path.append('../spacy_utils')
  
from pos_tagger import pos_tag
import feature_extractors

def load_classifier(name):
    # Loads the classifier pickle
    f = open('data/classifiers/%s' % name, 'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier

def classify(classifier,sentence):
    # Gets features from the sentence and uses the classifier to generate a prediction,
    # with a confidence score
    pos_tags = pos_tag(sentence)
    features = feature_extractors.automatic_feature_extractor(pos_tags, True)
    guess = classifier.classify(features)
    dist = classifier.prob_classify(features)
    confidence_prob = dist.prob(guess)
    return guess, confidence_prob

MODEL_NAME = "fc-classifier.pickle"

if __name__=='__main__':
    classifier = load_classifier(MODEL_NAME)
    prediction,confidence = classify(classifier,"Subió la inflación un 50%")
    print("Prediction: " + str(prediction) + " | Confidence: " + str(confidence))
