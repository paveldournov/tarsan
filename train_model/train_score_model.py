from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import array_to_img
from tensorflow import keras
from tensorflow.keras.preprocessing import image_dataset_from_directory
from keras.callbacks import TensorBoard
from time import time
import tensorflow as tf
import os
import json

from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import models as models
import numpy as np
import locale


def train_target_score_model(imagesPath, modelPath):
    train_images_dir = imagesPath
    scores_file = os.path.join(imagesPath, "scores.json")
    
    IMAGE_SIZE = 128

    with open(scores_file) as f:
        train_data = json.load(f)

    labels = []
    img_data = []
    first = True

    def add_image(img, rotation, score):
        labels.append(score)

        if rotation != 0:
            r_image = img.rotate(rotation)
        else:
            r_image = img

        img_array = img_to_array(r_image) / 255.0
        img_data.append(img_array)


    for file_name, score in train_data.items():
        full_file_name = os.path.join(train_images_dir, file_name)
        print("Loading {} with score {}".format(full_file_name, score))
        img = load_img(full_file_name, color_mode="grayscale", target_size=(IMAGE_SIZE,IMAGE_SIZE), interpolation='bilinear')
        if first:
            img.show()
            first = False
        add_image(img, 0, score)
        add_image(img, 45, score)
        add_image(img, 90, score)
        add_image(img, 135, score)

    np_labels = np.asfarray(labels)
    np_image_data = np.asfarray(img_data)

    # partition the data into training and testing splits using 75% of
    # the data for training and the remaining 25% for testing
    split = train_test_split(np_labels, np_image_data, test_size=0.25, random_state=42)
    (trainAttrX, testAttrX, trainImagesX, testImagesX) = split

    # find the largest score  in the training set and use it to
    # scale the scores to  the range [0, 1]
    maxScore = trainAttrX.max()
    trainY = trainAttrX / maxScore
    testY = testAttrX / maxScore


    # create our Convolutional Neural Network and then compile the model
    # using mean absolute percentage error as our loss, implying that we
    # seek to minimize the absolute percentage difference between our
    # score *predictions* and the *actual score*
    model = models.create_cnn(IMAGE_SIZE, IMAGE_SIZE, 1, regress=True)
    opt = Adam(lr=1e-3, decay=1e-3 / 200)
    model.compile(loss="mean_absolute_percentage_error", optimizer=opt)

    # Define Tensorboard as a Keras callback
    tensorboard = TensorBoard(
        log_dir='.\logs',
        histogram_freq=1,
        write_images=True
    )

    keras_callbacks = [
        tensorboard
    ]

    # train the model
    print("[INFO] training model...")
    model.fit(trainImagesX, trainY, validation_data=(testImagesX, testY), 
        epochs=100, batch_size=50, callbacks=keras_callbacks)

    print("[INFO] saving model to {} ...".format(modelPath))
    model.save(modelPath)

    # make predictions on the testing data
    print("[INFO] predicting scores prices...")
    preds = model.predict(testImagesX)

    # compute the difference between the *predicted* scores and the
    # *actual* scores, then compute the percentage difference and
    # the absolute percentage difference
    diff = preds.flatten() - testY
    percentDiff = (diff / testY) * 100
    absPercentDiff = np.abs(percentDiff)

    # compute the mean and standard deviation of the absolute percentage
    # difference
    mean = np.mean(absPercentDiff)
    std = np.std(absPercentDiff)

    # finally, show some statistics on our model
    print("[INFO] avg. score: {}, std score: {}".format(
        np_labels.mean(),
        np_labels.std()))

    metrics = {
        'metrics': [{
            'name': 'diff-mean', 
            'numberValue':  mean, 
            'format': "PERCENTAGE",  
        }]
    }
    
    with open('/mlpipeline-metrics.json', 'w') as f:
        json.dump(metrics, f)

    metadata = {
        'outputs' : [
            # Markdown that is hardcoded inline
            {
                'storage': 'inline',
                'source': '# Inline Markdown\n[A link](https://www.kubeflow.org/)',
                'type': 'markdown',
            },
            # Markdown that is read from a file
            {
                'storage':'inline',
                'source': 'Markdown text',
                'type': 'markdown',
            }]
        }
    
    with open('/mlpipeline-ui-metadata.json', 'w') as f:
        json.dump(metadata, f)

    #metadata = {
    #    'outputs' : [{
    #    'type': 'tensorboard',
    #    'source': args.job_dir,
    #    }]
    #}

    #with open('/mlpipeline-ui-metadata.json', 'w') as f:
    #    json.dump(metadata, f)


    print("[INFO] mean: {:.2f}%, std: {:.2f}%".format(mean, std))
