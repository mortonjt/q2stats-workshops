# q2stats-workshops
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mortonjt/q2stats-workshops/de4b87c07f7a64bcd065f039df5d4a00cd9740d6)



This repository is designed as a resource for microbial ecologist for a focus on statistical methodologies available in qiime2.

Much of the structure of this repository is inspired by [An-Introduction-To-Applied-Bioinformatics](https://github.com/applied-bioinformatics/An-Introduction-To-Applied-Bioinformatics).

# How should I run this?
These analyses are designed to be read and interactively run.  To run these notebooks, click on the red Binder link above and navigate to the terminal option under the pulldown on the upper right corner.  The tutorial commands can be directly executed in the terminal.

# Local installation
These notebooks can also be downloaded and run locally.  To do that run the following commands

```
git clone https://github.com/mortonjt/q2stats-workshops.git
cd q2stats-workshops
conda env create -n workshop-env -f environment.yml
source activate workshop-env
```

The notebooks then can be run via

```
pip install ipymd
ipymd --from markdown --to notebook lessons/*.md
jupyter notebook
```

# Lessons
## 1. [Differential abundance](https://github.com/mortonjt/q2stats-workshops/blob/master/lessons/differential-abundance.md)
## 2. [Multiomics](https://github.com/mortonjt/q2stats-workshops/blob/master/lessons/multiomics.md)


# FAQs
## What is the purpose of these notes?
These notes are designed to serve as a platform to better understand underlying statistical concepts. Here, we will discuss some of the caveats behind beta-diversity, differential abundance in addition to some emerging ideas on how to perform multiomics analyses (with an emphasis on microbe-metabolite interactions).

## What are the prerequisites?
These notes already assume that you have some background knowledge in [qiime2](https://qiime2.org/).
This includes understanding
 - How to install qiime2 and run commands in the commandline
 - How microbial features are determined - either through closed reference OTU-picking or denoising techniques such as DADA2 and Deblur.
 - Some background in alpha and beta-diversity analyses
 - Taxonomy assignment
 - qiime2 basics, importing Artifacts, viewing visualizations via qiime2 view.
