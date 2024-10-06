from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding
from tensorflow.keras.models import Sequential

# Sample Sentences
sent = [
    'the glass of milk',
    'the glass of juice',
    'the cup of tea',
    'I am a good boy',
    'I am a good developer',
    'understand the meaning of words',
    'your videos are good',
]

# Define Vocabulary Size
voc_size = 10000

# One Hot Representation
one_hot_rep = [one_hot(words, voc_size) for words in sent]
print("One Hot Representation:")
print(one_hot_rep)

# Define the maximum length for padding
sent_length = 8

# Pad the sequences
embedded_docs = pad_sequences(one_hot_rep, padding='pre', maxlen=sent_length)
print("Padded Sequences:")
print(embedded_docs)

# Feature Representation
dim = 10

# Define Model
model = Sequential()

# Add Embedding Layer (with correct parameters)
model.add(Embedding(input_dim=voc_size, output_dim=dim, input_length=sent_length))

# Compile the model
model.compile(optimizer='adam', loss='mse')

# Summary of the model
model.summary()
