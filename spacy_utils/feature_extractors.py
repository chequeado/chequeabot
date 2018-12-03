 # -*- coding: utf-8 -*-
from nltk import ngrams

def automatic_feature_extractor(spacy_tag, pos_ngrams=False):
    features = {}

    for tagged_word in spacy_tag:
        #pos, lemma, text, tag, dep ,is_punct, like_num, tense
        if tagged_word['is_punct'] and tagged_word['lemma'].encode('utf8') not in "%¿?":
            continue

        features[tagged_word['pos']] = True
        features[tagged_word['lemma']] = True
        features[tagged_word['dep']] = True

    if pos_ngrams:        
        ctags_chain = [e['pos'] for e in spacy_tag]
        ngs = ngrams(ctags_chain, 4)
        for ng in ngs:
            features[ng] = True
   
    return features

"""
def automatic_feature_extractor(spacy_tag, pos_ngrams=False):
    ''' features has to be a list of dictionaries, each
    dict being the tagged features of a sentence'''
    features = {}

    for tagged_word in spacy_tag:
        #pos, lemma, text, tag, dep ,is_punct, like_num, tense
        tagged_word['final'] = tagged_word['pos']

        if(tagged_word['pos'] in "PUNCT PROPN SYM ADP NOUN PRON"):
            features[tagged_word['lemma']] = True
            tagged_word['final'] = tagged_word['lemma']
        
        if(tagged_word['pos'] in "NUM"):
            number_of_digits = len(str(tagged_word['lemma'].encode('utf8')))
            features['%s_digits' %number_of_digits] = True
            tagged_word['final'] = '%s_digits' %number_of_digits
        
        if(tagged_word['lemma'].encode('utf8') in IMPORTANT_WORDS):
            features[tagged_word['lemma']] = True
            tagged_word['final'] = tagged_word['lemma']

        if(tagged_word["is_punct"]):
            features[tagged_word['text']] = True
            tagged_word['final'] = tagged_word['text'].encode('utf8')

        features['tense'] = tagged_word['tense']


    ctags_chain_lemma = [e['final'].lower() for e in spacy_tag ]

    #agregando pos trigrams
    if pos_ngrams:
        ngs = ngrams(ctags_chain_lemma, 3)
        for ng in ngs:
            features[ng] = True

    return features
    """