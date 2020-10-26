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
import base64
from io import BytesIO
from datetime import datetime

from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import models as models
import numpy as np
import locale


def train_target_score_model(imagesPath, modelPath, tensorboard_gcs_logs, epochs_count, batch_size):
    train_images_dir = imagesPath
    scores_file = os.path.join(imagesPath, "scores.json")
    
    IMAGE_SIZE = 128

    with open(scores_file) as f:
        train_data = json.load(f)

    labels = []
    img_data = []
    img_index = 0
    #tensorboard_gcs_logs = 'gs://dpa23/tarsanlogs'
    img_to_show = []

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
        if img_index < 10:
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8") 
            img_to_show.append((img_base64, score, 0.0))

        add_image(img, 0, score)
        add_image(img, 45, score)
        add_image(img, 90, score)
        add_image(img, 135, score)

        img_index = img_index + 1

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
        log_dir=tensorboard_gcs_logs +'/' + datetime.now().strftime("%Y%m%d-%H%M%S"),
        histogram_freq=5,
        write_images=True,
        update_freq='epoch'
    )

    keras_callbacks = []
    if len(tensorboard_gcs_logs) > 2:
        keras_callbacks = [
            tensorboard
        ]

    # train the model
    print("[INFO] training model...")
    model.fit(trainImagesX, trainY, validation_data=(testImagesX, testY), 
        epochs=epochs_count, batch_size=batch_size, callbacks=keras_callbacks)

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

    img_html = '<table><tr><th>Target</th><th>Actual Score</th><th>Predicted Score</th></tr>'

    for (img_b64, s1, s2) in img_to_show:
        html_line = '<tr><td><img src="data:image/png;base64, {}" alt="Target Example"></td><td>{}</td><td>{}</td></tr>'.format(img_b64, s1, s2)
        img_html = img_html + html_line
    
    img_html = img_html + '</table>'

    metadata = {
        'outputs' : [
            {
                'storage':'inline',
                'source': 'Markdown text',
                'type': 'markdown',
            },
             {
                'type': 'web-app',
                'storage': 'inline',
                'source': img_html,
            },
            {
                'type': 'tensorboard',
                'source': tensorboard_gcs_logs,
            }]
        }
    
    with open('/mlpipeline-ui-metadata.json', 'w') as f:
        json.dump(metadata, f)

    print("[INFO] mean: {:.2f}%, std: {:.2f}%".format(mean, std))
