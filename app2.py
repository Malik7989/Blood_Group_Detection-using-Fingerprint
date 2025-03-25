# # import os
# # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logs
# # os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable oneDNN custom operations
# import tensorflow as tf


# import tensorflow as tf
# import os



# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report, accuracy_score
# import numpy as np
# import cv2
# import os
# import matplotlib.pyplot as plt

# def load_dataset(dataset_path, img_size=(128, 128)):
#     images, labels = [], []
#     blood_groups = ['A', 'B', 'AB', 'O']
    
#     for label, blood_group in enumerate(blood_groups):
#         blood_group_dir = os.path.join(dataset_path, blood_group)
#         for img_name in os.listdir(blood_group_dir):
#             img_path = os.path.join(blood_group_dir, img_name)
#             img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
#             img = cv2.resize(img, img_size)
#             images.append(img)
#             labels.append(label)

#     images = np.array(images).reshape(-1, img_size[0], img_size[1], 1) / 255.0  # Normalize images
#     labels = np.array(labels)
#     return images, labels

# dataset_path = '"C:\Users\muni karthik\Desktop\blood group\blood_group_train"'
# images, labels = load_dataset(dataset_path)

# X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)
# data_gen = ImageDataGenerator(
#     rotation_range=10,
#     width_shift_range=0.1,
#     height_shift_range=0.1,
#     shear_range=0.1,
#     zoom_range=0.1,
#     horizontal_flip=True
# )
# data_gen.fit(X_train)
# def build_cnn_model(input_shape):
#     model = Sequential()

#     # Convolutional layers
#     model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
#     model.add(MaxPooling2D((2, 2)))

#     model.add(Conv2D(64, (3, 3), activation='relu'))
#     model.add(MaxPooling2D((2, 2)))

#     model.add(Conv2D(128, (3, 3), activation='relu'))
#     model.add(MaxPooling2D((2, 2)))

#     # Flatten and Dense layers
#     model.add(Flatten())
#     model.add(Dense(128, activation='relu'))
#     model.add(Dropout(0.5))  # To avoid overfitting
#     model.add(Dense(64, activation='relu'))
#     model.add(Dense(4, activation='softmax'))  # 4 classes for blood groups

#     # Compile model
#     model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
#     return model

# cnn_model = build_cnn_model((128, 128, 1))
# cnn_model.summary()
# history = cnn_model.fit(
#     data_gen.flow(X_train, y_train, batch_size=32),
#     validation_data=(X_test, y_test),
#     epochs=20
# )
# y_pred = np.argmax(cnn_model.predict(X_test), axis=-1)
# print(f'Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%')
# print(classification_report(y_test, y_pred, target_names=['A', 'B', 'AB', 'O']))
# plt.plot(history.history['accuracy'], label='Train Accuracy')
# plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
# plt.xlabel('Epochs')
# plt.ylabel('Accuracy')
# plt.legend()
# plt.show()

# plt.plot(history.history['loss'], label='Train Loss')
# plt.plot(history.history['val_loss'], label='Validation Loss')
# plt.xlabel('Epochs')
# plt.ylabel('Loss')
# plt.legend()
# plt.show()



import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


# Load your trained model
model = load_model('blood_group_classifier.h5')

def preprocess_image(image_path, img_size=(128, 128)):
    """
    Preprocess the image to match the model's expected input format.
    """
    # Load the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Check if image loading was successful
    if img is None:
        raise ValueError(f"Image not found or unable to load: {image_path}")
    
    # Resize the image to the required input size
    img = cv2.resize(img, img_size)
    
    # Normalize the image (0-1 range) and reshape to match input format
    img = img / 255.0
    img = img.reshape(1, img_size[0], img_size[1], 1)  # Add batch dimension
    
    return img

# Path to the new image
new_image_path = r"C:\Users\muni karthik\Desktop\blood group\test\B+\IMG20240915194232.jpg"
 # Replace with the actual image path

try:
    # Preprocess the image
    preprocessed_image = preprocess_image(new_image_path)

    # Make the prediction
    prediction = model.predict(preprocessed_image)

    # Get the predicted class index
    predicted_class = np.argmax(prediction, axis=1)[0]

    # Map the predicted index to the actual blood group label
    class_labels = ['A-', 'B-', 'AB-', 'O-', 'B+', 'A+', 'O+', 'AB+']
    
    if predicted_class < len(class_labels):
        predicted_label = class_labels[predicted_class]
        # Output the result
        print(f"The predicted blood group is: {predicted_label}")
    else:
        print(f"Prediction index {predicted_class} is out of range for blood group labels.")

except Exception as e:
    print(f"Error: {str(e)}")
