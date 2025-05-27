# Installation

1. Clone this repository: `git clone https://github.com/OleBialas/Intro-to-Neural-Spike-Analysis-in-Python.git`
2. Move to the cloned repository: `cd Intro-to-Neural-Spike-Analysis-in-Python`
3. Use the [pixi package manager](https://pixi.sh/latest/) to install the environment `pixi install`

# Render Notebooks

To render the notebooks from the quarto-markdown documents run 
`pixi run -e render quarto render --profile assign`
To render the notebooks **wihout** solutions or
`pixi run -e render quarto render --profile solution`
To render the notebooks **with** solutions or

Notebooks with and without solution can be dound in the folders `assign` and `solution`.

# Data

The notebooks require the user to download various data sets. These are hosted on sciebo and can be downloaded by executing the respective scripts in the beginning of every notebook.