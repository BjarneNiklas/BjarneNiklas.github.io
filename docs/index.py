import os
import re
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import gradio as gr
import time

# Funktion zum Bereinigen des Textes
def clean_text(text):
    text = re.sub(r'\([^)]*\)', '', text)  # Entfernt alles zwischen ( und )
    text = re.sub(r'\[[^]]*\]', '', text)  # Entfernt alles zwischen [ und ]
    text = re.sub(r'\d+', '', text)  # Entfernt alle Zahlen
    text = re.sub(r'\s+', ' ', text).strip()  # Reduziert mehrere Leerzeichen auf ein Leerzeichen
    return text

# Dateipfade
input_path_primary = 'docs\Corpus.txt'
input_path_secondary = '/kaggle/input/corpus/Corpus.txt'
output_path = 'docs\Corpus-cleaned.txt'
model_path = 'docs\word_prediction_model.keras'  # Keras Format
tokenizer_path = 'docs\tokenizer.pickle'

# Text bereinigen und speichern, falls die bereinigte Datei nicht existiert
if os.path.exists(input_path_primary):
    input_path = input_path_primary
elif os.path.exists(input_path_secondary):
    input_path = input_path_secondary
else:
    raise FileNotFoundError("Keiner der angegebenen Eingabepfade existiert.")

if not os.path.exists(output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        text = file.read()

    cleaned_text = clean_text(text)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

# Modell trainieren oder laden, falls bereits trainiert
if os.path.exists(model_path) and os.path.exists(tokenizer_path):
    model = tf.keras.models.load_model(model_path)
    with open(tokenizer_path, 'rb') as handle:
        tokenizer = pickle.load(handle)
else:
    with open(output_path, 'r', encoding='utf-8') as file:
        cleaned_text = file.read()

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts([cleaned_text])
    total_words = len(tokenizer.word_index) + 1
    input_sequences = []

    for line in cleaned_text.split('.'):
        token_list = tokenizer.texts_to_sequences([line])[0]
        for i in range(1, len(token_list)):
            n_gram_sequence = token_list[:i+1]
            input_sequences.append(n_gram_sequence)

    max_sequence_len = max([len(x) for x in input_sequences])
    input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

    X, y = input_sequences[:, :-1], input_sequences[:, -1]
    y = tf.keras.utils.to_categorical(y, num_classes=total_words)

    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(total_words, 100, input_length=max_sequence_len-1),
        tf.keras.layers.LSTM(100, return_sequences=True),
        tf.keras.layers.LSTM(100),
        tf.keras.layers.Dense(total_words, activation='softmax')
    ])

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X, y, epochs=1, batch_size=32)

    model.save(model_path)  # Im Keras Format speichern

    with open(tokenizer_path, 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Gradio Schnittstelle
max_sequence_len = model.input_shape[1] + 1
stop_signal = False

def predict_next_words(prompt, top_k=5):
    tokens = tokenizer.texts_to_sequences([prompt])
    padded_seq = pad_sequences(tokens, maxlen=max_sequence_len-1, padding='pre')
    predictions = model.predict(padded_seq)
    top_indices = np.argsort(predictions[0])[-top_k:][::-1]
    top_words = [(tokenizer.index_word.get(i, ''), predictions[0][i]) for i in top_indices]
    return top_words

def generate_text(prompt, num_words=10):
    result = prompt
    used_words = set()
    for _ in range(num_words):
        next_word = predict_next_words(result, top_k=1)[0][0]
        if next_word not in used_words:
            result += ' ' + next_word
            used_words.add(next_word)
        else:
            break
    return result

def append_word(prompt):
    next_word = predict_next_words(prompt, top_k=1)[0][0]
    return prompt + ' ' + next_word

def auto_generate_text(prompt):
    global stop_signal
    stop_signal = False
    generated_text = prompt
    used_words = set()
    word_count = 0
    while not stop_signal and word_count < 10:
        next_word = predict_next_words(generated_text, top_k=1)[0][0]
        generated_text += ' ' + next_word
        used_words.add(next_word)
        word_count += 1
        yield generated_text
        time.sleep(0.2)

def stop_auto_generation():
    global stop_signal
    stop_signal = True

def append_clicked_word(evt, prompt):
    clicked_word = evt.value.split()[0]
    return prompt + ' ' + clicked_word

with gr.Blocks() as demo:
    gr.Markdown("## LSTM-basierte Wortvorhersage")

    input_text = gr.Textbox(label="Eingabetext")
    prediction_button = gr.Button("Vorhersage")
    top_words = gr.Dataframe(headers=["Wort", "Wahrscheinlichkeit"], datatype=["str", "number"], interactive=True)
    auto_generate_button = gr.Button("Auto-Generierung")
    stop_button = gr.Button("Stop")
    continue_button = gr.Button("Weiter")
    reset_button = gr.Button("Reset")

    gr.Row(input_text, prediction_button, top_words)
    gr.Row(auto_generate_button, stop_button)
    gr.Row(continue_button)
    gr.Row(reset_button)

    def update_perplexity_and_predict(text):
        predictions = predict_next_words(text)
        return predictions

    input_text.change(fn=update_perplexity_and_predict, inputs=input_text, outputs=[top_words])
    prediction_button.click(fn=update_perplexity_and_predict, inputs=input_text, outputs=[top_words])
    continue_button.click(fn=append_word, inputs=input_text, outputs=input_text)
    auto_generate_button.click(fn=auto_generate_text, inputs=input_text, outputs=input_text)
    stop_button.click(fn=stop_auto_generation)
    reset_button.click(fn=lambda: '', outputs=[input_text])

demo.launch()
