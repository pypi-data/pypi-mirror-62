# -*- coding: utf-8 -*-

import os

from absl import logging
import tensorflow as tf
from sklearn.metrics import f1_score, precision_score, recall_score, classification_report

from fancy_nlp.utils import TextClassificationGenerator
from fancy_nlp.callbacks import TextClassificationMetric
from fancy_nlp.callbacks import SWA


class TextClassificationTrainer(object):
    def __init__(self, model, preprocessor):
        """

        Args:
            model: instance of keras Model
            preprocessor: instance of TextClassificationPreprocessor
        """
        self.model = model
        self.preprocessor = preprocessor

    def train(self, train_data, train_labels, valid_data=None, valid_labels=None, batch_size=32,
              epochs=5, callback_list=None, checkpoint_dir=None, model_name=None, swa_model=None,
              load_swa_model=False):
        callbacks = self.prepare_callback(callback_list, valid_data, valid_labels, checkpoint_dir,
                                          model_name, swa_model)

        train_features, train_y = self.preprocessor.prepare_input(train_data, train_labels)
        if valid_data is not None and valid_labels is not None:
            valid_features, valid_y = self.preprocessor.prepare_input(valid_data, valid_labels)
            validation_data = (valid_features, valid_y)
        else:
            validation_data = None

        logging.info('Training start...')
        self.model.fit(x=train_features, y=train_y, batch_size=batch_size, epochs=epochs,
                       validation_data=validation_data, callbacks=callbacks)
        logging.info('Training end...')

        if load_swa_model and callback_list is not None and 'swa' in callback_list:
            logging.info('Loading swa model after using SWA callback')
            self.load_model_weights(os.path.join(checkpoint_dir, f'{model_name}_swa.hdf5'))

        elif callback_list is not None and 'modelcheckpoint' in callback_list:
            logging.info('Loading best model after using ModelCheckpoint callback...')
            self.load_model_weights(os.path.join(checkpoint_dir, f'{model_name}.hdf5'))

    def train_generator(self, train_data, train_labels, valid_data=None, valid_labels=None,
                        batch_size=32, epochs=50, callback_list=None, checkpoint_dir=None,
                        model_name=None, swa_model=None, load_swa_model=False):
        callbacks = self.prepare_callback(callback_list, valid_data, valid_labels, checkpoint_dir,
                                          model_name, swa_model)

        train_generator = TextClassificationGenerator(
            self.preprocessor, train_data, train_labels, batch_size)

        if valid_data and valid_labels:
            valid_generator = TextClassificationGenerator(
                self.preprocessor, valid_data, valid_labels, batch_size)
        else:
            valid_generator = None

        logging.info('Training start...')
        # Note: Model.fit now supports generators
        self.model.fit(x=train_generator,
                       epochs=epochs,
                       callbacks=callbacks,
                       validation_data=valid_generator)
        logging.info('Training end...')

        if load_swa_model and callback_list is not None and 'swa' in callback_list:
            logging.info('Loading swa model after using SWA callback')
            self.load_model_weights(os.path.join(checkpoint_dir, f'{model_name}_swa.hdf5'))

        elif callback_list is not None and 'modelcheckpoint' in callback_list:
            logging.info('Loading best model after using ModelCheckpoint callback...')
            self.load_model_weights(os.path.join(checkpoint_dir, f'{model_name}.hdf5'))

    def prepare_callback(self, callback_list, valid_data=None, valid_labels=None,
                         checkpoint_dir=None, model_name=None, swa_model=None):
        """

        Args:
            callback_list: list of str, each item indicate the callback to apply during training.
                       For example, 'earlystopping' means using 'EarlyStopping' callback.
            valid_data: list of tokenized (in char level) texts for evaluation
            valid_labels: labels string of valid data
            checkpoint_dir: str, directory to save ner model, must be provided when using
                            `ModelCheckpoint` or `SWA` callback.
            model_name: str, prefix of ner model's weights filem must be provided when using
                        `ModelCheckpoint` or `SWA` callback.
                        For example, if checkpoint_dir is 'ckpt' and model_name is 'model', the
                        weights of ner model saved by `ModelCheckpoint` callback will be
                        'ckpt/model.hdf5' and by `SWA` callback will be 'ckpt/model_swa.hdf5'

        Returns: a list of `keras.callbacks.Callback` instances

        """
        assert not isinstance(callback_list, str)
        callback_list = callback_list or []
        callbacks = []
        if valid_data is not None and valid_labels is not None:
            callbacks.append(TextClassificationMetric(self.preprocessor, valid_data, valid_labels))
            add_metric = True
        else:
            add_metric = False

        if 'modelcheckpoint' in callback_list:
            if not add_metric:
                logging.warning('Using `ModelCheckpoint` with validation data not provided is not '
                                'Recommended! We will use `loss` (of training data) as monitor.')

            assert checkpoint_dir is not None, \
                '`checkpoint_dir` must must be provided when using "ModelCheckpoint" callback'
            assert model_name is not None, \
                '`model_name` must must be provided when using "ModelCheckpoint" callback'
            callbacks.append(tf.keras.callbacks.ModelCheckpoint(
                filepath=os.path.join(checkpoint_dir, f'{model_name}.hdf5'),
                monitor='val_f1' if add_metric else 'loss',
                save_best_only=True,
                save_weights_only=True,
                mode='max' if add_metric else 'min',
                verbose=1))
            logging.info('ModelCheckpoint Callback added')

        if 'earlystopping' in callback_list:
            if not add_metric:
                logging.warning(
                    'Using `ModelCheckpoint` without validation data provided is not Recommended! '
                    'We will use `loss` (of training data) as monitor.')
            callbacks.append(tf.keras.callbacks.EarlyStopping(
                monitor='val_f1' if add_metric else 'loss',
                mode='max' if add_metric else 'min',
                patience=5,
                verbose=1))
            logging.info('Earlystopping Callback added')

        if 'swa' in callback_list:
            assert checkpoint_dir is not None, \
                '`checkpoint_dir` must must be provided when using "SWA" callback'
            assert model_name is not None, \
                '`model_name` must must be provided when using "SWA" callback'
            assert swa_model is not None, \
                '`swa_model` must must be provided when using "SWA" callback'
            callbacks.append(SWA(swa_model=swa_model, checkpoint_dir=checkpoint_dir,
                                 model_name=model_name, swa_start=5))
            logging.info('SWA Callback added')

        return callbacks

    def load_model_weights(self, weights_file):
        self.model.load_weights(weights_file)

    def evaluate(self, data, labels):
        """Evaluate the performance of text classification model.

        Args:
            data: list of tokenized texts (, like ``[['我', '是', '中', '国', '人']]``
            labels: list of str, the corresponding label strings

        """
        features, y = self.preprocessor.prepare_input(data, labels)
        pred_probs = self.model.predict(features)

        y_pred = self.preprocessor.label_decode(pred_probs)

        r = recall_score(labels, y_pred, average='macro')
        p = precision_score(labels, y_pred, average='macro')
        f1 = f1_score(labels, y_pred, average='macro')

        logging.info('Recall: {}, Precision: {}, F1: {}'.format(r, p, f1))
        logging.info(classification_report(labels, y_pred))
        return f1
