import gradio as gr
from keras._tf_keras.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from PIL import Image
import numpy as np
import plotly.graph_objects as go

# Load the MobileNetV2 model
model = MobileNetV2(weights='imagenet', include_top=True)

# Example images and whether their predicted class is correct
example_images = [
    ("example_images/Hund.jpg", True),
    ("example_images/Auto.jpg", True),
    ("example_images/Quallen.jpg", True),
    ("example_images/Okapi.jpg", False),
    ("example_images/Obstkorb.png", False),
    ("example_images/Riesenrad.jpg", False)
]

# Preprocess an image for classification with MobileNetV2
def preprocess_image(image):
    img = image.resize((224, 224))
    img_array = np.array(img)
    img_array = preprocess_input(img_array)
    return img_array[None, ...]

def load_image(path):
    image = Image.open(path)
    image = image.resize((1750, 1080))
    return image

def display_examples(title, examples):
    gr.Markdown(f"# {title}:")
    for path, correct in examples:
        with gr.Row():
            with gr.Column():
                image = load_image(path)
                label, plot = classify_and_plot(image, correct)
                gr.Image(image, label=f"Predicted: {format_label(label)}")
            with gr.Column():
                gr.Plot(plot)

# Format lower_case to Natural Language
def format_label(label):
    return ' '.join(word.capitalize() for word in label.split('_'))

# Create a Plotly bar chart with colored border
def create_plot(decoded_predictions, correct_classification):
    labels, probabilities = zip(*[(format_label(label), round(prob * 100, 1)) for _, label, prob in decoded_predictions])
    fig = go.Figure([go.Bar(x=labels, y=probabilities)])
    fig.update_layout(
        title='Top 4 Predictions',
        xaxis_title='Classes',
        yaxis_title='Confidence (in %)',
        
        paper_bgcolor=('rgba(50,205,50, 1)' if correct_classification is True else 'rgba(219, 102, 79, 1)' if correct_classification is False else 'rgba(255,255,255,1)'),
    )
    # Update bar text for actual percentages
    fig.update_traces(text=probabilities, textposition='auto')
    return fig

# Process image, make predictions and generate plot
def classify_and_plot(image, correct_classification=None):
    if image is None:
        return gr.Label("Not a valid image. Please try again!"), None
    
    preprocessed_image = preprocess_image(image)
    predictions = model.predict(preprocessed_image)
    decoded_predictions = decode_predictions(predictions, top=4)[0]
    return decoded_predictions[0][1], create_plot(decoded_predictions, correct_classification)

# Define Gradio layout using Blocks
with gr.Blocks(css="footer{display:none !important}") as app:
    gr.Markdown("""# Bilderkennung mit MobileNetV2""")
    with gr.Row():
        with gr.Column():
            output_label = gr.Label("Lade ein Bild hoch, um es zu klassifizieren")
            img_input = gr.Image(type="pil", label="Image Upload")
            classify_button = gr.Button("Klassifizieren")
        with gr.Column():
            output_plot = gr.Plot()
            classify_button.click(fn=classify_and_plot, inputs=img_input, outputs=[output_label, output_plot])

    display_examples("Beispiele für korrekte Klassifikation", example_images[:3])
    display_examples("Beispiele für falsche Klassifikation", example_images[3:])

    gr.Markdown("""
        # Diskussion
        Für die Aufgabe habe ich diese Beispielbilder gewählt, weil sie verschiedene Besonderheiten aufweisen. 
        Das genutzte Modell wurde mit einer großen Menge an Bilddaten trainiert, insbesondere Bilder von Hunderassen wie der Golden Retriever.
        Deswegen ist die Confidence hier sehr hoch (über 85 %), Platz 2 ist hier erst im niedrigen Prozentbereich.
        Außerdem habe ich ein Bild eines Autorennspiels mit zwei Sportwagen gewählt und eine relative sichere Prediction von ca. 61 % erhalten. 
        Allerdings ist die Confidence beim Quallenbild deutlich geringer (ca. 17 %), weil es ähnlich wie Spinnennetzfäden aussieht.
                
        Das Okapi konnte nicht richtig klassifiziert werden und wurde wie gedacht zu 11 % vom Modell für ein Zebra gehalten (ähnliches Beinmuster).
        Zudem hat der Ausschnitt eines Riesenrads nicht gereicht, um es richtig zu klassifizeren (wieder ähnlich zu einem Spinnennetz, hier ist die Confidence aber nur im einstelligen Bereich).
        Da der Obstkorb mehrere Früchte enthält, konnte er auch nicht erkannt werden, aber zwei der Obstsorten auf dem Bild zu ca. 34 und 19 %. 
                
        Ich habe gelernt, dass das Modell auch KI-generierte Bilder klassifizieren kann.
        Werden Bilder bearbeitet, sind aus einem Cartoon, haben schlechte Lichtverhältnisse oder werden mit anderen Objekten zusammen abgebildet, so wird das Modell deutlich schlechter abschneiden.
        Dies gilt auch beim Skalieren/Verändern der Bildgrößen.
        Daher ist es wichtig, den Wert der Confidence zu betrachten und ein geeignetes Modell für die Bilddaten zu wählen.
    """)
    with gr.Row():
        with gr.Column():
            gr.Markdown("""# Technische Dokumentation
                Gradio: Zur Anzeige der UI-Elemente\n
                TensorFlow Keras: Um das MobileNetV2-Modell zu laden und für die Funktionen zur Input-Vorverarbeitung und Dekodieren der Predictions\n
                Plotly: Zur Visualisierung der Diagramme\n
                Python Imaging Library (PIL): Um die Beispielbilder aus dem Pfad zu laden\n\n
                Das Besondere an dieser Lösung ist die einfache Benutzerfreundlichkeit aufgrund des gewählten UI-Frameworks Gradio. Zudem ist sie einfach verständlich durch die populäre Python-Programmiersprache und dank der verschiedenen Bibliotheken beliebig erweiterbar.
            """)
        with gr.Column():
            gr.Markdown("""
                # Fachliche Dokumentation
        
                ## Ansatz:
                Die Implementierung nutzt das MobileNetV2-Modell für die Bildklassifizierung. Es wurde mit dem ImageNet-Datensatz trainiert. 
                Die Anwendung funktioniert folgendermaßen: Der Benutzer lädt ein Bild hoch, es passieren verschiedene logische Schritte und 
                die Ergebnisse werden dem Benutzer in Form eines Balkendiagramms angezeigt (Klassenbeschriftung und Confidence). 

                ## Logik:
                Die Logik der Implementierung kann wie folgt unterteilt werden: \n
                1. Das MobileNetV2-Modell wird mit den Standardgewichten initialisiert \n
                2. Funktion zur Bildvorverabeitung (in ein Format konvertieren, das vom Modell erwartet wird) \n
                3. Funktion zur Klassifizierung (gibt die 4 wahrscheinlichsten Klassen mit ihrer Confidence aus) \n
                4. Funktion zur Visualisierung der Diagramme \n
                5. Gradio zeigt die UI-Elemente an
                    
                ## Bildquellen und hilfreiche Links:
                - Forza (2022): Forza Horizon 5 Series 7 Update. Online: https://forza.net/news/forza-horizon-5-series-7-update \n
                - Gradio (o. A.): Image Classification in TensorFlow and Keras. Online: https://www.gradio.app/guides/image-classification-in-tensorflow
                - Green Hills Ecotours (o. A.): Okapi Wildlife Reserve in DR Congo: Online: http://www.greenhillsecotours.com/okapi-wildlife-reserve-in-dr-congo/ \n
                - Hugging Face (o. A.): Introduction to Gradio Blocks. Online: https://huggingface.co/learn/nlp-course/en/chapter9/7 \n
                - Pixabay (JörgHerrich): Früchtekorb. Online: https://pixabay.com/de/illustrations/fr%C3%BCchtekorb-obst-obstkorb-8410566/ \n
                - Pixabay (mreyati): AI Generated Golden Retriever. Online: https://pixabay.com/illustrations/ai-generated-golden-retriever-puppy-8601608/ \n
                - Pixabay (sonharam0): Skotcho Eye, Ferris Wheel. Online: https://pixabay.com/photos/sokcho-eye-ferris-wheel-sky-7711019/ \n
                - Pixabay (StockSnap): Jellyfish. Online: https://pixabay.com/photos/jellyfish-aquatic-animal-ocean-2566795/ 
            """)
    with gr.Row():
        with gr.Column():
            gr.Markdown("""### Medieninformatik-Wahlpflichtmodul: Deep Learning - ESA 1""")
        with gr.Column():
            gr.Markdown("""### Erstellt und abgegeben am 4. Mai 2024 von: Bjarne Niklas Luttermann (373960, TH Lübeck)""")

app.launch()