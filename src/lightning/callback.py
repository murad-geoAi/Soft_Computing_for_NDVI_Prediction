from pytorch_lightning.callbacks import (
    ModelCheckpoint,
    EarlyStopping,
    LearningRateMonitor,
)
from config import CHECKPOINT_DIR


def get_callbacks():
    checkpoint_callback = ModelCheckpoint(
        dirpath=CHECKPOINT_DIR,
        filename="best-checkpoint",
        monitor="val_mse",
        mode="min",
    )

    early_stopping_callback = EarlyStopping(
        monitor="val_mse",
        patience=10,
        verbose=True,
        mode="min",
    )

    lr_monitor = LearningRateMonitor(
        logging_interval="epoch",
    )

    return [checkpoint_callback, early_stopping_callback, lr_monitor]
