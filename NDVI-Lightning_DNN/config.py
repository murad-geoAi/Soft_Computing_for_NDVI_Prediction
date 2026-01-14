from pathlib import Path

# Data
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_PATH = DATA_DIR / "NDVI Prediction.csv"

# Training
BATCH_SIZE = 128
MAX_EPOCHS = 100
LEARNING_RATE = 1e-3
NUM_WORKERS = 0
TRAIN_VALIDATION_SPLIT = 0.2

# Features and Target
INPUT_FEATURES = ["precip", "lst", "eto"]
TARGET_FEATURE = "ndvi"

# Logging
CHECKPOINT_DIR = PROJECT_ROOT / "checkpoints"
LOG_DIR = PROJECT_ROOT / "logs"

# Training Settings
ACCELERATOR = "auto"
DEVICES = 1
PRECISION = 32

# Repro
SEED = 42

# Small helper to make directories
for p in [CHECKPOINT_DIR, LOG_DIR]:
    p.mkdir(parents=True, exist_ok=True)



