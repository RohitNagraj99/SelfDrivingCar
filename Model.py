import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.optimizers import Adam
from keras.layers import Lambda, Conv2D, Dropout, Dense, Flatten
from utils import INPUT_SHAPE, batch_generator
import os

np.random.seed(0)


def load_data():
    """
    Load training data and split it into training and validation set
    """
    data_df = pd.read_csv(os.path.join(os.getcwd(), 'data', 'driving_log.csv'), names=[
                          'center', 'left', 'right', 'steering', 'throttle', 'reverse', 'speed'])

    X = data_df[['center', 'left', 'right']].values
    y = data_df['steering'].values

    X_train, X_valid, y_train, y_valid = train_test_split(
        X, y, test_size=0.2, random_state=0)

    return X_train, X_valid, y_train, y_valid


def build_model():
    """
    Image normalization to avoid saturation and make gradients work better.
    Convolution: 5x5, filter: 24, strides: 2x2, activation: RELU
    Convolution: 5x5, filter: 36, strides: 2x2, activation: RELU
    Convolution: 5x5, filter: 48, strides: 2x2, activation: RELU
    Convolution: 3x3, filter: 64, strides: 1x1, activation: RELU
    Convolution: 3x3, filter: 128, strides: 1x1, activation: RELU
    Drop out (0.2)
    Fully connected: neurons: 100, activation: RELU
    Fully connected: neurons: 50, activation: RELU
    Fully connected: neurons: 10, activation: RELU
    Fully connected: neurons: 1 (output)
    """
    model = Sequential()
    model.add(Lambda(lambda x: x/127.5-1.0, input_shape=INPUT_SHAPE))
    model.add(Conv2D(24, 5, 5, activation='relu', subsample=(2, 2)))
    model.add(Conv2D(36, 5, 5, activation='relu', subsample=(2, 2)))
    model.add(Conv2D(48, 5, 5, activation='relu', subsample=(2, 2)))
    model.add(Conv2D(64, 3, 3, activation='relu'))
    model.add(Conv2D(128, 3, 3, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(100, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(1))
    model.summary()

    return model


def train_model(model, X_train, X_valid, y_train, y_valid):
    """
    Train the model
    """
    model.compile(loss='mean_squared_error',
                  optimizer=Adam(lr=1e-3), metrics=['accuracy'])

    model.fit_generator(batch_generator('data', X_train, y_train, 40, True),
                        10000,
                        20,
                        max_q_size=1,
                        validation_data=batch_generator(
        'data', X_valid, y_valid, 40, False),
        nb_val_samples=len(X_valid),
        verbose=1)
    model.save('model.h5')


def main():
    """
    Load train/validation data set and train the model
    """
    data = load_data()
    model = build_model()
    train_model(model, *data)


if __name__ == '__main__':
    main()
