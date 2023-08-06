# -*- coding: utf-8 -*-

import os

from absl import logging
import tensorflow as tf

'''
Applying ensemble during a single training process
'''


class SWA(tf.keras.callbacks.Callback):
    """This callback implements a stochastic weight averaging (SWA) method with constant lr as
    presented in the paper: "Izmailov et al. Averaging Weights Leads to Wider Optima and Better
    Generalization" (https://arxiv.org/abs/1803.05407)

    Author's implementation: https://github.com/timgaripov/swa
    """
    def __init__(self,
                 swa_model: tf.keras.models.Model,
                 checkpoint_dir: str,
                 model_name: str,
                 swa_start: int = 1) -> None:
        """

        Args:
            swa_model: Instance of `tf.keras.models.Model`. The model that used to store the
                average of the weights once SWA begins
            checkpoint_dir: str. tThe directory where the model will be saved in
            model_name: str. The name of model we're training.
                We use checkpoint_dir and model_name to save swa model's weights after training
                done. For example, if checkpoint_dir is 'ckpt' and model_name is 'model',
                the weights of swa model will be save in 'ckpt/model_swa.hdf5'.
            swa_start: str. The epoch when averaging begins. We generally pre-train the network
                for a certain amount of epochs to start (swa_start > 1), as opposed to starting to
                track the average from the very beginning.
        """
        super(SWA, self).__init__()
        self.checkpoint_dir = checkpoint_dir
        self.model_name = model_name
        self.swa_start = swa_start
        self.swa_model = swa_model

    def on_train_begin(self, logs=None):
        self.epoch = 0
        self.swa_n = 0
        # Note: I found deep copy of a model with customized layer would give errors
        # self.swa_model = copy.deepcopy(self.model)  # make a copy of the model we're training

        # Note: Something wired still happen even though i use keras.models.clone_model method,
        #       so I build swa_model outside this callback and pass it as an argument.
        #       It's not fancy, but the best I can do :)
        # see: https://github.com/keras-team/keras/issues/1765
        # self.swa_model = keras.models.clone_model(self.model)
        self.swa_model.set_weights(self.model.get_weights())

    def on_epoch_end(self, epoch, logs=None):
        if (self.epoch + 1) >= self.swa_start:
            self.update_average_model()
            self.swa_n += 1

        self.epoch += 1

    def update_average_model(self):
        # update running average of parameters
        alpha = 1. / (self.swa_n + 1)
        for layer, swa_layer in zip(self.model.layers, self.swa_model.layers):
            weights = []
            for w1, w2 in zip(swa_layer.get_weights(), layer.get_weights()):
                weights.append((1 - alpha) * w1 + alpha * w2)
            swa_layer.set_weights(weights)

    def on_train_end(self, logs=None):
        logging.info('Logging Info - Saving SWA model checkpoint: %s_swa.hdf5' % self.model_name)
        weights_file = os.path.join(self.checkpoint_dir, '{}_swa.hdf5'.format(self.model_name))
        self.swa_model.save_weights(weights_file)
        logging.info('Logging Info - SWA model Saved')
