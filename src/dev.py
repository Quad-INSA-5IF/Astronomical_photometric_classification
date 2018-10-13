import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.utils.data import Dataset


class StarDataset(Dataset):
    def __init__(self):
        data = np.genfromtxt('dataset/output_limit_v2.csv', delimiter=',')
        self._len = data.shape[0]
        self._labels = data[:, 0]
        features = data[:, 1:]
        reshape_features = features.reshape((self._len, 1, 8, -1))
        self._features = reshape_features

    def __len__(self):
        return self._len

    def __getitem__(self, idx):
        return torch.from_numpy(np.array(self._features[idx])), torch.from_numpy(np.array(self._labels[idx])).long()

    def one_hot_encoding(self, x, num_classes):
        return np.squeeze(np.eye(num_classes)[x.reshape(-1)])


def log_scale(data):
    return np.piecewise(
        data,
        [data < 0, data == 0, data > 0],
        [lambda x: -log_base(-x, 1.05),
         lambda x: x,
         lambda x: log_base(x, 1.05)
         ]
    )


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 1, kernel_size=(1, 60), stride=(1, 1))
        self.pool = nn.MaxPool2d((1, 6), stride=(1, 6))
        self.dense_layer = nn.Linear(1376, 173)
        self.output = nn.Linear(173, 14)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool(x)
        x = x.view(-1, 1376)
        x = F.relu(self.dense_layer(x))
        x = self.output(x)
        return x


def log_base(np_array, base):
    return np.log(np_array) / np.log(base)


def score(model, test_loader):
    class_correct = list(0. for i in range(14))
    class_total = list(0. for i in range(14))

    with torch.no_grad():
        for data in test_loader:
            features, labels = data
            outputs = model(features)
            _, predicted = torch.max(outputs, 1)
            c = (predicted == labels).squeeze()
            for i in range(labels.shape[0]):
                label = labels[i]
                class_correct[label] += c[i].item()
                class_total[label] += 1

    for i in range(14):
        print('Accuracy of %5s : %2d %%' % (
            i, 100 * class_correct[i] / class_total[i]))


if __name__ == '__main__':
    torch.set_default_tensor_type('torch.DoubleTensor')
    BATCH_SIZE = 32
    EPOCHS = 60
    dataset = StarDataset()

    train_size = int(0.8 * 1.0 * len(dataset))
    validation_size = int(0.0 * 0.2 * len(dataset))
    test_size = len(dataset) - (train_size + validation_size)
    train_dataset, validation_dataset, test_dataset = torch.utils.data.random_split(dataset,
                                                                                    [train_size, validation_size,
                                                                                     test_size])

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE)
    validation_loader = DataLoader(validation_dataset, batch_size=BATCH_SIZE)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE)

    net = Net()

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.01, momentum=0.9)

    for epoch in range(EPOCHS):
        running_loss = 0.0
        for i, data in enumerate(train_loader, 0):
            inputs, labels = data

            optimizer.zero_grad()

            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            if i == 1:
                print('[Epoch %d] loss: %.3f' %
                      (epoch + 1, running_loss / 13))
                running_loss = 0.0
                score(net, test_loader)

    print('Finished training')
