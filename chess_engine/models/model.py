import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    """
    Minimal supervised image classification model. Takes as input a chess board
    represented as 12 * 8 * 8 tensor. Predicts whether white won the game or
    not.
    """

    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=12, out_channels=12, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(in_channels=12, out_channels=12, kernel_size=3, stride=1, padding=1)
        self.fc1 = nn.Linear(in_features=8 * 8 * 12, out_features=400)
        self.fc2 = nn.Linear(in_features=400, out_features=200)
        self.fc3 = nn.Linear(in_features=200, out_features=1)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = torch.sigmoid(x)
        return x


def training_loop(n_epochs, optimizer, model, loss_fn, x_train, x_validate, y_train, y_validate):
    for epoch in range(1, n_epochs + 1):
        y_train_pred = model(x_train)
        loss_train = loss_fn(y_train_pred, y_train)

        y_val_pred = model(x_validate)
        loss_val = loss_fn(y_val_pred, y_validate)

        optimizer.zero_grad()
        loss_train.backward()
        optimizer.step()

        if epoch == 1 or epoch % 10 == 0:
            print(f'Epoch {epoch}, Training loss {loss_train.item():.4f}, '
                  f'Validation loss {loss_val.item():.4f}')


if __name__ == '__main__':
    x = np.load('/Users/brianelinsky/repos/chess-engine/data/features/x.npy')
    y = np.load('/Users/brianelinsky/repos/chess-engine/data/features/y.npy')
    x_tensor = torch.tensor(x, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.float32)
    y_tensor = torch.unsqueeze(y_tensor, 1)  # Add batch dimension

    # Naively split into test and train
    n = len(x_tensor)
    n_train = int(n * 0.90)
    n_test = int(n - n_train)
    x_train, x_test = torch.split(x_tensor, split_size_or_sections=[n_train, n_test])
    y_train, y_test = torch.split(y_tensor, split_size_or_sections=[n_train, n_test])

    # Instantiate the network
    model = Net()

    # Define the loss function
    loss_fn = nn.BCELoss()

    # Define the optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)

    # TODO - Incorporate tensorboard for logging
    # TODO - figure out how to compare the model results to an engine like stockfish
    # TODO - what is a good loss number? How do you interpret it?
    # TODO - add model checkpointing.

    training_loop(n_epochs=1000,
                  optimizer=optimizer,
                  model=model,
                  loss_fn=loss_fn,
                  x_train=x_train,
                  x_validate=x_test,
                  y_train=y_train,
                  y_validate=y_test)
