import nltk

def ensure_nltk_data():
    resources = ["stopwords", "wordnet", "omw-1.4"]
    for r in resources:
        try:
            nltk.data.find(f"corpora/{r}")
        except LookupError:
            nltk.download(r, quiet=True) 

ensure_nltk_data()