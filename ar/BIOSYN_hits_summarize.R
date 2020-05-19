library(data.table)
library(stringr)
library(stringi)

# set data.table threads
setDTthreads(10)

# allow for provide cutoff argument
args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  cutoff = 95
  cutoff2 = 90
} else if (length(args)==2) {
  cutoff = as.numeric(args[1])
  cutoff2 = as.numeric(args[2])
} else {
  stop("Need two arguments: the percent identity cutoff and the percent alignment cutoff!", call.=FALSE)
}

# combine all hits above the set cutoff for all blast outputs
folder <- "~/master/ar/dataflow/03-blast/biosynthesis/"
files <- list.files(folder, pattern = "\\.txt$")

df_list <- list()
i <- 1

for (file in files){
  
  input_file <- paste(folder, file, sep = "")
  
  if (file.size(input_file) > 0){
  
    df <- read.delim(input_file, header=FALSE)
    df <- data.table(df)
    
    if (nrow(df[V3 >= cutoff]) > 0){
      
      df_select = df[V3 >= cutoff]
      df_select[, V13 := (V12/V11)*100]
      df_select2 = df_select[V13 >= cutoff2]
      
      if (nrow(df_select2) > 0){
        
        df_select2 = df_select2[,.(V1,V2,V3,V13)]
        df_list[[i]] <- df_select2
        i <- i + 1
        
      }
    }
  }
}

df_hit_summary <- rbindlist(df_list)
colnames(df_hit_summary) <- c("query_id", "subject_id", "percent_identity", "percent_alignment")

# split query id into the gene id, contig id and genome file name
df_hit_summary <- as.data.frame(df_hit_summary)

for (i in 1:nrow(df_hit_summary)){
  # split query id
  df_hit_summary[i,"gene_id"] <- stri_reverse(str_split_fixed(stri_reverse(df_hit_summary[i,"query_id"]), "_", 3)[[1]])
  df_hit_summary[i,"contig_id"] <- stri_reverse(str_split_fixed(stri_reverse(df_hit_summary[i,"query_id"]), "_", 3)[[2]])
  df_hit_summary[i,"genome_id"] <- stri_reverse(str_split_fixed(stri_reverse(df_hit_summary[i,"query_id"]), "_", 3)[[3]])
}

# add extension for file name
df_hit_summary$file <- paste(df_hit_summary$genome_id, "_rename.fasta", sep = "")

# save the file with the cutoff applied in the file name
save_file <- paste("dataflow/04-tables/BIOSYN_hits_", as.character(cutoff), "_", as.character(cutoff2), ".csv", sep = "")
write.csv(df_hit_summary, save_file, row.names = FALSE)
