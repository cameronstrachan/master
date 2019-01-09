library(tidyverse)

df_metrics <- read.csv("~/master/rumen/dataflow/04-analysis-tables/henderson2015-20_320-99_df_metrics_lacto.csv")

library("phyloseq")
library("ape")
library("DESeq2")

OTU = otu_table(otumat, taxa_are_rows = TRUE)
TAX = tax_table(taxmat)
physeq = phyloseq(OTU, TAX)

samplesdata <- sample_data(df_phylocounts_meta)

physeq = phyloseq(OTU, TAX, samplesdata)

diagdds = phyloseq_to_deseq2(physeq, ~ lacto_signal)

#calculate geometric means prior to estimate size factors
gm_mean = function(x, na.rm=TRUE){
  exp(sum(log(x[x > 0]), na.rm=na.rm) / length(x))
}

geoMeans = apply(counts(diagdds), 1, gm_mean)
diagdds = estimateSizeFactors(diagdds, geoMeans = geoMeans)

rm(list=setdiff(ls(), c("diagdds", "physeq", "df_metrics")))

diagdds = DESeq(diagdds, fitType = "parametric", test = "Wald", parallel=TRUE)

res = results(diagdds, cooksCutoff = FALSE)
alpha = 0.05
#sigtab = res[which(res$padj < alpha), ]
sigtab = res[which(res$pvalue < alpha), ]

sigtab = cbind(as(sigtab, "data.frame"), as(tax_table(physeq)[rownames(sigtab), ], "matrix")) 

write.csv(sigtab, "~/master/rumen/dataflow/04-analysis-tables/henderson2015-20_320-99_df_metrics_lacto_DESeq_sigtab.csv")