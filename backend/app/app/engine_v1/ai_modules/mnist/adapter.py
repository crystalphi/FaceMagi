# -*- coding: utf-8 -*-
"""
model: Functions related to Deep Learning model based on Keras.
api: api views used by Flask server.
"""
__author__ = "vedasky"
__copyright__ = "Copyright 2019"

import io
import numpy as np
from flask import Blueprint, current_app, jsonify, request
from skimage.io import imread
from skimage import transform, util
from keras.models import load_model

from app.engine_v1 import app_config


def init_model():
    """Function that loads Deep Learning model.
    Returns:
        model: Loaded Deep Learning model.
    """

    model = load_model(app_config.MODEL_PATH["mnist"])
    model._make_predict_function()
    return model


def preprocess_image(image):
    """Function that preprocess image.
    Returns:
        image: Preprocessed image.
    """

    # invert grayscale image
    image = util.invert(image)
    # resize and reshape image for model
    image = transform.resize(
        image, (28, 28), anti_aliasing=True, mode="constant")
    image = np.array(image)
    image = image.reshape((1, 28*28))

    return image


def mnist_predict():
    # result dictionary that will be returned from the view
    result = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if request.method == "POST":
        if request.files.get("file"):
            # read image as grayscale
            image_req = request.files["file"].read()
            request.files["file"].close()
            image = imread(io.BytesIO(image_req), as_gray=True)

            # preprocess the image for model
            preprocessed_image = preprocess_image(image)

            # classify the input image generating a list of predictions
            model = app_config["model"]["minist"]
            preds = model.predict(preprocessed_image)

            # add generated predictions to result
            result["predictions"] = []

            for i in range(0, 10):
                pred = {"label": str(i), "probability": str(preds[0][i])}
                result["predictions"].append(pred)

            result["most_probable_label"] = str(np.argmax(preds[0]))

            # indicate that the request was a success
            result["success"] = True

    # return result dictionary as JSON response to client
    return jsonify(result)
