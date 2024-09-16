from transformers import AutoTokenizer
from collections import Counter

def count_unique_tokens(file_path):
    
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased", clean_up_tokenization_spaces=False)

 
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

   
    tokens = tokenizer.tokenize(text)

   
    token_counts = Counter(tokens)

    top_30_tokens = token_counts.most_common(30)

    return token_counts, top_30_tokens


file_path = '/Users/aimanahamed/Desktop/Software Now/data.txt'  
token_counts, top_30_tokens = count_unique_tokens(file_path)

print(f"Total unique tokens: {len(token_counts)}")
print("Top 30 tokens:")
for token, count in top_30_tokens:
    print(f"{token}: {count}")