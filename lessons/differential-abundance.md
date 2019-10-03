# Differential abundance

## Motivation

## Compositional effects

## Running Songbird

```
qiime songbird multinomial \
    --i-table redsea.biom.qza \
    --m-metadata-file data/redsea/redsea_metadata.txt \
    --p-formula "Depth+Temperature+Salinity+Oxygen+Fluorescence+Nitrate" \
    --p-epochs 10000 \
    --p-differential-prior 0.5 \
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

```
qiime metadata tabulate \
    --m-input-file differentials.qza \
    --o-visualization differentials-viz.qzv
```


## Considerations

Multinomial and overdispersion


## Other tools

It is worth noting that differentials can be properly computed by many other differential abundance tools such as aldex2, corncob and DESeq2.  The main question up for debate is whether or not microbe can be detected to be significantly changed or not.

## References
