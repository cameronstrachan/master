library(tidyverse) 

df_metrics <- read.csv("~/master/rumen/dataflow/04-analysis-tables/henderson2015-20_320-99_df_metrics_lacto_1000.csv")

df_phlycounts_counts <- df_metrics %>%
  select(asv_id, GRCid, count) %>%
  spread(GRCid, count)

df_phlycounts_counts[is.na(df_phlycounts_counts)] <- 0

df_phlycounts_counts <- df_phlycounts_counts[order(df_phlycounts_counts$asv_id),] 

numsamples <- length(df_phlycounts_counts)

otumat <- as.matrix(df_phlycounts_counts[,2:numsamples])
rownames(otumat) <- as.data.frame(df_phlycounts_counts)[,1]

df_phlycounts_tax <- df_metrics %>%
  select(asv_id, phylum, family, genus) %>%
  unique()

df_phlycounts_tax$phylum <- as.character(df_phlycounts_tax$phylum)
df_phlycounts_tax$family <- as.character(df_phlycounts_tax$family)
df_phlycounts_tax$genus <- as.character(df_phlycounts_tax$genus)

df_phlycounts_tax[is.na(df_phlycounts_tax)] <- "NotAssigned"

df_phlycounts_tax <- df_phlycounts_tax[order(df_phlycounts_tax$asv_id),] 

taxmat <- as.matrix(df_phlycounts_tax[,2:4])
rownames(taxmat) <- as.data.frame(df_phlycounts_tax)[,1]

df_phylocounts_meta <- df_metrics %>% 
  select(GRCid, lacto_signal) %>%
  unique() 

df_phylocounts_meta$lacto_signal <- as.factor(df_phylocounts_meta$lacto_signal)

df_phylocounts_meta <- as.data.frame(df_phylocounts_meta)

row.names(df_phylocounts_meta) <- df_phylocounts_meta[,1]

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

rm(list=setdiff(ls(), c("diagdds", "physeq")))

diagdds = DESeq(diagdds, fitType = "parametric", test = "Wald", parallel=TRUE)

res = results(diagdds, cooksCutoff = FALSE)
alpha = 0.15
#sigtab = res[which(res$padj < alpha), ]
sigtab = res[which(res$pvalue < alpha), ]

sigtab = cbind(as(sigtab, "data.frame"), as(tax_table(physeq)[rownames(sigtab), ], "matrix")) 

write.csv(sigtab, "~/master/rumen/dataflow/04-analysis-tables/henderson2015-20_320-99_df_metrics_lacto_DESeq_sigtab_1000.csv")