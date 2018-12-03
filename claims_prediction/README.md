<h1>FACT-CHECKABLE CLAIMS PREDICTION</h1>

This project, written in Python 2.7, allows you to train a classifier that can predict if a claim is fact-checkable or not.
At<a href="https://chequeado.com">Chequeado</a> we are using a solution that is more customized and complex, which we are hoping to make open source soon. Nevertheless, this current uploaded version is good enough to get accurate results if you train your model with a proper sized set of manually tagged sentences.

<h3>OVERVIEW</h3>

We extract features from a set of sentences using NLP (Natural Language Processing), and then train a Naive Bayes classifier on those features to detect if a new sentence is fact-checkable or not.

Before training the classifier we need to create a manually tagged corpus. We do this by labelling sentences as "fact-checkable" or "non-fact-checkable", in order to later train a Machine Learning model. 

Once we have those sentences tagged, we generate <a href="https://en.wikipedia.org/wiki/Part-of-speech_tagging">Part-Of-Speech</a> tags for each sentence, using <a href="https://spacy.io/models/">Spacy</a> and use those to extract the important features from each sentence. Finally, the features are used to train a Machine Learning model (Naive Bayes classifier), that will predict the outcome of new, non-tagged, claims.


<h3>QUICK START</h3>

<h4>Install required Python libraries</h4>

You can easilly install all the required libraries using pip:

```python
pip install -r requirements.txt
```

<h3>Training your own classifier</h3>

<h4>1. Manually label fact-checkable sentences</h4>

First of all you will need to tag a large amount of text with "\<chequeable\>\</chequeable\>" tags. 
To do this, find texts that are likely to have fact-checkable claims. For our example, we downloaded some presidential speechs from <a href="https://www.casarosada.gob.ar/informacion/discursos">here</a> and tagged the fact-checkable sentences. Here's an example:

        Algunos datos importantes vinculados a este informe de Agricultura y Ganadería y la ayuda que la FAO reconoce que hemos dado los productores, 
        además de los 54 mil millones, <chequeable>hoy la Argentina está produciendo en su sector agroalimentario alimentos para 400 millones de personas</chequeable>.
        <chequeable> O sea, nosotros representamos el 10 por ciento como población de lo que estamos produciendo en materia de agroalimentos</chequeable>. 
        Por otro lado, quiero leerles algunas cifras en materia de turismo. <chequeable>15% interanual de aumento en llegada de turistas no residentes al país</chequeable>, 
        <chequeable>aproximadamente 6 millones de extranjeros eligieron la República Argentina para sus vacaciones</chequeable>, 
        convirtiéndonos en <chequeable>uno de los cinco países del mundo que más crecieron en llegada de turismo de extranjeros entre enero y agosto del 2014</chequeable> según la Organización Mundial del Turismo.

As you can see, we only tag the fact-checkable claims. The ones without tag are read as not fact-checkable.
Once you have tagged those files, dump them in ".txt" format in the "data/tagged_corpus" folder. 


<b>If you want to use our tagged files, skip this step, as they are already loaded in the "data/tagged_corpus" folder.</b>

<h4>2. Save Part-Of-Speech tags</h4>

<i>The use of the word "tag" may be confusing as this proccess requires us to do two taggins. First, the "fact-checkable" or not tagging and then POS tag. To refer to the lather we will us always the term "POS tag" or "POS tagging".</i>

For this step we created a module called "tag_corpus.py", which loads all the ".txt" files in the "data/tagged_corpus" folder, generates POS tags, and dumps them in the "data/pos_sentences" folder.
This POS tags are essentially linguistic features. An example can be found in <a href="https://spacy.io/usage/linguistic-features#section-pos-tagging">this section</a>.

<b>To do this, simply open your console and type: "python tag_corpus.py". </b>

```python
python tag_corpus.py
```

This will take all the sentences from the ".txt" files and generate individual POS tags for each sentence. After this, those tags will be dumped in <a href="https://docs.python.org/2/library/pickle.html">pickles</a>.


<h4>3. Train the classifier</h4>

Now, we have all the POS tags for each sentence, and we also know if that sentence is fact-checkable or not.
The final step is to train the classifier. This means two things: first, that we need to extract from the POS tags, the things that we believe will be important for the classifier (features), and second, we need to feed the model with those features to train and test it.

Now you can run the trainer script:

```python
python trainer.py
```

This will train a new classifier and save the model in "data/classifiers", also as a pickle. You can change the name of your classifier by changing the variable "MODEL_NAME".

<h3>USING IT IN OTHER LANGUAGES</h3> 

To change the language you have to simply choose a different model in the "spacy_utils/pos_tag.py" file from the ones available in <a href="https://spacy.io/usage/models">Spacy models</a>.
By the way, remember that the language of the initial tagged corpus has to correspond the language you use for the model, but the <chequeable></chequeable> tags are still the same.

To use your classifier you will first have to load it:

```python
f = open('data/classifiers/' + MODEL_NAME, 'rb')
classifier = pickle.load(f)
f.close()
```

After that, import the spacy_utils functions "pos_tag" and "automatic_feature_extractor" to classify a new sentence:
```python
# imports from spacy_utils
import sys
sys.path.append('../spacy_utils')
from pos_tagger import pos_tag
from feature_extractors import automatic_feature_extractor
        
# Generate pos tags for the sentence
pos_tags = pos_tag(sentence)
# Get features
features = automatic_feature_extractor(pos_tags, True)
# Take a guess
guess = classifier.classify(features)
```

This code is commented and ready to run in "test.py", read it to get a bit more understanding.
