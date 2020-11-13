# -*- coding: utf-8 -*-
from nltk import ngrams

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def automatic_feature_extractor(spacy_tag, pos_ngrams=False):
    features = {}

    for tagged_word in spacy_tag:
        #pos, lemma, text, tag, dep ,is_punct, like_num, tense
        if tagged_word['is_punct'] and tagged_word['lemma'] not in "%¿?":
            continue

        features[tagged_word['pos']] = True
        features[tagged_word['lemma']] = True
        features[tagged_word['dep']] = True
        features[tagged_word['tense']] = True

        if is_int(tagged_word['lemma']):
            number_of_digits = len(str(tagged_word['lemma']))
            features['%s_digits' %number_of_digits] = True

    if pos_ngrams:        
        ctags_chain = [e['pos'] for e in spacy_tag]
        ngs = ngrams(ctags_chain, 3)
        for ng in ngs:
            features[ng] = True
   
    return features