import markovify
import nltk
import re
import EksiEntriesRequest
import os

baslik = "ttnet"

EksiEntriesRequest.fetch_entries(baslik)

class NaturalLanguageText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = ["::".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

combined_model = None
for (dirpath, _, filenames) in os.walk("./data/"):
    for filename in filenames:
        if filename != ".DS_Store":
            with open(os.path.join(dirpath, filename)) as f:
                model = NaturalLanguageText(f, state_size=3, retain_original=False)
                if combined_model:
                    combined_model = markovify.combine(models=[combined_model, model])
                else:
                    combined_model = model

# Print five randomly-generated sentences
for i in range(5):
    print(combined_model.make_short_sentence(500,300,tries=1000))
