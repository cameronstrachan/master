library(data.table)

# set data.table threads
#setDTthreads(10)

summarize_blast_output <- function(folder = folder, files = files, cutoff = cutoff, cutoff2 = cutoff2){
  
  df_list <- list()
  i <- 1
  
  for (file in files){
    
    input_file <- paste(folder, file, sep = "")
    
    if (file.size(input_file) == 0) next
    
    df <- read.delim(input_file, header=FALSE)
    df <- data.table(df)
    
    if (nrow(df[V3 >= cutoff]) > 0){
      
      df_select = df[V3 >= cutoff]
      df_select[, V13 := (V12/V11)*100]
      df_select2 = df_select[V13 >= cutoff2]
      
      if (nrow(df_select2) > 0){
        
        df_select2 = df_select2[,.(V1,V2,V3, V4, V5, V13)]
        df_select2$V14 <- file
        df_list[[i]] <- df_select2
        i <- i + 1
        
      }
    }
  }
  
  df_hit_summary <- rbindlist(df_list)
  colnames(df_hit_summary) <- c("query_id", "subject_id", "percent_identity", "subject_start", "subject_end", "percent_alignment", "query_file")
  df_hit_summary <- as.data.frame(df_hit_summary)
  
  return(df_hit_summary)
}