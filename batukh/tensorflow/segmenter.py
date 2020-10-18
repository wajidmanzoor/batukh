from .utils.models.segmentation_model import SegmentationModel
from .utils.train import Train
from .utils.data.dataloader import SegmentationDataLoader
from .utils.data.augmentation import MultipleColorJitter


# todo:apply augmentation


class PageExtracter(Train):
    r"""This class used to extract pages (removing borders and blank spaces around pages) from originals.

    Example

    .. code-block:: python

        >>> from batukh.tensorflow.segmenter import PageExtraction
        >>> page_extracter = PageExtraction()
        >>> page_extracter.load_data(train_path = "/train_data/")
        >>> page_extracter.train(n_epochs=10,batch_size=1,weights=[1,100])
        Initializing from scratch
        Epoch: 1. Traininig: 100%|██████████| 70/70 [00:02<00:00, 23.95it/s, loss=0.0708]
        Model saved to /tf_ckpts/Fri Oct 16 08:23:13 2020/ckpt-14280
        >>> page_extracter.save_model("/model/")
        Model saved at /saved_models


        """

    def __init__(self):
        super().__init__(model=SegmentationModel(2))
        self.train_dl = None
        self.val_dl = None

    def load_data(self, train_path, val_path=None):
        r"""Loads Train and Validation datset.

        Note:
            Respective images and labels should be of same size with same filename.
            label images should be of black background with  pixels corresponding to page area colored red.

        Args:
            train_path (str)        : path of the folder contaings originals folder (containing original images) and labels folder (containing label images) for train dataset.
            val_path (str,optional) : path of the folder contaings originals folder (containing original images) and labels folder (containing label images) for validation dataset.
            """
        self.train_dl = SegmentationDataLoader(
            train_path, self.model.n_classes)
        if val_path is not None:
            self.val_dl = SegmentationDataLoader(
                val_path, self.model.n_classes)

    def train(self, n_epochs, batch_size=1, repeat=1, criterion=None, class_weights=None, optimizer=None, learning_rate=0.0001, save_checkpoints=True, checkpoint_freq=None, checkpoint_path=None, max_to_keep=5):
        super().train(n_epochs, train_dl=self.train_dl, val_dl=self.val_dl, batch_size=batch_size, repeat=repeat, criterion=criterion, class_weights=class_weights,
                      optimizer=optimizer, learning_rate=learning_rate, save_checkpoints=save_checkpoints, checkpoint_freq=checkpoint_freq, checkpoint_path=checkpoint_path, max_to_keep=max_to_keep)


class ImageExtracter(Train):
    r"""The class used to extract images.

    Example

    .. code-block:: python

        >>> from batukh.tensorflow.segmenter import ImageExtracter
        >>> image_extracter = ImageExtracter()
        >>> image_extracter.load_data( train_path="/train_data/",val_path="/val_data/")
        >>> image_extracter.train(n_epochs=1)
        Initializing from scratch
        Epoch: 1. Traininig: 100%|██████████| 70/70 [00:02<00:00, 23.95it/s, loss=0.0708]
        Epoch: 1. validation: 100%|██████████| 70/70 [00:02<00:00, 23.95it/s, loss=0.0708]
        Model saved to /tf_ckpts/Fri Oct 16 08:23:13 2020/ckpt-14280

        """

    def __init__(self):
        super().__init__(model=SegmentationModel(2))
        self.train_dl = None
        self.val_dl = None

    def load_data(self, train_path, val_path=None):
        r"""Loads Train and Validation datset.

        Note:
            Respective images and labels should be of same size with same filename.
            label images should be of black background with  pixels corresponding image areas colored red.

        Args:
            train_path (str)        : path of the folder contaings originals folder (containing originals images) and labels folder (containing label images) for train dataset.
            val_path (str,optional) : path of the folder contaings originals folder (containing originals images) and labels folder (containing label images) for validation dataset.
            """
        self.train_dl = SegmentationDataLoader(
            train_path, self.model.n_classes)
        if val_path is not None:
            self.val_dl = SegmentationDataLoader(
                val_path, self.model.n_classes)

    def train(self, n_epochs, batch_size=1, repeat=1, criterion=None, class_weights=None, optimizer=None, learning_rate=0.0001, save_checkpoints=True, checkpoint_freq=None, checkpoint_path=None, max_to_keep=5):
        super().train(n_epochs, train_dl=self.train_dl, val_dl=self.val_dl, batch_size=batch_size, repeat=repeat, criterion=criterion, class_weights=class_weights,
                      optimizer=optimizer, learning_rate=learning_rate, save_checkpoints=save_checkpoints, checkpoint_freq=checkpoint_freq, checkpoint_path=checkpoint_path, max_to_keep=max_to_keep)


class LayoutExtracter(Train):
    r"""This class is used to extract diffrent layouts from a image.

<<<<<<< HEAD:batukh/tensorflow/segmenter.py
    def __init__(self, n_layouts):
||||||| 56159e5:KoshurRecognition/tensorflow/segmenter.py
    def __init__(self, train_path, val_path, batch_size, repeat,  n_layouts):
=======
    Example

    .. code-block:: python

        >>> from batukh.tensorflow.segmenter import LayoutExtracter
        >>> layout_extracter = LayoutExtracter(2)
        >>> layout_extracter.load_data(train_path ="/train_data/",val_data="/val_data/")
        >>> layout_extracter.train(n_epochs=1,checkpoint_path="/tf_chkpts/")
        Restored from /tf_chkpts/ckpt-13280
        Epoch: 1. Traininig: 100%|██████████| 70/70 [00:02<00:00, 23.95it/s, loss=0.0708]
        Epoch: 1. validation: 100%|██████████| 70/70 [00:02<00:00, 23.95it/s, loss=0.0708]
        Model saved to /tf_ckpts/Fri Oct 16 08:23:13 2020/ckpt-14280

        """

    def __init__(self, n_layouts):
>>>>>>> wajid:KoshurRecognition/tensorflow/segmenter.py
        super().__init__(model=SegmentationModel(n_layouts))
        self.train_dl = None
        self.val_dl = None

    def load_data(self, train_path, val_path=None):
        r"""Loads Train and Validation datset.

        Note:
            Respective images and labels should bepython of same size with same filename.
            label images should be of black background with  pixels corresponding to diffrent areas colored diffrently.

        Args:
            train_path (str)        : path of the folder contaings originals folder (containing originals images) and labels folder (containing label images) for train dataset.
            val_path (str,optional) : path of the folder contaings originals folder (containing originals images) and labels folder (containing label images) for validation dataset.
            """
        self.train_dl = SegmentationDataLoader(
            train_path, self.model.n_classes)
        if val_path is not None:
            self.val_dl = SegmentationDataLoader(
                val_path, self.model.n_classes)

    def train(self, n_epochs, batch_size=2, repeat=1, criterion=None, class_weights=None, optimizer=None, learning_rate=0.0001, save_checkpoints=True, checkpoint_freq=None, checkpoint_path=None, max_to_keep=5):
        super().train(n_epochs, train_dl=self.train_dl, val_dl=self.val_dl, batch_size=batch_size, repeat=repeat, criterion=criterion, class_weights=class_weights,
                      optimizer=optimizer, learning_rate=learning_rate, save_checkpoints=save_checkpoints, checkpoint_freq=checkpoint_freq, checkpoint_path=checkpoint_path, max_to_keep=max_to_keep)


class BaselineDetecter(Train):
    r"""This class is used to detect baseline.

<<<<<<< HEAD:batukh/tensorflow/segmenter.py
    def __init__(self):
||||||| 56159e5:KoshurRecognition/tensorflow/segmenter.py
    def __init__(self, train_path, val_path, batch_size, repeat):
=======
    Example

    .. code-block:: python

        >>> from batukh.tensorflow.segmenter import BaselineDetecter
        >>> baseline_detecter = BaselineDetecter()
        >>> baseline_detecter.load_data("/train_data/")
        >>> baseline_detecter.train(1,weights=[1:700])
        Initializing from scratch
        Epoch: 1. Traininig: 100%|██████████| 70/70 [00:02<00:00, 23.95it/s, loss=0.0708]
        Model saved to /tf_ckpts/Fri Oct 16 08:23:13 2020/ckpt-14280

        """

    def __init__(self):
>>>>>>> wajid:KoshurRecognition/tensorflow/segmenter.py
        super().__init__(model=SegmentationModel(2))
        self.train_dl = None
        self.val_dl = None

    def load_data(self, train_path, val_path=None):
        r"""Loads Train and Validation datset.

        Note:
            Respective images and labels should be of same size with same filename.
            label images should be of black background with  red lines of about 5px representing baselines.

        Args:
            train_path (str)        : path of the folder contaings originals folder (containing original images) and labels folder (containing label images) for train dataset.
            val_path (str,optional) : path of the folder contaings originals folder (containing original images) and labels folder (containing label images) for validation dataset.
            """
        self.train_dl = SegmentationDataLoader(
            train_path, self.model.n_classest)
        if val_path is not None:
            self.val_dl = SegmentationDataLoader(
                val_path, self.model.n_classes)

    def train(self, n_epochs, batch_size=2, repeat=1, criterion=None, class_weights=None, optimizer=None, learning_rate=0.0001, save_checkpoints=True, checkpoint_freq=None, checkpoint_path=None, max_to_keep=5):
        super().train(n_epochs, train_dl=self.train_dl, val_dl=self.val_dl, batch_size=batch_size, repeat=repeat, criterion=criterion, class_weights=class_weights,
                      optimizer=optimizer, learning_rate=learning_rate, save_checkpoints=save_checkpoints, checkpoint_freq=checkpoint_freq, checkpoint_path=checkpoint_path, max_to_keep=max_to_keep)
