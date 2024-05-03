import gradio as gr
import tensorflow as tf
from keras._tf_keras.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from PIL import Image
import numpy as np
import plotly.graph_objects as go

# Load the MobileNetV2 model
model = MobileNetV2(weights='imagenet', include_top=True)

def preprocess_image(image):
    """Preprocesses an image for classification with MobileNetV2."""
    img = image.resize((224, 224))  # Resize to the input size required by MobileNetV2
    img_array = np.array(img) # Convert to numpy array
    img_array = preprocess_input(img_array)  # Preprocess input
    return img_array[None, ...]

def classify_image(image):
    """Classifies an image with MobileNetV2 and returns the top-5 results."""
    preprocessed_image = preprocess_image(image)
    predictions = model.predict(preprocessed_image)
    decoded_predictions = decode_predictions(predictions, top=5)[0]
    return {f"{label} ({class_id})": float(prob) for class_id, label, prob in decoded_predictions}

def create_plot(decoded_predictions):
    """Creates a Plotly bar chart showing the top-5 predicted classes with probabilities."""
    labels, probabilities = zip(*[(f"{label} ({class_id})", prob) for class_id, label, prob in decoded_predictions])
    fig = go.Figure([go.Bar(x=labels, y=probabilities)])
    fig.update_layout(title='Top-5 Predictions', xaxis_title='Classes', yaxis_title='Probability')
    return fig

def wrap_classification_with_plot(image):
    """Wrapper function to handle classification and plotting."""
    preprocessed_image = preprocess_image(image)
    predictions = model.predict(preprocessed_image)
    decoded_predictions = decode_predictions(predictions, top=5)[0]
    plot = create_plot(decoded_predictions)
    predicted_class = decoded_predictions[0][1]  # Highest probability class label
    return predicted_class, plot

# Create the Gradio interface
interface = gr.Interface(
    fn=wrap_classification_with_plot,
    inputs=gr.Image(type="pil", label="Upload an Image"),
    outputs=[
        gr.Textbox(label="Predicted Class"),
        gr.Plot(label="Probability Distribution")
    ],
    title="MobileNetV2 Image Classification",
    description="Upload an image to classify with MobileNetV2 and see the top-5 predictions."
)

# Launch the Gradio application
interface.launch()

"""

    # Top 5 Vorhersagen dekodieren
    decoded = decode_predictions(prediction, top=5)[0]
    # Formatieren der Ausgabe für Anzeige
    return ", ".join([f"{d[1]}: {np.round(d[2], 4)*100}%" for d in decoded])

# GUI definieren
interface = gr.Interface(
    fn=classify_image,
    inputs=gr.Image(label="Bild-Upload"),
    outputs=gr.Label(label="Confidence"),

    examples=[
        'example_images/correct1.jpg',
        'example_images/correct2.jpg',
        'example_images/correct3.jpg',
        'example_images/incorrect1.jpg',
        'example_images/incorrect2.jpg',
        'example_images/incorrect3.jpg'
    ]
)

"""
"""


interface = gr.Interface(
    fn=classify_image,
    inputs = gr.components.Image(label="Bild-Upload"),
    outputs = gr.components.Label(label="Confidence", num_top_classes=3),
    examples=[
        ['example_images/correct1.jpg'],
        ['example_images/correct2.jpg'],
        ['example_images/correct3.jpg'],
        ['example_images/incorrect1.jpg'],
        ['example_images/incorrect2.jpg'],
        ['example_images/incorrect3.jpg']
    ],
)


"""



"""

css="footer{display:none !important}

 title="Bilderkennung mit MobileNetV2",
    description="Lade ein Bild zur Klassifikation hoch. Das Modell verwendet MobileNetV2 (trainiert auf ImageNet).",

zur Doku:
1. ein Bild aus dem Datensatz, ich habe damit gerechnet dass es 100% richtig klassifiziert wird
2. ein bild von 
3. ein bild von...

1.

3. etwas ziemlich neues, zB ein neues fahrzeug das anders aussieht

"""