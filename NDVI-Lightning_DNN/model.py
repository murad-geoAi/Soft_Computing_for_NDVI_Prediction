import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl
import torchmetrics
from torch.optim import Adam

from config import (
    BATCH_SIZE,
    MAX_EPOCHS,
    LEARNING_RATE,
    NUM_WORKERS,
    INPUT_FEATURES,
    TARGET_FEATURE,
)


class MLPRegressor(pl.LightningModule):
    def __init__(self, input_dim:int=len(INPUT_FEATURES), lr:float=LEARNING_RATE):
        super().__init__()
        self.save_hyperparameters()
        self.lr =lr

        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.BatchNorm1d(128),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
        )

        self.criterion = nn.MSELoss()

        #Metrics
        self.train_mse = torchmetrics.MeanSquaredError()
        self.val_mse = torchmetrics.MeanSquaredError()
        self.train_mae = torchmetrics.MeanAbsoluteError()
        self.val_mae = torchmetrics.MeanAbsoluteError()
    
    def forward(self, x):
        return self.net(x).squeeze(1)

    def training_step(self, batch, batch_idx):
        return self.step(batch,batch_idx,prefix="train")


    def on_train_epoch_end(self):
        self.log("train_mse", self.train_mse.compute(), on_epoch=True, on_step=False)
        self.log("train_mae", self.train_mae.compute(), on_epoch=True, on_step=False)
        self.train_mse.reset()
        self.train_mae.reset()


    def on_validation_epoch_end(self):
        self.log("val_mse", self.val_mse.compute(), on_epoch=True, on_step=False)
        self.log("val_mae", self.val_mae.compute(), on_epoch=True, on_step=False)
        self.val_mse.reset()
        self.val_mae.reset()


    def configure_optimizers(self):
        return Adam(self.parameters(), lr=self.lr)
        opt = Adam(self.parameters(), lr=self.lr)
        
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            opt, mode="min", factor=0.2, patience=2, verbose=True
        )
        return [opt], [scheduler]



    

        

   def      