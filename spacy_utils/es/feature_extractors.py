 # -*- coding: utf-8 -*-
from nltk import ngrams

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def is_symbol(tagged_word):
    return tagged_word['pos'] in "PUNCT SYM"

def automatic_feature_extractor(spacy_tag, pos_ngrams=False):
    features = {}
    symbols = ["$","%","¿","?","u$s","US$","U$S"]

    for tagged_word in spacy_tag:
        #pos, lemma, text, tag, dep ,is_punct, like_num, tense
        lemma = tagged_word['lemma'].encode('utf8')
        
        if is_symbol(tagged_word):
            # For symbols, we only want to keep $,% and ¿?. The rest doesnt mater to us
            if lemma in symbols:
                features[tagged_word['lemma']] = True
        elif is_int(tagged_word['lemma']):
            # For numbers we are gonna keep only the number of digits
            number_of_digits = len(str(tagged_word['lemma'].encode('utf8')))
            features['%s_digits' %number_of_digits] = True
        elif 'temporal' in tagged_word:
            # Group words that work as temporal references
            for key in tagged_word['temporal'].keys():
                features[key] = True
        elif 'measure' in tagged_word:
            # Group words that imply measurements
            for key in tagged_word['measure'].keys():
                features[key] = True
        else:
            features[tagged_word['lemma']] = True

        features[tagged_word['pos']] = True
        features[tagged_word['tense']] = True

    if pos_ngrams:        
        ctags_chain = [e['pos'] for e in spacy_tag]
        ngs = ngrams(ctags_chain, 3)
        for ng in ngs:
            features[ng] = True
   
    return features
