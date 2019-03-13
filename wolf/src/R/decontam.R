library(dplyr)

# load meta data that specifies control data
df_phylocounts_meta <- read.csv("~/master/wolf/dataflow/00-meta-merge/sample-complete-all.csv")

df_phylocounts_meta$SampleID <- as.character(df_phylocounts_meta$SampleID)
df_phylocounts_meta$Cow <- as.factor(df_phylocounts_meta$Sample)
df_phylocounts_meta$SampleOrControl <- as.factor(df_phylocounts_meta$SampleOrControl)

df_phylocounts_meta <- df_phylocounts_meta %>% 
  unique()

df_phylocounts_meta <- as.data.frame(df_phylocounts_meta)
row.names(df_phylocounts_meta) <- df_phylocounts_meta[,1]
df_phylocounts_meta[,1] <- NULL


# load feature table with both control and normal sampes
df_phlycounts_counts <- read.csv("~/master/wolf/dataflow/03-asv-table-merge/feature-table-97.txt", sep = '\t', skip = 1)
colnames(df_phlycounts_counts)[1] <- "asv_id"

df_phlycounts_counts <- df_phlycounts_counts[order(df_phlycounts_counts$asv_id),] 

numsamples <- length(df_phlycounts_counts)

otumat <- as.matrix(df_phlycounts_counts[,2:numsamples])
rownames(otumat) <- as.data.frame(df_phlycounts_counts)[,1]


# load combined taxonomy
df_phlycounts_tax  <- read.csv("~/master/wolf/dataflow/03-asv-table-merge/taxonomy-complete.tsv", sep = '\t')
df_phlycounts_tax$Confidence <- NULL
colnames(df_phlycounts_tax)[1] <- 'asv_id'
df_phlycounts_tax$Taxon <- gsub("D_.__", "", df_phlycounts_tax$Taxon)

df_phlycounts_tax <- df_phlycounts_tax %>%
  separate(Taxon , into = c("domain", "phylum", "class", "order", "family", "genus", "species"), sep = ";")

df_phlycounts_tax$phylum <- as.character(df_phlycounts_tax$phylum)
df_phlycounts_tax$family <- as.character(df_phlycounts_tax$family)
df_phlycounts_tax$class<- as.character(df_phlycounts_tax$class)
df_phlycounts_tax$order <- as.character(df_phlycounts_tax$order)
df_phlycounts_tax$genus <- as.character(df_phlycounts_tax$genus)
df_phlycounts_tax$species <- as.character(df_phlycounts_tax$species)

df_phlycounts_tax[is.na(df_phlycounts_tax)] <- "NotAssigned"

df_phlycounts_tax <- df_phlycounts_tax[order(df_phlycounts_tax$asv_id),] 

numsamples2 <- length(df_phlycounts_tax)

taxmat <- as.matrix(df_phlycounts_tax[,2:numsamples2])
rownames(taxmat) <- as.data.frame(df_phlycounts_tax)[,1]

library("phyloseq")
library("ape")
library(plyr)

# import tree and load phyloseq obect

tree = read.tree("~/master/wolf/dataflow/04-tree-merge/tree.nwk")

OTU = otu_table(otumat, taxa_are_rows = TRUE)
TAX = tax_table(taxmat)
samplesdata <- sample_data(df_phylocounts_meta)
physeq = phyloseq(OTU, TAX, samplesdata, tree)

# run decomtam

library(decontam)

sample_data(physeq)$is.neg <- sample_data(physeq)$SampleOrControl == "Control"
contam.prev05 <- isContaminant(physeq, method="prevalence", neg="is.neg", threshold=0.2)

List_of_contaminants <- subset(contam.prev05,contam.prev05$contaminant == TRUE)
List_of_contaminants$asv_id <- rownames(List_of_contaminants)
taxa <- as.data.frame(taxmat)
taxa$asv_id <- rownames(taxmat)
List_of_contaminants <- merge(List_of_contaminants, taxa, by="asv_id")

physeq.neg <- prune_samples(sample_data(physeq)$SampleOrControl == "Control", physeq)
physeq.neg.presence <- transform_sample_counts(physeq.neg, function(abund) 1*(abund>0))

physeq.pos <- prune_samples(sample_data(physeq)$SampleOrControl == "Sample", physeq)
physeq.pos.presence <- transform_sample_counts(physeq.pos, function(abund) 1*(abund>0))

df.pres <- data.frame(prevalence.pos=taxa_sums(physeq.pos.presence), prevalence.neg=taxa_sums(physeq.neg.presence),
                      contam.prev=contam.prev05)

ggplot(data=df.pres, aes(x=prevalence.neg, y=prevalence.pos, color=contam.prev.contaminant)) + geom_jitter() + ggtitle("Contamination - TRUE")

#over10 <- rownames(subset(df.pres, prevalence.neg > 1))
all_taxa = taxa_names(physeq)
my_contaminants <- c(subset(List_of_contaminants, select = asv_id))
#my_contaminants <- unique(unlist(c(my_contaminants, over10)))
my_taxa <- all_taxa[!(all_taxa %in% my_contaminants)]
physeq_no_cont = prune_taxa(my_taxa, physeq)


# save decontaminated table

physeq_no_cont_df_count <- as.data.frame(physeq_no_cont@otu_table) %>%
  select(-Mock, -NTCf, -NTCs)

physeq_no_cont_df_count <- cbind(rownames(physeq_no_cont_df_count), physeq_no_cont_df_count)

colnames(physeq_no_cont_df_count)[1] <- "OTU ID"

features_noheader <- physeq_no_cont_df_count[1:nrow(physeq_no_cont_df_count ),]

mat <- as.matrix(features_noheader)
mat <- matrix(mat, ncol = ncol(features_noheader), dimnames = NULL)

mat2 <- t(as.matrix(colnames(features_noheader)))
mat2 <- matrix(mat2, ncol = ncol(features_noheader), dimnames = NULL)

mat_final <- rbind(mat2, mat)

write.table(mat_final, '~/master/wolf/dataflow/03-asv-table-merge/feature-table-no-contam.txt', col.names = FALSE, quote = FALSE, row.names = FALSE, sep = "\t")
