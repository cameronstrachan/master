### package-less script to take gdtb output, select a genus, and save a data frame with the file, accession and species 

# HARDCODED
# select genus, gtdb output and the fasta file ending for the genomes used
genus <- "Campylobacter_D"
file <- "./dataflow/00-meta/gtdbtk.bac120.summary.tsv"
genome_file_ending <- ".fna"

# script

df_gtdbk_output <- read.delim(file, colClasses = "character")
df_gtdbk_output <- df_gtdbk_output[,1:2]
df_gtdbk_output$file <- paste(df_gtdbk_output$user_genome, genome_file_ending, sep = "")
df_gtdbk_selected <- df_gtdbk_output[grepl(genus, df_gtdbk_output$classification),]

for (i in 1:nrow(df_gtdbk_selected)){
  classifications <- df_gtdbk_selected$classification
  species <- strsplit(classifications[i], "s__")[[1]][2]
  
  if (is.na(species)){
    species <- paste(genus, "unclassified")
  }
  
  df_gtdbk_selected$species[i] <- species
  
  genomes <- df_gtdbk_selected$user_genome
  prefix <- strsplit(genomes[i], "_")[[1]][1]
  acc_number <- strsplit(genomes[i], "_")[[1]][2]
  df_gtdbk_selected$accession[i] <- paste(prefix, acc_number, sep = "_")
}

df_gtdbk_selected$user_genome <- NULL
df_gtdbk_selected$classification <- NULL

output_file <- paste("dataflow/00-meta/gtdbtk_", genus, ".csv", sep ="")

write.csv(df_gtdbk_selected, output_file, row.names=FALSE)
