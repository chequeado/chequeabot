# -*- coding: utf-8 -*-
import spacy
nlp = spacy.load('es_core_news_md')

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
        
        if "Tense" in token.tag_:
            trunk = token.tag_[token.tag_.find("Tense") :]
            trunk = trunk[trunk.find('=')+1:trunk.find('|')]
            word['tense'] = trunk
        else:
            word['tense'] = "undefined"

        tags.append(word)

    return tags