# -*- coding: utf-8 -*-
import sys
import spacy
nlp = spacy.load('es_core_news_md')

sys.path.append("../regex_utils/es")
import tagger_regex

def extract_value_from_tag(tag,value):
    if value in tag:
        trunk = tag[tag.find(value) :]
        trunk = trunk[trunk.find('=')+1:trunk.find('|')]
        return trunk
    else:
        return "undefined"

def pos_tag(frase):
    frase = frase.decode('utf8')
    #doc = nlp(frase,disable=['parser','nec'])
    doc = nlp(frase)
    tags = []

    for token in doc:
        word = {}
        word['pos'] = token.pos_
        word['lemma'] = token.lemma_.lower()
        word['text'] = token.text
        word['tag'] = token.tag_
        word['dep'] = token.dep_
        word['is_punct'] = token.is_punct
        word['like_num'] = token.like_num
        word['tense'] = extract_value_from_tag(token.tag_,"Tense")
        
        temporal =  tagger_regex.tag(token.lemma_.lower(),tagger_regex.temporal_regex)
        if temporal:
            word['temporal'] = temporal
        
        measure = tagger_regex.tag(token.lemma_.lower(),tagger_regex.measure_regex)
        if measure:
            word['measure'] = measure

        tags.append(word)

    return tags