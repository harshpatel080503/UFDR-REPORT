import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

print("--- DEBUG SCRIPT STARTING ---")
import torch
print("Torch imported")
import torch.utils.data
print("torch.utils.data imported")
from torch.utils.data import BatchSampler, ConcatDataset, SubsetRandomSampler
print("Specific torch classes imported")
