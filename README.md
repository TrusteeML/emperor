# AI/ML and Network Security: <br>The Emperor has no Clothes

Reproducibility artifacts for the paper AI/ML and Network Security: The Emperor has no Clothes.

## Overview

Each of the use cases and related work presented in this repository has its own set of dependecies, described inside each associated [Poetry](https://python-poetry.org/docs/pyproject/) environment.

However, all the use cases presented depend on the implementation of our ***Trustee*** framework and Trust Report, which was implemented in a separated Python library, we called `trustee`,  to facilitate using it in other projects.

The `trustee` library can be found [here](https://github.com/asjacobs92/trustee)

## Folder structure

| Folder          | Description                                                              |
| --------------- | ------------------------------------------------------------------------ |
| `use_cases/`    | Reproducible artifacts for each of the use cases presented in the paper. |
| `related_work/` | Reproducible artifacts for the related work we compared our work with.   |



## Citing us

```
@inproceedings{Jacobs2022,
	title        = {AI/ML and Network Security: The Emperor has no Clothes},
	author       = {A. S. Jacobs and R. Beltiukov and W. Willinger and R. A. Ferreira and A. Gupta and L. Z. Granville},
	year         = 2022,
	booktitle    = {Proceedings of the 2022 ACM SIGSAC Conference on Computer and Communications Security},
	location     = {Los Angeles, CA, USA},
	publisher    = {Association for Computing Machinery},
	address      = {New York, NY, USA},
	series       = {CCS '21}
}
```