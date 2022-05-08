Decision Tree Extraction (DTExtract)
=====

> This folder contains code and data from the original author's repository, with minor changes made to update and run the code when necessary.
> https://github.com/obastani/dtextract

<br>

DTExtract is a tool for extracting model explanations in the form of decision trees. More precisely, given

- blackbox access to a model (i.e., for a given input, produce the corresponding output),
- a sampling distribution over the input space,

then DTExtract constructs a decision tree approximating that model.

Table of Contents
=====
0. Prerequisites
1. Setting Up DTExtract
2. Using DTExtract

Prerequisites
=====

DTExtract has been tested using Python 2.7. DTExtract depends on numpy, scipy, scikit-learn, and pandas.

Setting Up DTExtract
=====

Run `setup.sh` to set up the datasets used in the examples that come with DTExtract.

Using DTExtract
=====

See `python/dtextract/examples/iris.py` for an example using a dataset from the UCI machine learning repository with the goal of classifying Iris flowers. The dataset is located at `data/iris.zip` ([download link](https://archive.ics.uci.edu/ml/datasets/Iris)). To run this example, run

    $ cd python
    $ python -m dtextract.examples.iris

Similarly, see `python/dtextract/examples/diabetes.py` for an example using a diabetes readmissions dataset. The dataset is located at `data/dataset_diabetes.zip` ([download link](https://archive.ics.uci.edu/ml/datasets/Diabetes+130-US+hospitals+for+years+1999-2008)). To run this example, run

    $ cd python
    $ python -m dtextract.examples.diabetes

Finally, see `python/dtextract/examples/wine.py` for an example using a dataset from the UCI machine learning repository with the goal of classifying wines. The dataset is located at `data/wine.zip` ([download link](https://archive.ics.uci.edu/ml/datasets/Wine)). To run this example, run

    $ cd python
    $ python -m dtextract.examples.wine
