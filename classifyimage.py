import sys
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

def load_model(model_path):
    return tf.keras.models.load_model(model_path)

def preprocess_image(img_path, target_size=(150, 150)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Rescale the image array
    return img_array

def classify_image(model, img_array):
    prediction = model.predict(img_array)
    return 'yes' if prediction[0][0] > 0.5 else 'no'

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python classify_image.py <model_path> <image_path>")
        sys.exit(1)

    model_path = sys.argv[1]
    image_path = sys.argv[2]

    if not os.path.isfile(model_path):
        print(f"Error: {model_path} is not a valid file.")
        sys.exit(1)

    if not os.path.isfile(image_path):
        print(f"Error: {image_path} is not a valid file.")
        sys.exit(1)

    model = load_model(model_path)
    img_array = preprocess_image(image_path)
    result = classify_image(model, img_array)

    print(f"The image is classified as: {result}")