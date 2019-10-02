# q2stats-workshops

This repository is designed as a resource for microbial ecologist for a focus on statistical methodologies available in qiime2.

Much of the structure of this repository is inspired by [An-Introduction-To-Applied-Bioinformatics](https://github.com/applied-bioinformatics/An-Introduction-To-Applied-Bioinformatics).

# Installation

These analyses are designed to be read and interactively run.  To run these notebooks, click on the red Binder link above and navigate to the lessons tab.
These notebooks can also be downloaded and run locally.  To do that run the following commands

```
git clone https://github.com/mortonjt/q2stats-workshops.git
cd
conda env create -n workshop-env -f environment.yml
source activate workshop-env
```

The notebooks then can be run via

```
ipymd --from markdown --to notebook lessons/*.md
jupyter notebook
```

# FAQs
## What is the purpose of these notes?
These notes are designed to serve as a platform to better understand underlying statistical concepts. Here, we will discuss some of the caveats behind beta-diversity, differential abundance in addition to some emerging ideas on how to perform multiomics analyses (with an emphasis on microbe-metabolite interactions).

## What are the prerequisites?
These notes already assume that you have some background knowledge in qiime2.
This includes understanding
 - How to install qiime2 and run commands in the commandline
 - How microbial features are determined - either through closed reference OTU-picking or denoising techniques such as DADA2 and Deblur.
 - Some background in alpha and beta-diversity analyses
 - Taxonomy assignment
 - qiime2 basics, importing Artifacts, viewing visualizations via qiime2 view.

