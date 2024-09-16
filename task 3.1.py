import re
from collections import Counter
import csv


input_text_file = '/Users/aimanahamed/Desktop/Software Now/output_text_file.txt'
output_csv_file = '/Users/aimanahamed/Desktop/Software Now/top_30_common_words.csv'


with open(input_text_file, 'r', encoding='utf-8') as file:
    text = file.read()

words = re.findall(r'\b[a-zA-Z]+\b', text.lower())

word_counts = Counter(words)

top_30_common_words = word_counts.most_common(30)


with open(output_csv_file, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Word', 'Count']) 
    writer.writerows(top_30_common_words)  

print(f"Top 30 common words (excluding numbers) have been written to {output_csv_file}")