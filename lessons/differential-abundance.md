# Differential abundance

## 1. Motivation

Differential abundance is a core technique in every microbiome application.  If a large microbial difference is detected between different environments, the next step is to identify microbes that explain the differences between these environments.  However, this problem can be tricky to answer due to the relative nature of the data that we measured.


The main issue behind differential abundance is compositionality, the mathematical nature of relative measurements.
Consider the example below

![](../img/composition.png)

In the left environment we don't observe the entire environment, but we can count the number of blue and orange microbes.
If there is a major perturbation, and we again count the microbes, there are multiple possibilities that could have explained the difference of proportions between the two environments. One possibility is that the number of blue microbes decreased.  Another possibility is that both the number of blue and orange microbes increased.  The reason behind this confusion is because we are missing information about the total abundance.  More concretely, if we have environment $A = (a_1, ... a_D)$ with proportions from $D$ taxa and the same environment after perturbation $B = (b_1, ... b_D)$, then the following holds.

![](../img/rank-equations1.png)

From sequencing we can measure the proportions _p<sub>A<\sub>_ and _p<sub>B<\sub>_, but in the majority of experiments, the total abundances _N<sub>A<\sub>_ and _N<sub>B<\sub>_ are inaccessible.  Due to this, the ratio _N<sub>A<\sub>_ / _N<sub>B<\sub>_ confounds our inference to determine if a microbe has changed or not.

In essence, it is not possible to infer absolute changes from relative data.

But fear not. While we often cannot infer the absolute change, there are a couple of workarounds.  First, we can compute something that looks like a concentration - by picking a reference microbe, we can look at their ratio, effectively negating the need to measure total biomass.

![](../img/rank-equations2.png)


As a result, we can conduct a statistical test to determine if the log ratio of pairs of microbes have been altered across conditions. One of the outcomes of this procedure is, one would have to determine what a reference microbe needs to be.

Another workaround is to infer the relative changes (which we call the differential).  The ordering of the log fold change is consistent between absolute and relative abundances.

![](../img/rank-equations3.png)

Here, the total biomass does not influence the ordering of the log fold change calculation. As a result, the ranking of the log fold change between the proportions is equal to the ranking of the log fold change between the absolute abundances. This is a huge win for differential abundance methodologies, since many methods can already infer the differential.  The major outstanding issue is how to determine which microbes to focus on.  Since the total biomass fluctuation will confound the absolute log fold change estimates, it won't be possible to build a statistical test to determine if a microbe's abundance has changed or not.

More information these concepts can be found in our paper [here](https://www.nature.com/articles/s41467-019-10656-5)

## 2. Differential abundance workflow


In this tutorial, we will first demonstrate how to run a basic differential abundance analysis using multinomial regression via songbird. Then we will show how to interpret the underlying differentials estimated from songbird.


## Setup
We'll be using the moving picture tutorial data for demonstration.  If you haven't already, download those files using the following commands.

Download Feature Table
`wget https://docs.qiime2.org/2019.7/data/tutorials/moving-pictures/table.qza`

Download Sample metadata
`wget https://data.qiime2.org/2019.7/tutorials/moving-pictures/sample_metadata.tsv`

Download Taxonomy
`wget https://docs.qiime2.org/2019.7/data/tutorials/moving-pictures/taxonomy.qza`


## Running Songbird

Once the tables are downloaded, we can now run the basic multinomial regression command

```
qiime songbird multinomial \
	--i-table table.qza \
	--m-metadata-file sample-metadata.txt \
	--p-formula "subject + body_site" \
	--p-epochs 10000 \
	--p-summary-interval 1 \
	--o-differentials differentials.qza \
	--o-regression-stats regression-stats.qza \
	--o-regression-biplot regression-biplot.qza
```



```
qiime songbird summarize-single \
	--i-regression-stats regression-stats.qza \
	--o-visualization regression-summary.qzv
```

The `regression-summary.qzv` can be downloaded and directly visualized in (view.qiime2.org)[https://view.qiime2.org/].
The top plot corresponds to cross-validation accuracy.  The bottom plot corresponds to overall model fit.

The raw differentials can be viewed as a table using the following command.

```
qiime metadata tabulate \
	--m-input-file differentials.qza \
	--o-visualization differentials-viz.qzv
```

The `differentials-viz.qzv` can be viewed in (view.qiime2.org)[https://view.qiime2.org/].

In addition, the differentials can be unpacked as follows

```
qiime tools export differentials.qza
```

The resulting text file can be viewed in your favorite spreadsheet program.

Finally, this differential abundance analysis can be readily visualized using qurro

```
qiime qurro differential-plot \
	--i-ranks differentials.qza \
	--i-table table.qza \
	--m-sample-metadata sample-metadata.txt \
	--m-feature-metadata taxonomy.tsv \
	--o-visualization qurro-viz.qzv
```

The `differentials-viz.qzv` can be viewed in (view.qiime2.org)[https://view.qiime2.org/].


## Considerations

The workflow presented here is designed to be easy to understand and use.  However, note that there are still limitations.
First, while we can pick pairs of microbes of interest, intelligently choosing interesting microbes is still a challenging task.
It is still possible have issues with false discovery rate.

Furthermore, differential abundance is not a replacement for beta diversity - if there isn't a notable trend in beta diversity, then one shouldn't expect meaningful results in the differential abundance analysis.

Finally, the multinomial model does not account for overdispersion, so some of the differentials, particularly low abundance taxa maybe still unreliable.


## Other tools

It is worth noting that differentials can be properly computed by many other differential abundance tools such as aldex2, corncob and DESeq2.  The main question up for debate is whether or not microbe can be detected to be significantly changed or not.

## References

Morton, J.T., Marotz, C., Washburne, A., Silverman, J., Zaramela, L.S., Edlund, A., Zengler, K. and Knight, R., 2019. Establishing microbial composition measurement standards with reference frames. Nature communications, 10(1), p.2719.
