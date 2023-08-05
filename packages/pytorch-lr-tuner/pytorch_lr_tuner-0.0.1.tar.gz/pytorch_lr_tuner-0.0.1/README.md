# PyTorch Learning Rate Tuner

Python package to plot loss against varied learning rate for PyTorch neural network models and finding optimal learning rate for specific optimizer.

### Installation:

    pip install saif-lr-finder

### Dependency:

* Python 3.6
* Numpy
* Pandas
* Matplotlib
* PyTorch

### Example:

The package includes `LearningRateFinder` class which can be instantiated with pytorch model reference, optimizer, criterion and training set. The `fit()` method searches for optimal learning rate with multiplicative increment and smoothing with exponential weighted average and bias correction and the visualization of this log can be obtained through calling `plot()` method. 

    from saif_lr_finder import LearningRateFinder

    ESTIMATOR_CONFIG = {'input_shape': 21, 'output_shape': 1, 'hidden_units': [32, 64, 16]}

    binary_crossentropy = nn.BCELoss()

    lr_finder = LearningRateFinder(estimator=VanillaNet, config=ESTIMATOR_CONFIG, optimizer='sgd', criterion=binary_crossentropy, train_set=train_set, val_set=val_set)

    lr_finder.fit()

    lr_finder.plot()

### Output:

<img src='loss_vs_lr.png'> <br>

Here, the learning rate with steepest gradient in loss can be inferred as an optimal one for this specific architecture.