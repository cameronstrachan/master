library(rRDP)
library(tidyverse)

files <- list.files("~/master/wolf/dataflow/03-asv-seqs-merge")

files_out <- list.files("~/master/wolf/dataflow/03-asv-taxonomy")


for (file in files){

  
  file_out <- paste("~/master/wolf/dataflow/03-asv-taxonomy/", strsplit(file, ".fa")[[1]][1], "-rdp.csv", sep = "")
  
  if(!(file_out %in% files_out)){
  
    seq <- readDNAStringSet(paste("~/master/wolf/dataflow/03-asv-seqs-merge/", file, sep = ""))
    pred <- predict(rdp(), seq)
    conf <- attr(pred, "confidence")
    
    pred$asv_id <- row.names(pred)
    conf <- as.data.frame(conf)
    colnames(conf) <- paste(colnames(conf), "conf", sep = "_")
    conf$asv_id <- row.names(conf)
  
    df_taxa <- inner_join(pred, conf) 
    
    write.csv(df_taxa, file_out)
  }
  
  
}



