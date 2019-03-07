library(seqinr)

infile <- "~/Downloads/alignment.fasta"
outfile <- "~/Downloads/alignment_renamed.fasta"

#read in alignment
alignment = read.alignment(infile, "fasta", forceToLower = TRUE)

#make mapping file with new names
mapping_file <- as.data.frame(alignment$nam)
colnames(mapping_file) <- "full_id"
mapping_file$new_id <- paste("seq", seq(1, nrow(mapping_file), 1), sep ="")

#write alignment
write.fasta(alignment$seq, mapping_file$new_id, file.out = outfile)
