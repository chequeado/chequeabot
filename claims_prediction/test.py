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

MODEL_NAME = "classifier-2018-12-06.pickle"

SENTENCES = [
    "En el 2016 equiparamos el sueldo con la inflación; en el 2017, también",
    "En un ránking de las 50 ciudades más violentas, Brasil fue incluida en 17 ciudades. Nosotros no tenemos ni una sola ciudad incluida",
    "El 30% de las cárceles federales están llenas de extranjeros",
    "Argentina es el quinto país en formación de activos externos",
    "Este presupuesto tiene más del 60% en cuestiones sociales",
    "El plan Progresar (…) prácticamente han desaparecido",
    "La inflación de este año será la más alta de los últimos 27 años",
    "Al 25 de septiembre sólo se ejecutó el 24% del presupuesto de Salud Sexual y Procreación Responsable",
    "En nuestro país muere una mujer cada 30 horas por femicidios",
    "Hemos reducido el gasto en términos reales un 20% en estos cuatro años"
]

if __name__=='__main__':
    classifier1 = load_classifier(MODEL_NAME)

    for sentence in SENTENCES:
        print(sentence)
        print(classify(classifier1,sentence))
        print("****")
