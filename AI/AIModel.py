# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 17:45:58 2024

@author: User
"""

import os
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Directory with training pictures
train_good_dir = os.path.join('E:\\Dataset\\train\\good-wheat')
train_damaged_dir = os.path.join('E:\\Dataset\\train\\damaged-wheat')

# Validation dataset
val_good_dir = os.path.join('E:\\Dataset\\validation\\val-good')
val_damaged_dir = os.path.join('E:\\Dataset\\validation\\val-damaged')

# Test dataset
test_good_dir = os.path.join('E:\\Dataset\\test\\test-good')
test_damaged_dir = os.path.join('E\\Dataset\\test\\test-damaged')

# Model definition
model = tf.keras.models.Sequential([
    # Convolutional layers
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(256, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    # Fully connected layers
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),  
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
optimizer1 = tf.keras.optimizers.Adam(learning_rate=0.0001)
model.compile(loss='binary_crossentropy',
              optimizer=optimizer1,
              metrics=['accuracy'])

# Organizing data into generators
# Data augmentation
train_datagen = ImageDataGenerator(
      rescale=1./255,
      rotation_range=20,
      width_shift_range=0.2,
      height_shift_range=0.2,
      shear_range=0.2,
      zoom_range=0.2,
      horizontal_flip=True,
      fill_mode='nearest'
)

# Flow training images in batches of 128 using train_datagen generator
train_generator = train_datagen.flow_from_directory(
        'E:\\Dataset\\train',  
        target_size=(100, 100),  
        batch_size=128,
        class_mode='binary')

validation_datagen = ImageDataGenerator(rescale=1./255)

validation_generator = validation_datagen.flow_from_directory(
        'E:\\Dataset\\validation',
        target_size=(100, 100),
        class_mode='binary')

# Test data generator
test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
        'E:\\Dataset\\test',
        target_size=(100, 100),
        class_mode='binary',
        shuffle=False)

# Calculate the total number of samples
total_samples = 1004
batch_size = 128
steps_per_epoch = total_samples // batch_size

# Training the model
history = model.fit(
    train_generator,
    steps_per_epoch=steps_per_epoch,
    epochs=20,
    verbose=1,
    validation_data=validation_generator)

# Plotting accuracy and loss
plt.figure(figsize=(12, 5))

# Plotting accuracy
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim(0, 1)  # Set y-axis limit from 0 to 1
plt.legend()

# Plotting loss
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.show()

# Get the predictions on the test data
y_pred = model.predict(test_generator)
y_pred = (y_pred > 0.5).astype(int)

# Get the true labels
y_true = test_generator.classes

# Calculate the confusion matrix
cm = confusion_matrix(y_true, y_pred)

# Visualize the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, cmap='Blues', fmt='g', xticklabels=['damaged', 'good'], yticklabels=['damaged', 'good'])
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix')
plt.show()
model.save('wheat_classification_model.h5')
# Convert model to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# Using float 16 quantization.
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float16]

# Converting the model
tflite_fp16_model = converter.convert()

# Saving the model.
with open('/content/fp_16_model.tflite', 'wb') as f:
  f.write(tflite_fp16_model)

