import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Input
from tensorflow.keras.callbacks import EarlyStopping
from collections import Counter

def create_image_generators(directory):
    train_datagen = ImageDataGenerator(rescale=0.2, validation_split=0.2)

    train_generator = train_datagen.flow_from_directory(
        directory,
        target_size=(150, 150),
        batch_size=32,
        class_mode='binary',
        subset='training'
    )

    validation_generator = train_datagen.flow_from_directory(
        directory,
        target_size=(150, 150),
        batch_size=32,
        class_mode='binary',
        subset='validation'
    )

    return train_generator, validation_generator

def build_model():
    model = Sequential([
        Input(shape=(150, 150, 3)),
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def compute_class_weights(generator):
    counter = Counter(generator.classes)
    majority = max(counter.values())
    return {cls: float(majority / count) for cls, count in counter.items()}

def train_model(model, train_generator, validation_generator, epochs=50):
    steps_per_epoch = len(train_generator)
    validation_steps = len(validation_generator)

    class_weights = compute_class_weights(train_generator)

    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    history = model.fit(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        validation_steps=validation_steps,
        epochs=epochs,
        validation_data=validation_generator,
        class_weight=class_weights,
        callbacks=[early_stopping]
    )
    return history

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python buildmodel.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)

    train_generator, validation_generator = create_image_generators(directory)
    model = build_model()
    history = train_model(model, train_generator, validation_generator, epochs=50)

    model.save('image_classification_model.h5')
    print("Model saved as image_classification_model.h5")