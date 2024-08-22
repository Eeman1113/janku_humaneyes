# pages/api/humanize.py
from http.server import BaseHTTPRequestHandler
import nltk
from nltk.corpus import wordnet, stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import random
import re
import json
import traceback

try:
    # Download NLTK resources
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('stopwords', quiet=True)

    # Get English stopwords
    stop_words = set(stopwords.words('english'))

    def get_synonyms(word):
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonym = lemma.name().replace('_', ' ')
                if synonym.isalpha() and len(synonym.split()) == 1 and len(synonym) <= 10:
                    synonyms.add(synonym)
        return synonyms

    def introduce_human_errors(text):
        words = text.split()
        for i in range(len(words)):
            if i % 10 == 0 and i != 0:
                words[i] = " " + words[i]  # Introduce a double space
        return ' '.join(words)

    def paraphrase_sentence(sentence):
        quote_pattern = r'(".*?")'
        parts = re.split(quote_pattern, sentence)
        
        new_parts = []
        for part in parts:
            if part.startswith('"') and part.endswith('"'):
                new_parts.append(part)  # Keep quoted text as is
            else:
                words = word_tokenize(part)
                pos_tags = nltk.pos_tag(words)
                new_words = []

                num_words_to_replace = int(len(words) * 0.42)  # Replace approximately 42% of words
                words_replaced = 0

                for word, tag in pos_tags:
                    if words_replaced >= num_words_to_replace:
                        new_words.append(word)
                    elif tag.startswith('NN') or tag.startswith('VB') or tag.startswith('JJ') or tag.startswith('RB'):
                        if word.lower() not in stop_words:
                            synonyms = get_synonyms(word)
                            if synonyms:
                                synonym = random.choice(list(synonyms))
                                new_words.append(synonym)
                                words_replaced += 1
                            else:
                                new_words.append(word)
                        else:
                            new_words.append(word)
                    else:
                        new_words.append(word)

                new_parts.append(' '.join(new_words))

        return ''.join(new_parts)

    def paraphrase_text(input_text):
        paragraphs = input_text.split('\n\n')
        paraphrased_paragraphs = []

        for paragraph in paragraphs:
            sentences = sent_tokenize(paragraph)
            paraphrased_sentences = [paraphrase_sentence(sentence) for sentence in sentences]
            paraphrased_paragraph = ' '.join(paraphrased_sentences)
            paraphrased_paragraph = introduce_human_errors(paraphrased_paragraph)
            paraphrased_paragraphs.append(paraphrased_paragraph)

        return '\n\n'.join(paraphrased_paragraphs)

    class handler(BaseHTTPRequestHandler):
        def do_POST(self):
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                input_text = data.get('text', '')
                
                if input_text:
                    paraphrased_text = paraphrase_text(input_text)
                    response = {'paraphrased_text': paraphrased_text}
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                else:
                    raise ValueError('No text provided')
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error_message = f"An error occurred: {str(e)}\n{traceback.format_exc()}"
                self.wfile.write(json.dumps({'error': error_message}).encode('utf-8'))

except Exception as e:
    print(f"Initialization error: {str(e)}")
    traceback.print_exc()