# -*- coding: utf-8 -*-
import pickle
import sys

# SETTINGS
from constants import CLASSIFIERS_FOLDER, SPACY_FOLDER

sys.path.append(SPACY_FOLDER)
from pos_tagger import pos_tag
import feature_extractors

def load_classifier(name):
    # Loads the classifier pickle
    f = open(CLASSIFIERS_FOLDER + name, 'rb')
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

# CONSTANTS

MODEL_NAME = "classifier-2018-12-06.pickle"

SENTENCES = [
    "El 99% de la gente que muere por un arma de fuego en la Argentina muere en manos de un delincuente que la asesina",
    "En el 2016 equiparamos el sueldo con la inflación; en el 2017, también",
    "En un ránking de las 50 ciudades más violentas, Brasil fue incluida en 17 ciudades. Nosotros no tenemos ni una sola ciudad incluida",
    "El 30% de las cárceles federales están llenas de extranjeros",
    "Argentina es el quinto país en formación de activos externos",
    "Este presupuesto tiene más del 60% en cuestiones sociales",
    "El plan Progresar (...) prácticamente han desaparecido",
    "La inflación de este año será la más alta de los últimos 27 años",
    "Al 25 de septiembre sólo se ejecutó el 24% del presupuesto de Salud Sexual y Procreación Responsable",
    "El aumento de Ciencia y Tecnología [será] de 28%",
    "En 2014 había 876 personas en situación de calle; en 2018, 5.872 y 25.872 en riesgo de situación de calle",
    "En el presupuesto se prevé un recorte de 20% para el Incucai, siempre en términos reales",
    "Se prevé un recorte de 70% en infraestructura escolar y un 70% para jardines de infantes",
    "En nuestro país muere una mujer cada 30 horas por femicidios",
    "Hemos reducido el gasto en términos reales un 20% en estos cuatro años",
    "En términos reales, la reducción del gasto será del 6% en Servicios Sociales",
    "Ecuador tiene 97% de la población urbana con cloacas, nosotros el 50%",
    "La deuda pública a fin de año representará el 87% del PBI",
    "La pérdida del poder [adquisitivo] del salario este año ha sido muy alta",
    "Hay 800 mil pensiones por invalidez de más. Son más que los muertos de Estados Unidos, Reino Unido, Francia, Polonia, Grecia y los Países Bajos juntos en la Segunda Guerra Mundial",
    "¿Sabés cuántas villas hay en el cordón de la Provincia de Buenos Aires? Cerca de cuatro mil",
    "Hubo más deportaciones este último año que en los últimos diez años",
    "El año que viene terminaría con seis puntos menos de PBI per cápita que en 2015",
    "Las prestaciones sociales aumentan 37%",
    "Salta tuvo el doble de éxito que la Argentina en cuanto a la reducción de la pobreza de acuerdo al censo nacional",
    "Un millón de turistas viajó por el país este fin de semana largo. Si se compara con el año pasado, la cantidad creció un 7,4%",
    "No es una compensación por la devaluación",
    "La Argentina ya ha recibido 130 mil venezolanos",
    "Las exportaciones están creciendo a una velocidad del 18 o 20%",
    "La Argentina, lo tenemos que reconocer, es de los países más vulnerables del mundo",
    "De las 22 provincias que suscribieron el Consenso Fiscal, hoy 20 tienen superávit. La relación cambió",
    "Cambiemos contrajo una deuda superior, en dos años y medio, a la de la dictadura militar durante todo su gobierno",
    "Un jubilado necesita $19.400 para poder vivir y este Gobierno les da $8.600",
    "Nuestro compromiso con la universidad pública (...) se refleja en el presupuesto que hemos duplicado en estos tres años de gobierno",
    "En un mes y medio ya quemaron la mitad en fuga de capitales: US$ 7 mil millones",
    "Tenemos más detenidos por narcotráfico en los últimos dos años que en toda la gestión del gobierno de Scioli",
    "Si uno mira el presupuesto de este año, ha sido solamente ejecutado en un 12%",
    "En Uruguay las muertes maternas por aborto prácticamente cayeron a cero",
    "De cada 10 embarazos adolescentes, siete no son deseados",
    "Entre el 2010 y el 2014 se produjeron en todo el mundo alrededor de 25 millones de abortos peligrosos, casi la mitad de los abortos totales",
    "Hay tantas miles de personas que quieren adoptar y miles de niños que quieren un hogar",
    "La provincia del Chaco tiene diez puntos más de tasa de embarazo adolescente que el promedio del país",
    "Esta es la realidad que tenemos en Corrientes una tasa de mortalidad materna que cuadruplica la nacional",
    "Se estiman entre 44 mil y 53 mil egresos hospitalarios anuales por abortos con complicaciones",
    "Las estadísticas muestran que hay otros factores que la reducen Chile tiene una mortalidad menor a la argentina con una ley mucho más restrictiva"
]

# TEST
import csv
import re 

FACT_CHECKABLE_REGEX = re.compile('".*?"') #non greedy regex

if __name__=='__main__':
    classifier = load_classifier(MODEL_NAME)

    classifications = []
    for sentence in SENTENCES:
        print(sentence)
        classification = classify(classifier,sentence)
        classifications.append(classification[0])
        print(classification)
        print("****")
    """
    sentences = []
    with open('data/fc_2018_dump.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            quotes = FACT_CHECKABLE_REGEX.findall(row['sentence'])
            if quotes:
                for quote in quotes:
                    freeling =  row['fc_predict']
                    spacy = classify(classifier,quote)[0]
                    sentences.append({'sentence':row['sentence'],'quote':quote, 'freeling':freeling,'spacy':spacy})
                    if freeling != spacy:
                        print(row['sentence'])
                        print(quote)
                        print("F: "+freeling)
                        print("S: "+spacy)
                        print("***")
    """
    import pdb; pdb.set_trace()