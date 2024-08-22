import streamlit as st
import nltk
from nltk.corpus import wordnet, stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import random
import re

#darpan1985#

# Download NLTK resources
@st.cache_resource
def download_nltk_resources():
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    nltk.download('stopwords')

download_nltk_resources()

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
        elif i % 15 == 0 and i != 0:
            word = words[i]
            # if len(word) > 2:
            #     pos = random.randint(1, len(word) - 2)
            #     words[i] = word[:pos] + word[pos] * 2 + word[pos + 1:]  # Introduce a typo
    return ' '.join(words)

def paraphrase_sentence(sentence):
    # Preserve quotation marks
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

            num_words_to_replace = int(len(words) * 0.42)  # Replace approximately 5% of words
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

def main():
    st.title("Humanizer")

    input_text = st.text_area("Enter text to humanize:", height=200)

    if st.button("Paraphrase"):
        if input_text:
            with st.spinner("Paraphrasing..."):
                paraphrased_text = paraphrase_text(input_text)
            st.subheader("Humanized Text:")
            # paraphrased_text = paraphrased_text.replace('``','"')
            st.text_area("", value=paraphrased_text, height=200, key="output")
            st.button("Copy to Clipboard", on_click=lambda: st.write("Text copied to clipboard!"))
        else:
            st.warning("Please enter text to paraphrase.")

if __name__ == "__main__":
    main()