# Differential abundance

## 1. Motivation

Differential abundance is a core technique in every microbiome application.  If a large microbial difference is detected between different environments, the next step is to identify microbes that explain the differences between these environments.  However, this problem can be tricky to answer due to the relative nature of the data that we measured.


The main issue behind differential abundance is compositionality, the mathematical nature of relative measurements.
Consider the example below

![](../img/composition.png)

In the left environment we don't observe the entire environment, but we can count the number of blue and orange microbes.
If there is a major perturbation, and we again count the microbes, there are multiple possibilities that could have explained the difference of proportions between the two environments. One possibility is that the number of blue microbes decreased.  Another possibility is that both the number of blue and orange microbes increased.  The reason behind this confusion is because we are missing information about the total abundance.  More concretely, if we have environment *A = (a<sub>1</sub>, ... a<sub>D</sub>)* with proportions from *D* taxa and the same environment after perturbation *B = (b<sub>1</sub>, ... b<sub>D</sub>)*, then the following holds.

![](../img/rank-equations1.png)

From sequencing we can measure the proportions _p<sub>A</sub>_ and _p<sub>B</sub>_, but in the majority of experiments, the total abundances _N<sub>A</sub>_ and _N<sub>B</sub>_ are inaccessible.  Due to this, the ratio _N<sub>A</sub>_ / _N<sub>B</sub>_ confounds our inference to determine if a microbe has changed or not.

In essence, it is not possible to infer absolute changes from relative data.

But fear not. While we often cannot infer the absolute change, there are a couple of workarounds.  First, we can compute something that looks like a concentration - by picking a reference microbe, we can look at their ratio, effectively negating the need to measure total biomass.

![](../img/rank-equations2.png)


As a result, we can conduct a statistical test to determine if the log ratio of pairs of microbes have been altered across conditions. One of the outcomes of this procedure is, one would have to determine what a reference microbe needs to be.

Another workaround is to infer the relative changes (which we call the differential).  The ordering of the log fold change is consistent between absolute and relative abundances.

![](../img/rank-equations3.png)

Here, the total biomass does not influence the ordering of the log fold change calculation. As a result, the ranking of the log fold change between the proportions is equal to the ranking of the log fold change between the absolute abundances. This is a huge win for differential abundance methodologies, since many methods can already infer the differential.  The major outstanding issue is how to determine which microbes to focus on.  Since the total biomass fluctuation will confound the absolute log fold change estimates, it won't be possible to build a statistical test to determine if a microbe's abundance has changed or not.

More information these concepts can be found in our paper [here](https://www.nature.com/articles/s41467-019-10656-5)


In this tutorial, we will first demonstrate how to run a basic differential abundance analysis using multinomial regression via songbird. Then we will show how to interpret the underlying differentials estimated from songbird.


## 2. Setup
We'll be using the cystic fibrosis data from this [paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6157970/) for demonstration.
First create a new create a new directory and move into it

```
mkdir cystic-fibrosis-tutorial
cd cystic-fibrosis-tutorial
```

Download the tutorial files using the following commands.

Download Feature Table
```
curl -sL https://github.com/mortonjt/q2stats-workshops/blob/master/data/oxygen-cf/otus_nt.qza?raw=true > otus_nt.qza
```

Download Sample metadata
```
curl -sL https://raw.githubusercontent.com/mortonjt/q2stats-workshops/master/data/oxygen-cf/sample-metadata.txt > sample-metadata.txt
```

Download Taxonomy
```
curl -sL https://github.com/mortonjt/q2stats-workshops/blob/master/data/oxygen-cf/taxonomy.tsv?raw=true > taxonomy.tsv
```

The feature table and sample metadata can be found in [Qiita](https://qiita.ucsd.edu/study/description/10863).

## 3. Running Songbird

Once the files are downloaded, we can now run the basic multinomial regression command

```
qiime songbird multinomial \
	--i-table otus_nt.qza \
	--m-metadata-file sample-metadata.txt \
	--p-formula "depth + C(Pseudo)" \
	--p-epochs 500 \
	--p-training-column Testing \
	--p-summary-interval 1 \
	--output-dir microbe_differentials \
	--verbose
```

There are couple of important things to note here.  First, we used `--p-training-column Testing` to specify the hold out samples.
In this case, we excluded samples from one patient to serve as cross validation.  These samples were excluded when fitting the model,
to be used later to evaluate predictive accuracy.  Second, we specified `--p-formula "Depth + C(Pseudo)"` to investigate relationships to
`Depth` and `Pseudo`.  `Pseudo` is a categorical variable, which is why we used `C()` to mark it as categorical.
`Depth` is a continuously valued variable, negating the need to use the `C()` decorator.

The model fit can be summarized with the following command.

```
qiime songbird summarize-single \
	--i-regression-stats microbe_differentials/regression_stats.qza \
	--o-visualization regression_summary.qzv
```

The `regression-summary.qzv` can be downloaded and directly visualized in [view.qiime2.org](https://view.qiime2.org/).
The top plot corresponds to cross-validation accuracy.  The bottom plot corresponds to overall model fit.

The raw differentials can be viewed as a table using the following command.

```
qiime metadata tabulate \
	--m-input-file microbe_differentials/differentials.qza \
	--o-visualization differentials_viz.qzv
```

The `differentials_viz.qzv` can be viewed in [view.qiime2.org](https://view.qiime2.org/).
This applies to every file that has a `.qzv` extension.

In addition, the differentials can be unpacked as follows

```
qiime tools export \
	--input-path microbe_differentials/differentials.qza \
	--output-path microbe_differentials/diffs
```

The resulting text file under `microbe_differentials/diffs` can be viewed in your favorite spreadsheet program.


To access model fit, it is recommended to try to run a baseline model.  This baseline model is generally a very simple
model, usually a model with fewer covariates.  Here, we will run a model with just the intercept.

```
qiime songbird multinomial \
	--i-table otus_nt.qza \
	--m-metadata-file sample-metadata.txt \
	--p-formula "1" \
	--p-epochs 500 \
	--p-training-column Testing \
	--p-summary-interval 1 \
	--output-dir microbe_baseline_differentials \
	--verbose
```

We can now compare the baseline model to the previous model we built.

```
qiime songbird summarize-paired \
	--i-regression-stats microbe_differentials/regression_stats.qza \
	--i-baseline-stats microbe_baseline_differentials/regression_stats.qza \
	--o-visualization paired_regression_summary.qzv
```

The obvious trend is that the baseline has a much higher cross-validation error compared to the previous model.
Furthermore, there is a _Q<sup>2</sup>_ value - this can be interpreted similarly to _R<sup>2</sup>_.
The _Q<sup>2</sup>_ value measures the error in the samples that we held out for cross validation.

Once we are happy with our model, the estimated differentials can be readily visualized using qurro

```
qiime qurro differential-plot \
	--i-ranks microbe_differentials/differentials.qza \
	--i-table otus_nt.qza \
	--m-sample-metadata-file sample-metadata.txt \
	--m-feature-metadata-file taxonomy.tsv \
	--o-visualization qurro_viz.qzv
```

The `differentials-viz.qzv` can be viewed in [view.qiime2.org](https://view.qiime2.org/).


## 4. Considerations

The workflow presented here is designed to be easy to understand and use.  However, note that there are still limitations.
First, while we can pick pairs of microbes of interest, intelligently choosing interesting microbes is still a challenging task.
It is still possible have issues with false discovery rate.

Furthermore, differential abundance is not a replacement for beta diversity - if there isn't a notable trend in beta diversity, then one shouldn't expect meaningful results in the differential abundance analysis.

Finally, the multinomial model does not account for overdispersion, so some of the differentials, particularly low abundance taxa maybe still unreliable.


## 5. Other tools

It is worth noting that differentials can be properly computed by many other differential abundance tools such as aldex2, corncob and DESeq2.  The main question up for debate is whether or not microbe can be detected to be significantly changed or not.

## 6. References

See [songbird documentation](https://github.com/biocore/songbird) for more information.


Morton, J.T., Marotz, C., Washburne, A., Silverman, J., Zaramela, L.S., Edlund, A., Zengler, K. and Knight, R., 2019. Establishing microbial composition measurement standards with reference frames. Nature communications, 10(1), p.2719.
