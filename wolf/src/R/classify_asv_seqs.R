library(rRDP)
library(tidyverse)

<<<<<<< HEAD
files <- list.files("~/master/wolf/dataflow/03-asv-seqs-merge")
=======
files <- list.files("~/master/wolf/dataflow/03-asv-seqs")
>>>>>>> bc63259588b9b18c1f659eccbc5b966d470663f4

files_out <- list.files("~/master/wolf/dataflow/03-asv-taxonomy")


for (file in files){

  
  file_out <- paste("~/master/wolf/dataflow/03-asv-taxonomy/", strsplit(file, ".fa")[[1]][1], "-rdp.csv", sep = "")
  
  if(!(file_out %in% files_out)){
  
<<<<<<< HEAD
    seq <- readDNAStringSet(paste("~/master/wolf/dataflow/03-asv-seqs-merge/", file, sep = ""))
=======
    seq <- readDNAStringSet(paste("~/master/wolf/dataflow/03-asv-seqs/", file, sep = ""))
>>>>>>> bc63259588b9b18c1f659eccbc5b966d470663f4
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



