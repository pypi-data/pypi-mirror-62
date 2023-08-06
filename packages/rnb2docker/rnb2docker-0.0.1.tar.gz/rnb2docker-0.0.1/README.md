# rnb2docker
Library for turning R Jupyter Notebooks into Docker images.

Specifically, notebooks that use the [IRKernel](https://irkernel.github.io) ([installation](https://irkernel.github.io/installation/)).

## Installation (Linux)

* Create a virtual environment:

  ```commandline
  virtualenv -p /usr/bin/python3.7 venv
  ```

* From source:

  ```commandline
  git clone https://github.com/fracpete/rnb2docker.git
  cd rnb2docker
  ../venv/bin/pip install setup.py
  ```
* From PyPI

  ```commandline
  ./venv/bin/pip install rnb2docker
  ```

## Coding conventions

Required libraries should all be installed within the notebook itself, e.g.:

```
install.packages('PKGNAME')
```

When generating the Docker image, these packages will get installed and commented
out in the R script itself.


## Example

For this example we use the [r_filter_pipeline.ipynb](jupyter/r_filter_pipeline.ipynb)
notebook and the additional [r_filter_pipeline.dockerfile](jupyter/r_filter_pipeline.dockerfile)
Docker instructions. This notebook contains a simple Pands filter setup, using
a simple query to remove certain rows from the input CSV file and saving the cleaned 
dataset as a new CSV file.

The command-lines for this example assume this directory structure:

```
/some/where
|
+- venv   // virtual environment with rnb2docker installed
|
+- data
|  |
|  +- notebooks
|  |  |
|  |  +- r_filter_pipeline.ipynb       // actual notebook
|  |  |
|  |  +- r_filter_pipeline.dockerfile  // additional Dockerfile instructions
|  |
|  +- in
|  |  |
|  |  +- bolts.csv   // raw dataset to filter
|  |
|  +- out
|
+- output
|  |
|  +- rcsvcleaner  // will contain all the generated data, including "Dockerfile"
```

For our `Dockerfile`, we use the `r-base:latest` base image (`-b`), which
contains a base R installation on top of a [Debian "testing"](https://www.debian.org/releases/testing/)
image. The `r_filter_pipeline.ipynb` notebook (`-i`) then gets turned into Python code
using the following command-line:

```commandline
./venv/bin/rnb2docker \
  -i /some/where/data/notebooks/r_filter_pipeline.ipynb \ 
  -o /some/where/output/rcsvcleaner \
  -b r-base:latest \
  -I /some/where/data/notebooks/r_filter_pipeline.dockerfile  
```

Now we build the docker image called `rcsvcleaner` from the `Dockerfile`
that has been generated in the output directory `/some/where/output/rcsvcleaner` 
(`-o` option in previous command-line):

```
cd /some/where/output/rcsvcleaner
sudo docker build -t rcsvcleaner .
```

With the image built, we can now push the raw CSV file through for cleaning.
For this to work, we map the in/out directories from our directory structure
into the Docker container (using the `-v` option) and we supply the input
and output files via the `INPUT` and `OUTPUT` environment variables (using 
the `-e` option). In order to see a few more messages, we also turn on the
debugging output that is part of the notebook, using the `VERBOSE` environment
variable:

```
sudo docker run -ti \
  -v /some/where/data/in:/data/in \
  -v /some/where/data/out:/data/out \
  -e INPUT=/data/in/bolts.csv \
  -e OUTPUT=/data/out/bolts-clean.csv \
  -e VERBOSE=true \
  rcsvcleaner
```

From the debugging messages you can see that the initial dataset with 40 rows
of data gets reduced to 24 rows.

**Disclaimer:** This is just a simple notebook tailored to the UCI dataset
*bolts.csv*.
