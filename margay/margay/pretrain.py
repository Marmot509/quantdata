import torch
from torch import nn
from torch.nn import functional as F
# from torch.cuda.amp import autocast
from matplotlib import pyplot as plt
import time
import numpy as np
import pandas as pd

MASTER_CONFIG = {
    'n_layers': 4,
    'n_heads': 8,
    'd_model': 11,
    'context_window': 60,
    
    'epochs': 1000,
    'batch_size': 6400,
    'print_logs': True,
    'log_interval': 100,
}

# Check if GPU is available
if torch.cuda.is_available():  
    device = torch.device("cuda")
    print('Default GPU Device: {}'.format(torch.cuda.get_device_name(0)))
else:
    print("No GPU available, using the CPU instead.")
    device = torch.device("cpu")

# load index_pc_hist.pkl into a dataframe
df = pd.read_pickle('../data/index_pct_hist.pkl')

# drop rows that contains NaN
# pre-rescaling
# std = 0.001031, mean = 0.000004
# post-rescaling
# std = 1.031144, mean = 0.004247
index_scale_factor = 1000
df = df.dropna() * index_scale_factor

# convert the dataframe to a tensor
dataset = torch.from_numpy(df.values).to(device)

print(f'tensor device: {dataset.device}')
print(f'first 2 rows: {dataset[:2,: ]}')
print(f'shape of dataset: {dataset.shape}')
print(f'standard deviation: {dataset.std():.6f}')
print(f'mean: {dataset.mean():.6f}')

def get_batches(data, split, config=MASTER_CONFIG, extraY=0):
    train = data[:int(.8 * len(data))]
    valid = data[int(.8 * len(data)): int(.9 * len(data))]
    test  = data[int(.9 * len(data)):]

    batch_data = train
    if split in ['valid', 'val', 'validation']:
        batch_data = valid
    elif split in ['test', 'testing']:
        batch_data = test
    
    # pick random starting points
    ix = torch.randint(0, batch_data.size(0) - config['context_window']-extraY, (config['batch_size'],))
    x = torch.stack([batch_data[i:i+config['context_window']] for i in ix])
    y = torch.stack([batch_data[i+1:i+config['context_window']+1+extraY] for i in ix])
    return x, y

@torch.inference_mode()
def evaluate_loss(model, config=MASTER_CONFIG, size=10, include_test=False):
    out = {}
    model.eval()
    for split in ["train", "val"] + (["test"] if include_test else []):
        losses = []
        for _ in range(size):
            xb, yb = get_batches(dataset, split, config)
            _, loss = model(xb, yb)
            
            losses.append(loss.item())
        out[split] = np.mean(losses)
    model.train()
    return out

def train(model, optimizer, scheduler=None, config=MASTER_CONFIG):
    losses = []

    tmp_loss = evaluate_loss(model)
    print(f"[BEFORE training]\ntrain loss: {tmp_loss['train']:.3f}\nvalid loss: {tmp_loss['val']:.3f}\n")

    log_start_time = train_start_time = time.time()
    print(f"pre-training started at {time.ctime()}\n")

    total_steps = config['epochs'] * dataset.size(0) // config['batch_size']

    for step in range(total_steps):
        optimizer.zero_grad()
        
        xs, ys = get_batches(dataset, 'train', MASTER_CONFIG)
        logits, loss = model(xs, targets=ys)

        loss.backward()
        optimizer.step()
        
        if scheduler:
            scheduler.step()
        
        if step % config['log_interval'] == 0:
            log_time = time.time() - log_start_time
            x = evaluate_loss(model)
            losses += [x]
            if config['print_logs']:
                print(f"Step {step} | val loss {x['val']:.3f} | Time {log_time:.3f} | ETA in {time.strftime('%H:%M:%S', time.gmtime(log_time * (config['epochs'] - step)/config['log_interval']))}")
            log_start_time = time.time()

            if scheduler:
                print("lr: ", scheduler.get_lr())
    
    print(f"\ntraining finished in {time.strftime('%H:%M:%S', time.gmtime(time.time() - train_start_time))} at {time.ctime()}\n")

    tmp_loss = evaluate_loss(model, size=100, include_test=True)
    print(f"[AFTER training]\ntrain loss: {tmp_loss['train']:.3f}\nval loss: {tmp_loss['val']:.3f}\ntest loss: {tmp_loss['test']:.3f}")

    return pd.DataFrame(losses).plot()