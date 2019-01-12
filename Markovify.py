import markovify
import nltk
import re
import EksiEntriesRequest
import os

header = "ttnet"
EksiEntriesRequest.fetch_entries(header)


class NaturalLanguageText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = ["::".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


combined_model = None
for (dir_path, _, file_names) in os.walk("./data/"):
    for filename in file_names:
        if filename != ".DS_Store":
            with open(os.path.join(dir_path, filename)) as f:
                model = NaturalLanguageText(f, state_size=2, retain_original=False)
                if combined_model:
                    combined_model = markovify.combine(models=[combined_model, model])
                else:
                    combined_model = model

for i in range(5):
    print(combined_model.make_short_sentence(300, 150, tries=1000))
