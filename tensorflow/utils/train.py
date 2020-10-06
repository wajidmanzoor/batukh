import tensorflow as tf
import time
from tqdm import tqdm
import numpy as np


class Train():
    def __init__(self, model, criterion=None, weights=None, optimizer=None, checkpoint_path=None, max_to_keep=5, is_ocr=False):

        self.is_ocr = is_ocr
        self.model = model
        if optimizer == None:
            optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
        self.optimizer = optimizer
        self.val_logits = []
        if criterion == None:
            if self.is_ocr:
                criterion = tf.nn.ctc_loss
            criterion = tf.nn.softmax_cross_entropy_with_logits
        self.criterion = criterion
        if weights == None:
            weights = [1]*self.model.n_classes
        self.weights = weights

        localtime = time.asctime()
        if checkpoint_path == None:
            checkpoint_path = "tf_ckpts/{}".format(localtime)
        self.checkpoint = tf.train.Checkpoint(
            model=self.model, optimizer=self.optimizer)

        self.manager = tf.train.CheckpointManager(
            self.checkpoint,
            directory=checkpoint_path,
            max_to_keep=5)

        self.train_summary_writer = tf.summary.create_file_writer(
            f"logs/{localtime}/train")
        self.val_summary_writer = tf.summary.create_file_writer(
            f"logs/{localtime}/val")
        self.train_loss = tf.keras.metrics.Mean(name="loss", dtype=tf.float32)
        self.val_loss = tf.keras.metrics.Mean(name="loss", dtype=tf.float32)

    def train_one_step(self, x, y):
        with tf.GradientTape() as tape:
            logits = self.model(x, training=True)
            if self.is_ocr:
                logit_length = tf.fill(
                    [tf.shape(logits)[0]], tf.shape(logits)[1])
                loss = tf.nn.ctc_loss(labels=y, logits=logits, label_length=None,
                                      logit_length=logit_length, logits_time_major=False, blank_index=0)
                loss = tf.reduce_mean(loss)
            else:
                loss = self.criterion(y, logits)
                loss, _ = tf.nn.weighted_moments(
                    loss, (1, 2), np.sum(y*self.weights, axis=3))
                loss = loss[0]

        grads = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(
            zip(grads, self.model.trainable_variables))
        return loss

    def _train(self, ds, epoch, batch_size=64, repeat=1):
        pbar = tqdm(total=len(ds))
        pbar.set_description(f"Epoch: {epoch}. Traininig")

        for (x, y) in enumerate(ds(batch_size=64, repeat=1)):
            loss = self.train_one_step(x, y)
            self.train_loss.update_state(loss)
            pbar.update(1)
            pbar.set_postfix(loss=float(self.train_loss.result()))
        pbar.close()

    def train(self, train_ds, val_ds=None, epochs=10, batch_size=64, repeat=1, save_checkpoints=True, checkpoint_freq=5, save_logits=False):
        self.checkpoint.restore(self.manager.latest_checkpoint)
        if self.manager.latest_checkpoint:
            print("Restored from {}".format(self.manager.latest_checkpoint))
        else:
            print("Initializing from scratch")

        for epoch in range(1, epochs + 1):

            with self.train_summary_writer.as_default():
                self._train(train_ds, epoch)
            if epoch % checkpoint_freq == 0:
                checkpoint_path = self.manager.save(self.optimizer.iterations)
                print("Model saved to {}".format(checkpoint_path))
            if val_ds is not None:
                with self.val_summary_writer.as_default():
                    self._val(val_ds, epoch, save_logits)
        self.train_loss.reset_states()
        self.val_loss.reset_states()

    def val_one_step(self, x, y):
        logits = self.model(x, training=False)
        loss = self.criterion(y, logits)
        loss, _ = tf.nn.weighted_moments(
            loss, (1, 2), np.sum(y*self.weights, axis=3))

        return loss[0], logits

    def _val(self, ds, epoch, save_logits=False):
        pbar = tqdm(total=len(ds))
        pbar.set_description(f"Epoch: {epoch}. validation")
        for (x, y) in enumerate(ds()):
            loss, logits = self.val_one_step(x, y)
            self.val_loss.update_state(loss)
            if save_logits:
                self.val_logits.append(logits)
            pbar.update(1)
            pbar.set_postfix(loss=float(self.val_loss.result()))
        pbar.close()

    def predict(self, x):
        logits = self.model(x, training=False)
        return logits
