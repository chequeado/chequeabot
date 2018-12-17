#!/usr/bin/python
# -*- coding: utf-8 -*-

# CHEQUEADO
#
# This module will extract all .txt files in data/tagged_corpus, 
# split the sentences in them between fact-checkable (fc) and not fact-checkable, 
# and finally generate the POS tags for each sentence.
# The results will be saved in the pos_sentences folder for later use.

import pickle 
import re
import nltk
import glob
import sys

# SETTINGS
from constants import TAGGED_FOLDER,POS_TAGGED_FOLDER, SPACY_FOLDER

sys.path.append(SPACY_FOLDER)
from pos_tagger import pos_tag
import feature_extractors

# TO USE A DIFFERENT LANGUAGE:
# 1- Create a folder named as the language code (example: "en") in the tagged_corpus and pos_sentences folder.
# 2- Drop your tagged text files in "tagged_corpus/your_language".
# 3- Change the language code in settings.py 
# 3- Run "python tag_corpus.py"
# 4- The pos_tagged resulting files will appear in "pos_sentences/your_language"

# To split between fact-checkable and not fc
FACT_CHECKABLE_REGEX = re.compile('<chequeable>([^>]*)</chequeable>') #non greedy regex

# UTILS FUNCTIONS

def tokenize(text):
    return nltk.sent_tokenize(text.decode('utf8'))
            
def clean_sentence(sentence):
    return sentence.encode('utf8').replace(',','').replace('.','').replace(';','').replace('[','').replace(']','').replace("(Aplausos.)","").replace("(aplausos)","")        

def get_output_path(name):
    return name.replace(".txt",".pickle").replace(TAGGED_FOLDER, POS_TAGGED_FOLDER)

def extract_fc_tags(sentences, regex):
    # From a list of sentence, find all the fact-checakble tags in it, else, tag as non fact checkable
    tagged_sentences = []
    for sentence in sentences: 
        sentence = clean_sentence(sentence)
        fact_checkable_claims = regex.findall(sentence)
        if fact_checkable_claims:
            for claim in fact_checkable_claims:
                tagged_sentences.append({'classification': 'fact-checkable', 'sentence': claim})
        else:
            tagged_sentences.append({'classification': 'non-fact-checkable', 'sentence': sentence})
    return tagged_sentences

def dump_pickle(name, content):
    pickle_file = open(name, 'wb')
    pickle.dump(content, pickle_file)
    pickle_file.close()

# MAIN FUNCTION

def dataset_tagging():   
    # This function takes all the .txt files, 
    # extracts fact-checkable and not-fact-checkable tags 
    # and finally adds pos tags and dumps it in a pickle
    # NOTE: tagging here refers to POS tags, not to the fact-checkable tags (<chequeable>)

    CORPUS_FILES = glob.glob(TAGGED_FOLDER + "*.txt")
    TAGGED_FILES = glob.glob(POS_TAGGED_FOLDER + "*.pickle")    
    
    UNTAGGED_FILES = [f for f in CORPUS_FILES if get_output_path(f) not in TAGGED_FILES]
    for filename in UNTAGGED_FILES:
        with open(filename, 'rb') as corpus_file:
            print("Tagging elements in file " + filename)

            sentences = tokenize(corpus_file.read())
            tagged_sentences = extract_fc_tags(sentences, FACT_CHECKABLE_REGEX)

            for sentence in tagged_sentences:
                # Tag
                sentence['pos_tag'] = pos_tag(sentence['sentence'])
                # Show progress
                progress = (tagged_sentences.index(sentence)/float(len(tagged_sentences)))*100
                print("Progress: %.2f%%" % progress) 

            print("Dumping tagged sentences")
            dump_pickle(get_output_path(filename), tagged_sentences)    

    print("All corpus have been tagged, find them in " + TAGGED_FOLDER)

if __name__ == '__main__':
    dataset_tagging()
