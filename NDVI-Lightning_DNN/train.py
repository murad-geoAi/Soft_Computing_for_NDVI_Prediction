# train.py

import on
import argparse
import pytorch_lightning as pl
from pytorch_lightning.loggers import TensorBoardLogger

from config import (
    BATCH_SIZE,
    MAX_EPOCHS,
    LEARNING_RATE,
    NUM_WORKERS,
    INPUT_FEATURES,
    TARGET_FEATURE,
    CHECKPOINT_DIR,
    LOG_DIR,
    SEED,
    ACCELERATOR,
    DEVICES,
    PRECISION,
)
from dataset import NdviDataModule
from model import MLPRegressor
from callback import get_callbacks


def main():
    parser = argparse.ArgumentParser(description="NDVI Prediction")
    parser.add_argument(
        "--data_path", type=str, default=DATA_PATH, help="Path to the dataset"
    )
    args = parser.parse_args()

    pl.seed_everything(SEED)

    dm = NdviDataModule(
        data_path=args.data_path,
        batch_size=BATCH_SIZE,
        num_workers=NUM_WORKERS,
        train_valid_split=TRAIN_VALIDATION_SPLIT,
        seed=SEED,
    )
    model = MLPRegressor(input_dim=len(INPUT_FEATURES), lr=LEARNING_RATE)
    callbacks = get_callbacks()
    logger = TensorBoardLogger(LOG_DIR, name="mlp_regressor")

    trainer = pl.Trainer(
        max_epochs=MAX_EPOCHS,
        accelerator=ACCELERATOR,
        devices=DEVICES,
        precision=PRECISION,
        callbacks=callbacks,
        logger=logger,
    )
    trainer.fit(model, dm)
    trainer.save_checkpoint(CHECKPOINT_DIR / "mlp_regressor.ckpt")


if __name__ == "__main__":
    main()
