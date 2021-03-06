library(stringr)
library(stringi)
source('~/master/ar/modules/R_functions.R')

# allow for provide cutoff argument
args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  cutoff = 100
  cutoff2 = 60
} else if (length(args)==2) {
  cutoff = as.numeric(args[1])
  cutoff2 = as.numeric(args[2])
} else {
  stop("Need two arguments: the percent identity cutoff and the percent alignment cutoff!", call.=FALSE)
}

# combine all hits above the set cutoff for all blast outputs
folder <- "~/master/ar/dataflow/03-blast/pathogens/"
files <- list.files(folder, pattern = "\\.txt$")

df_list <- list()
i <- 1

folder <- "~/master/ar/dataflow/03-blast/pathogens/"
files <- list.files(folder, pattern = "\\.txt$")

df_hit_summary <- summarize_blast_output(folder = folder, files = files, cutoff = cutoff, cutoff2 = cutoff2)

# split query id into the gene id, contig id and genome file name
for (i in 1:nrow(df_hit_summary)){
  # split query id
  df_hit_summary[i,"genome_id"] <- stri_reverse(str_split_fixed(stri_reverse(df_hit_summary[i,"query_id"]), "_", 3)[[3]])
  # split subject id
  df_hit_summary[i,"pathogen_genome_id"] <- stri_reverse(str_split_fixed(stri_reverse(df_hit_summary[i,"subject_id"]), "_", 2)[[2]])
}

# add extension for file name
df_hit_summary$pathogen_file <- paste(df_hit_summary$pathogen_genome_id, "_rename.fasta", sep = "")

# merge with card meta data
df_card_hits <- read.csv("~/master/ar/dataflow/04-tables/CARD_hits_95_90.csv")
df_card_hits <- subset(df_card_hits, select=c("query_id", "card_annotation"))

df_final  <- merge(x=df_hit_summary,y=df_card_hits,by="query_id",all.x=TRUE)

# save the file with the cutoff applied in the file name
save_file <- paste("~/master/ar/dataflow/04-tables/PATH_hits_", as.character(cutoff), "_", as.character(cutoff2), ".csv", sep = "")
write.csv(df_final, save_file, row.names = FALSE)