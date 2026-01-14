# Config.py
form pathlib import Path

#Data
PROJECT_ROOT = Path("./")
DATA_DIR = PROJECT_ROOT / "data"
DATA_PATH = DATA_DIR / "NDVI Prediction.csv"

#Training
BATCH_SIZE = 128
MAX_EPOCHS = 100
LEARNING_RATE = 1e-3
NUM_WORKERS = 0
TRAIN_VALIDATION_SPLIT = 0.2
INPUT_FEATURES = df.iloc[:,2]
TARGET_FEATURE = df.iloc[:,3]

#Logging
CHECKPOINT_DIR = PROJECT_ROOT / "checkpoints"
LOG_DIR = PROJECT_ROOT / "logs"

# Training Settings
ACCELERATOR = "tpu"
DEVICES = 8
PRECISION = 32

# Repro
SEED = 42

# Small helper to make directoris
for p in [PROJECT_ROOT, DATA_DIR, CHECKPOINT_DIR, LOG_DIR]:
    p.mkdir(parents=True,exist_ok=True)



