# specify input and ouput directories
dir <- "~/master/benny/dataflow/01-nucl/"
dir_out <- "~/master/benny/dataflow/01-nucl-headers/"
file <- "Pacbio_dna.fasta"


df_select_list <- list()
df <- read.csv(paste(dir, file, sep = ""), sep = ",", header = FALSE)
df$V1 <- as.character(df$V1)

seq <- 1
j <- 1
k <- 1

# loop through each row (or line basically)
for (j in 1:nrow(df)) {
  

  if (startsWith(df[j, 1], ">")) {
    
    header <- paste(">", "asv", toString(seq), sep = "")
    seq <- seq + 1
    
    df_select_list[[k]] <- header
    k <- k + 1
    
    } else {
    
    df_select_list[[k]] <- df[j, 1]
    k <- k + 1

    }
  
}

selected_long <- as.matrix(unlist(rbind(df_select_list)))
selected_long <- gsub("\"", "", selected_long)

write.table(selected_long, paste(dir_out, "Pacbio_dna.fasta"), row.names = FALSE, 
            col.names = FALSE, quote = FALSE)
