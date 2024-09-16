import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def process_text(text):
    sentences = sent_tokenize(text)
    
    processed_sentences = []
    for sentence in sentences:
        tokens = word_tokenize(sentence.lower())
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
        stemmer = PorterStemmer()
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        processed_sentences.append(stemmed_tokens)
    
    return processed_sentences

def extract_medical_terms(text):
    words = word_tokenize(text)
    
    medical_terms = []
    medical_prefixes = ['hyper', 'hypo', 'anti', 'endo', 'cardio', 'neuro', 'gastro']
    medical_suffixes = ['itis', 'osis', 'emia', 'pathy']
    specific_terms = ['diagnosed', 'prescribed', 'symptoms', 'allergies', 'patient', 'drug', 'medicine']
    
    for word in words:
        if any(word.lower().startswith(prefix) for prefix in medical_prefixes) or \
           any(word.lower().endswith(suffix) for suffix in medical_suffixes) or \
           word.lower() in specific_terms:
            medical_terms.append(word)
    
    return medical_terms

sample_text = "The patient was diagnosed with hypertension and prescribed lisinopril. They also showed symptoms of diabetes mellitus and were referred to an endocrinologist. The patient reported allergies to penicillin and sulfa drugs."

processed_text = process_text(sample_text)
print("Processed text:")
for sentence in processed_text:
    print(sentence)

print("\nExtracted medical terms:")
medical_terms = extract_medical_terms(sample_text)
print(medical_terms)