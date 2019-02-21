# specify input and ouput directories
dir <- "~/master/rumen/dataflow/01-prot/"
dir_out <- "~/master/rumen/dataflow/01-prot/"

files <- list.files("~/master/rumen/dataflow/01-prot/", pattern = ".fast")

#file <- files[[1]]

for (file in files){

df_select_list <- list()
df <- read.csv(paste(dir, file, sep = ""), sep = ",", header = FALSE)
df$V1 <- as.character(df$V1)
df$V1 <- gsub("RMG_", "RMG", df$V1)
df$V1 <- gsub("_none", "none", df$V1)
df$V1 <- gsub("_[^_]+$", "", df$V1)
df$V1 <- gsub("_[^_]+$", "", df$V1)

seq <- 1
k <- 1

# loop through each row (or line basically)
for (j in 1:nrow(df)) {
  

  if (startsWith(df[j, 1], ">")) {
    
    header <- df[j, 1]
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

write.table(selected_long, paste(dir_out, file, sep = ""), row.names = FALSE, 
            col.names = FALSE, quote = FALSE)

}
