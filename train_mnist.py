import pandas as pd
import numpy as np
import torch
import torch.distributed as dist
from torch.distributed.optim import DistributedOptimizer
from torch import nn, optim
from torch.nn.parallel import DistributedDataParallel
from torch.utils.data import DataLoader, Dataset
from torch.utils.data.distributed import DistributedSampler
from torchvision.datasets import MNIST
from torchvision import transforms

from tqdm import tqdm

from time import perf_counter


class VolModel(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.num_classes = num_classes

        self.conv1 = nn.Conv2d(1, 4, 3)
        self.activation = nn.ReLU()
        self.conv2 = nn.Conv2d(4, 10, 3)
        self.pool = nn.AdaptiveMaxPool2d((1, 1))
        self.classifier = nn.Linear(10, num_classes)

    def forward(self, x):
        x = self.conv1(x)
        x = self.activation(x)
        x = self.conv2(x)
        x = self.activation(x)
        x = self.pool(x)
        x = x.squeeze(-1).squeeze(-1)
        x = self.classifier(x)
        return x

class VolData(Dataset):
    """
    Load images from directory.

    Example directory listing:
    ./images/0.png
    ./images/1.png
    ...
    """
    def __init__(self, image_dir='./images'):
        super().__init__()
        self.image_dir = image_dir
        # list directory to find how many images we have
        self.filenames = sorted(os.listdir(self.image_dir))

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, ix):
        fn = self.filenames[ix]
        im = PIL.load('{self.image_dir}/{fn}')
        return im
        

def train(num_epochs=30, batch_size=128, learning_rate=0.05):
    # set up an MNIST dataset
    train_dataset = MNIST(root='.', train=True, transform=transforms.Compose([
        transforms.ToTensor(),
        ]),
    download=True)
    test_dataset = MNIST(root='.', train=False, download=True)

    #print(train_dataset[0])
    #return

    # set up dataloader
    sampler = DistributedSampler(train_dataset)
    train_dataloader = DataLoader(train_dataset, batch_size=batch_size,
        sampler=sampler)

    # instantiate a model from our class
    model = VolModel(num_classes=10)

    model = DistributedDataParallel(model)

    rank = dist.get_rank()
    world_size = dist.get_world_size()

    # set up optimizer
    learning_rate *= world_size
    optimizer = optim.SGD(model.parameters(), lr=learning_rate)

    # set up a loss criterion
    criterion = nn.CrossEntropyLoss()

    # loop for some epochs
    iter_losses = []
    #eps = []
    epoch_losses = []
    epoch_accs = []
    elapsed_times = []
    epbar = range(num_epochs)
    #epbar = tqdm(epbar)

    start = perf_counter()
    for ep in epbar:
        ep_loss = 0.0
        num_iters = 0
        corr = 0
        total = 0
        #y_true = []
        #y_pred = []

        for X, Y in train_dataloader:
            # zero the gradients  (resets the optimizer)
            optimizer.zero_grad()
            
            # evaluate model on the minibatch to get predictions
            pred = model(X)

            # compare predictions  to labels to get loss 
            loss = criterion(pred, Y)

            # record the loss
            iter_losses.append(loss.item())
            ep_loss += loss.item()

            # compute gradient by backpropagation from loss
            loss.backward()

            # step the optimizer
            optimizer.step()

            num_iters += 1

            # record correct number of classifications and total samples 
            y_pred = torch.argmax(pred, dim=1)
            
            corr += (Y == y_pred).sum().item()
            total += Y.size(0)


        ep_loss /= num_iters
        #y_pred = np.asarray(y_pred)
        # compute accuracy per epoch
        #y_pred = np.argmax(y_pred, axis=1)
        ep_acc = corr / float(total)

        if rank == 0:
            #epbar.set_postfix(loss=ep_loss)
            print("epoch",ep,"iter",num_iters, "loss",ep_loss, "accuracy",ep_acc,"elapsed time (s)" ,perf_counter() - start)
        
        #eps.append(ep)
            epoch_losses.append(ep_loss)
            epoch_accs.append(ep_acc)
            elapsed_times.append(perf_counter()  - start)
        
            metrics = pd.DataFrame({'epoch_losses': epoch_losses, 'epoch_accs': epoch_accs,'elapsed_time': elapsed_times})
            metrics.to_csv(f'metrics{world_size}.csv')

    return iter_losses, epoch_losses

if __name__ ==  '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    import mpi4py.MPI as MPI

    rank = MPI.COMM_WORLD.Get_rank()
    world_size = MPI.COMM_WORLD.Get_size()

    if rank == 0:
        print("World size:", world_size)

    dist.init_process_group('gloo',
        init_method='env://',
        world_size=world_size,
        rank=rank,
    )

    train()
