# SETTINGS

# Languages available
SPANISH = "es"

# Language to use:
# (Only supports spanish right now)
LANGUAGE = SPANISH

# FOLDERS
TAGGED_FOLDER = "data/tagged_corpus/" + LANGUAGE + "/"
POS_TAGGED_FOLDER = "data/pos_sentences/" + LANGUAGE + "/"
CLASSIFIERS_FOLDER = "data/classifiers/" + LANGUAGE + "/"
SPACY_FOLDER = "../spacy_utils/" + LANGUAGE + "/"

# Training
TRAIN_PERCENTAGE = 0.7
TEST_PERCENTAGE = 0.3
