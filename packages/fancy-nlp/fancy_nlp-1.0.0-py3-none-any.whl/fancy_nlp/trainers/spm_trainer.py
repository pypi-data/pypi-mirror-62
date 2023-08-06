# -*- coding: utf-8 -*-

import os
from typing import Tuple, List, Union, Optional

from absl import logging
import numpy as np
import tensorflow as tf
from sklearn import metrics

from fancy_nlp.utils import SPMGenerator
from fancy_nlp.callbacks import SPMMetric
from fancy_nlp.callbacks import SWA
from fancy_nlp.preprocessors import SPMPreprocessor


class SPMTrainer(object):
    def __init__(self,
                 model: tf.keras.models.Model,
                 preprocessor: SPMPreprocessor) -> None:
        """

        Args:
            model: instance of keras Model
            preprocessor: instance of SPMPreporcessor
        """
        self.model = model
        self.preprocessor = preprocessor

    def train(self,
              train_data: Tuple[List[str], List[str]],
              train_labels: List[str],
              valid_data: Optional[Tuple[List[str], List[str]]] = None,
              valid_labels: Optional[List[str]] = None,
              batch_size: int = 32,
              epochs: int = 50,
              callback_list: Optional[List[str]] = None,
              checkpoint_dir: Optional[str] = None,
              model_name: Optional[str] = None,
              swa_model: Optional[tf.keras.models.Model] = None,
              load_swa_model: bool = False) -> None:
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

    def train_generator(self,
                        train_data: Tuple[List[str], List[str]],
                        train_labels: List[str],
                        valid_data: Optional[Tuple[List[str], List[str]]] = None,
                        valid_labels: Optional[List[str]] = None,
                        batch_size: int = 32,
                        epochs: int = 50,
                        callback_list: Optional[List[str]] = None,
                        checkpoint_dir: Optional[str] = None,
                        model_name: Optional[str] = None,
                        swa_model: Optional[tf.keras.models.Model] = None,
                        load_swa_model: bool = False) -> None:
        callbacks = self.prepare_callback(callback_list, valid_data, valid_labels, checkpoint_dir,
                                          model_name, swa_model)

        train_generator = SPMGenerator(self.preprocessor, train_data, train_labels, batch_size)

        if valid_data and valid_labels:
            valid_generator = SPMGenerator(self.preprocessor, valid_data, valid_labels,
                                           batch_size)
        else:
            valid_generator = None

        print('Training start...')
        # Note: Model.fit now supports generators
        self.model.fit(x=train_generator,
                       epochs=epochs,
                       callbacks=callbacks,
                       validation_data=valid_generator)
        print('Training end...')

        if load_swa_model and callback_list is not None and 'swa' in callback_list:
            logging.info('Loading swa model after using SWA callback')
            self.load_model_weights(os.path.join(checkpoint_dir, f'{model_name}_swa.hdf5'))

        elif callback_list is not None and 'modelcheckpoint' in callback_list:
            logging.info('Loading best model after using ModelCheckpoint callback...')
            self.load_model_weights(os.path.join(checkpoint_dir, f'{model_name}.hdf5'))

    def prepare_callback(self,
                         callback_list: List[str],
                         valid_data: Optional[Tuple[List[str], List[str]]] = None,
                         valid_labels: Optional[List[str]] = None,
                         checkpoint_dir: Optional[str] = None,
                         model_name: Optional[str] = None,
                         swa_model: Optional[tf.keras.models.Model] = None) -> \
        Optional[List[tf.keras.callbacks.Callback]]:
        """

        Args:
            callback_list: list of str, each item indicate the callback to apply during training.
                       For example, 'earlystopping' means using 'EarlyStopping' callback.
            valid_data: list of tokenized (in char level) texts for evaluation
            valid_labels: labels string of valid data
            checkpoint_dir: str, directory to save spm model, must be provided when using
                            `ModelCheckpoint` or `SWA` callback.
            model_name: str, prefix of spm model's weights file must be provided when using
                        `ModelCheckpoint` or `SWA` callback.
                        For example, if checkpoint_dir is 'ckpt' and model_name is 'model', the
                        weights of spm model saved by `ModelCheckpoint` callback will be
                        'ckpt/model.hdf5' and by `SWA` callback will be 'ckpt/model_swa.hdf5'

        Returns: a list of `keras.callbacks.Callback` instances

        """
        assert not isinstance(callback_list, str)
        callback_list = callback_list or []
        callbacks = []
        if valid_data is not None and valid_labels is not None:
            callbacks.append(SPMMetric(self.preprocessor, valid_data, valid_labels))
            add_metric = True
        else:
            add_metric = False

        if 'modelcheckpoint' in callback_list:
            if not add_metric:
                logging.warning(
                    'Using `ModelCheckpoint` without validation data provided is not Recommended! '
                    'We will use `loss` (of training data) as monitor.')

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
                logging.warning('Using `Earlystopping` with validation data not provided is not '
                                'Recommended! We will use `loss` (of training data) as monitor.')
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

    def load_model_weights(self, weights_file: str) -> None:
        self.model.load_weights(weights_file)

    def evaluate(self, data: Tuple[List[str], List[str]], labels: List[str]) -> float:
        """Evaluate the performance of spm model.

        Args:
            data: list of text pairs, like ``[['我是中国人', ...], ['我爱中国', ...]]``
            labels: list of str, the corresponding label strings

        """
        features, y = self.preprocessor.prepare_input(data, labels)
        pred_probs = self.model.predict(features)

        y_pred = np.argmax(pred_probs, axis=-1)
        labels = np.argmax(y, axis=-1)

        r = metrics.recall_score(labels, y_pred, average='macro')
        p = metrics.precision_score(labels, y_pred, average='macro')
        f1 = metrics.f1_score(labels, y_pred, average='macro')

        logging.info('Recall: {}, Precision: {}, F1: {}'.format(r, p, f1))
        logging.info(metrics.classification_report(labels, y_pred))
        return f1
