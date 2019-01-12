import markovify

# Get raw text as string.
with open("ttnet.txt") as f:
    text = f.read()

# Build the model.
text_model = markovify.Text(text, state_size=2)

# Print five randomly-generated sentences
for i in range(5):
    print(text_model.make_sentence(tries=1000))