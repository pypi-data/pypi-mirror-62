# Torch Learning Rate Finder

This package can be used to find optimal learning rate.

The package includes `LearningRateFinder` class which implements the `fit`, `find_optimal_lr method` . The `fit` method is used to find optimal learning rate within a range (optional) 
## Installation
To install with pip run the following command

    pip install tanjid-lr-finder

## Dependencies
This package requires the following to be installed:

* Python 3.6 or higher
* Pytorch
* Numpy
* Pandas
* Matplotlib

## Instruction for usage

`LearningRateFinder` takes instantiated pytorch model (`nn.module`), criterion and optimizer (`torch.optim`).

The `fit` method requires a dataloader (`torch.utils.data.DataLoader`), you can optionally include the number of steps, the starting and ending learning rate. The `plot` function can be used to visualize the results in a plot. Please follow the example below for reference.

    lrf = LearningRateFinder(model, criterion, optimizer)
    lrf.fit(train_loader)
    lrf.plot()

## Example
![plot example](example.png)