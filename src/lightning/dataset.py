# Dataset.py

import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader, random_split
import pytorch_lightning as pl
from sklearn.model_selection import train_test_split

from config import (
    BATCH_SIZE,
    NUM_WORKERS,
    INPUT_FEATURES,
    TARGET_FEATURE,
    DATA_PATH,
    TRAIN_VALIDATION_SPLIT,
    SEED,
)

class NdviDataset(Dataset):
    def __init__(self, features: torch.Tensor, targets: torch.Tensor):
        self.features = features
        self.targets = targets

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx], self.targets[idx]


class NdviDataModule(pl.LightningDataModule):
    def __init__(
        self,
        data_path=DATA_PATH,
        batch_size=BATCH_SIZE,
        num_workers=NUM_WORKERS,
        train_valid_split=TRAIN_VALIDATION_SPLIT,
        seed=SEED,
    ):
        super().__init__()
        self.data_path = data_path
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.train_valid_split = train_valid_split
        self.seed = seed

    def setup(self, stage=None):
        df = pd.read_csv(self.data_path)

        # Drop rows with NaN in features or target
        df = df.dropna(subset=INPUT_FEATURES + [TARGET_FEATURE])

        X = df[INPUT_FEATURES].values.astype("float32")
        y = df[TARGET_FEATURE].values.astype("float32")

        X_train, X_val, y_train, y_val = train_test_split(
            X,
            y,
            test_size=self.train_valid_split,
            random_state=self.seed,
            shuffle=True,
        )

        # Convert to torch tensors
        self.train_dataset = NdviDataset(
            torch.tensor(X_train, dtype=torch.float32),
            torch.tensor(y_train, dtype=torch.float32),
        )
        self.val_dataset = NdviDataset(
            torch.tensor(X_val, dtype=torch.float32),
            torch.tensor(y_val, dtype=torch.float32),
        )

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            shuffle=True,
        )

    def val_dataloader(self):
        return DataLoader(
            self.val_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
        )
