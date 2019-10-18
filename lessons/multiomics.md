# Multiomics

## 1. Motivation

Understanding microbial metabolism has been considered the holy grail of microbiology by some.
With the growth of paired microbe-metaboite datasets, there is a chance that we can begin to
obtain hints of these microbe-metabolite interactions.

Similar to the differential abundance discussion, attempting to infer microbe-metabolite co-occurrences is prone to compositional problems.  Both microbiome and metabolite datasets are compositional, in the vast majority of experiments, it is not possible to infer the total microbial population size or the total number of chemicals within the environment of interest.  As a result, it is not possible to infer which metabolite is correlated with which microbe due to the missing total abundance.

The approach that we will explore is to estimate co-occurrence probabilities, namely the probability of observing a metabolite given the microbe has already been observed.  A high level schematic is given below

![](../img/mmvec.png)

The algorithm mmvec (microbe-metabolite vectors) attempts to learn how to factorize the conditional probability matrix. Similar to how ordination is commonly used in microbial ecology, we can try to learn a low dimensional representation of these interactions.  In this tutorial, we will cover how to run mmvec, and more importantly how to interpret the output in order to identify potentially useful interactions.

## 2. Setup

First make sure that you are in the `cystic-fibrosis-tutorial` folder created in the [differential abundance tutorial](https://github.com/mortonjt/q2stats-workshops/blob/master/lessons/differential-abundance.md#2-setup)

Then download the tutorial files through the following commands

Download Feature Table
```
curl -sL https://github.com/mortonjt/q2stats-workshops/blob/master/data/oxygen-cf/lcms_nt.qza?raw=true > lcms_nt.qza
```

Download Metabolite Annotations
```
curl -sL https://raw.githubusercontent.com/mortonjt/q2stats-workshops/master/data/oxygen-cf/metabolite-metadata.txt > metabolite-metadata.txt
```

The metabolite bucket table and metabolite annotations can be found on [GNPS](https://gnps.ucsd.edu/ProteoSAFe/status.jsp?task=34d825dbf4e9466e81d809faf814995b) (Global Natural Products Social NEtworking).

Once the tutorial files are downloaded, we will also want to run differential abundance on the metabolites.  This will become important when interpreting the biplots.

```
qiime songbird multinomial \
	--i-table lcms_nt.qza \
	--m-metadata-file sample-metadata.txt \
	--p-formula "depth + C(Pseudo)" \
	--p-epochs 500 \
	--p-training-column Testing \
	--p-summary-interval 1 \
	--output-dir metabolite_differentials \
	--verbose
```

If you are downloading these artifacts, make sure to first create the following folder before downloading

```
mkdir metabolite_differentials
cd metabolite_differentials
```

#####  Output artifacts:
`differentials.qza` [download](https://www.dropbox.com/s/pmlk3bdczmt6r19/differentials.qza?dl=0)

`regression_stats.qza` [download](https://www.dropbox.com/s/prxj5zgi5otaisx/regression_stats.qza?dl=0)


If you downloading, make sure to return back to the original folder by running `cd -`.

# 3. Running mmvec

Now we are ready to run mmvec.  The command is given below

```
qiime mmvec paired-omics \
	--i-microbes otus_nt.qza \
	--i-metabolites lcms_nt.qza \
	--m-metadata-file sample-metadata.txt \
	--p-summary-interval 1 \
	--p-training-column Testing \
	--output-dir mmvec_results \
	--verbose
```

If you are downloading these artifacts, make sure to first create the following folder before downloading

```
mkdir mmvec_results
cd mmvec_results
```

#####  Output artifacts:
`differentials.qza`  [download](https://www.dropbox.com/s/pxmbbftcg6d6p4v/conditionals.qza?dl=0)

`conditional_biplot.qza` [download](https://www.dropbox.com/s/wzzcrycaijw99tu/conditional_biplot.qza?dl=0)

If you downloading, make sure to return back to the original folder by running `cd -`.

## 4. Visualizing microbe-metabolite interactions

Once this is complete, you should see two different files under the `mmvec_results` folder, `conditional_biplot.qza` and `conditionals.qza`.  `conditional_biplot.qza` contains the factorized conditional probability matrix that can be visualized as an ordination.  This biplot can allow for rapid interpretation of the global microbe-metabolite patterns apparent in this dataset.

We can create an interactive biplot visualization in Emperor with the following command.

```
qiime emperor biplot \
	--i-biplot mmvec_results/conditional_biplot.qza \
	--m-sample-metadata-file metabolite-metadata.txt \
	--m-sample-metadata-file metabolite_differentials/differentials.qza \
	--m-feature-metadata-file taxonomy.tsv \
	--m-feature-metadata-file microbe_differentials/differentials.qza \
	--p-number-of-features 50 \
	--p-ignore-missing-samples \
	--o-visualization emperor.qzv
```

#####  Output artifacts:
`conditionals-viz.qzv` [view](https://view.qiime2.org/visualization/?type=html&src=https%3A%2F%2Fdl.dropbox.com%2Fs%2Fkj0v5wwumqd2vdf%2Femperor.qzv%3Fdl%3D1) | [download](https://www.dropbox.com/s/kj0v5wwumqd2vdf/emperor.qzv?dl=0)

Here points are representing molecules and arrows represent microbes.  The distances between points represents the co-occurrence strength between molecules and distances between arrows represents the co-occurrence strength between microbes. The directionality and strength of the arrows can be used to explain the variance of the metabolite due to specific microbes. The drop down menus can be utilized to color the microbes and metabolites acrossing to their annotations as well as their differentials.  One can also double click on the points or arrows to identify microbes or molecules of interest.

`conditionals.qza` contains the microbe-metabolite conditional probabilities estimated from mmvec.  These conditional probabilities can be viewed with `qiime metadata tabulate` as follows.

```
qiime metadata tabulate \
	--m-input-file mmvec_results/conditionals.qza \
	--o-visualization conditionals-viz.qzv
```

#####  Output artifacts:
`conditionals-viz.qzv` [view](https://view.qiime2.org/visualization/?type=html&src=https%3A%2F%2Fdl.dropbox.com%2Fs%2F1r34krm1n8pekkt%2Fconditionals-viz.qzv%3Fdl%3D1) | [download](https://www.dropbox.com/s/1r34krm1n8pekkt/conditionals-viz.qzv?dl=0)

Note that these are log transformed conditional probabilities (centered around zero).  One can sort the columns to identify metabolites most likely to be present in the presence of a specific microbe.

To further explore these iteractions, paired heatmaps of the microbe and metabolite abundances can be made to show how well the metabolite profiles match the microbe profiles.
We will highlight two microbes, namely Pseudomonas aeroginosa and Streptococcus, whose sequences we will copy from the Emperor clipboard.  The following paired heatmap command can be run

```
qiime mmvec paired-heatmap \
  --i-ranks mmvec_results/conditionals.qza \
  --i-microbes-table otus_nt.qza \
  --i-metabolites-table lcms_nt.qza \
  --m-microbe-metadata-file taxonomy.tsv \
  --m-microbe-metadata-column Taxon \
  --p-features bc23d2ee539bf2f52faf789289af7879 \
  --p-features 29f6e97a2ed3b8abe26bb45acba8451f \
  --p-top-k-microbes 0 \
  --p-normalize rel_row \
  --p-top-k-metabolites 100 \
  --p-level 6 \
  --o-visualization paired-heatmap-top2.qzv
```

#####  Output artifacts:
`paired-heatmap-top2.qzv` [view](https://view.qiime2.org/visualization/?type=html&src=https%3A%2F%2Fdl.dropbox.com%2Fs%2Fy4eijy0tkjcsd85%2Fpaired-heatmap-top2.qzv%3Fdl%3D1) | [download](https://www.dropbox.com/s/y4eijy0tkjcsd85/paired-heatmap-top2.qzv?dl=0)

Here, we are only visualizing the abundances of 2 microbes, but are pulling out the top 100 metabolites associated with these microbes as predicted from the conditional probabilities.

## 5. Considerations

The workflow presented here provides a means to try to explore microbe-metabolite relationships.  However, it is imporant to note the limitations of these tools.  First, this framework does not currently provide a means to test global significance - we cannot currently determine if the detected interactions are real or due to noise.  It is critical to first run beta diversity on individual datasets to first determine if there are strong patterns present in the data before attempting multiomics analyses.  It is also worthwhile to check out other techniques such as Canonical correlation analysis and Partial least squares, since these techniques can provide a measure of global fit between two datasets - the [mixomics](http://mixomics.org/) package is a good place to start.

## 6. References

See [mmvec documentation](https://github.com/biocore/mmvec) for more information.
