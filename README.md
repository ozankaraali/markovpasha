# markovpasha
Markov Chain Text Generation Using existing Eksi Entries.

## Usage:
Run it with Markovify.py
```
import EksiEntriesRequest
import markovify

EksiEntriesRequest.fetch_entries('ttnet')

with open("input.txt") as f:
    text = f.read()

text_model = markovify.Text(text, state_size=2) #state_size=3

for i in range(5):
    print(text_model.make_sentence(tries=1000))
```


## Dependencies:
pycurl,
BeautifulSoup4,
requests,
markovify,
nltk
