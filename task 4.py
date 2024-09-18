import spacy


nlp_sci = spacy.load("en_core_sci_sm")
nlp_bc5cdr = spacy.load("en_ner_bc5cdr_md")


with open('combined_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

doc_sci = nlp_sci(text)
doc_bc5cdr = nlp_bc5cdr(text)


diseases_sci = [ent.text for ent in doc_sci.ents if ent.label_ == 'DISEASE']
drugs_bc5cdr = [ent.text for ent in doc_bc5cdr.ents if ent.label_ == 'CHEMICAL']

from transformers import pipeline


ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")


ner_results = ner_pipeline(text)


diseases_biobert = [res['word'] for res in ner_results if res['entity_group'] == 'DISEASE']
drugs_biobert = [res['word'] for res in ner_results if res['entity_group'] == 'DRUG']

from collections import Counter


print("SciSpacy Diseases:", len(diseases_sci))
print("BioBERT Diseases:", len(diseases_biobert))


common_diseases_sci = Counter(diseases_sci).most_common(10)
common_diseases_biobert = Counter(diseases_biobert).most_common(10)

print("Most common diseases in SciSpacy:", common_diseases_sci)
print("Most common diseases in BioBERT:", common_diseases_biobert)