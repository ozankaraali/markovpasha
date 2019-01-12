import markovify
import nltk
import re
import EksiEntriesRequest

nltk.download('averaged_perceptron_tagger')

#EksiEntriesRequest.fetch_entries('hepsiburada.com')


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

with open("hepsiburadacom.txt") as f:
    textinput = f.read()

with open("ttnet.txt") as f:
    textttnet = f.read()

with open("playstation.txt") as f:
    textplaystation = f.read()

# Build the model.
text_modeli = POSifiedText(textinput, state_size=3)
text_modelp = POSifiedText(textttnet, state_size=3)
text_modelt = POSifiedText(textplaystation, state_size=3)

model_combo = markovify.combine([ text_modeli, text_modelp, text_modelt ], [ 1, 1, 1 ])

# Print five randomly-generated sentences
for i in range(5):
    print(model_combo.make_short_sentence(500,300,tries=1000))