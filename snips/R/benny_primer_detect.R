#Read in data
library(dada2)
library(ShortRead)

#Set path to folder in which you have your data
path <- "~/master/wolf/dataflow/01-fastq/wetzels2018" 

#Check if path is correct and all files are here
list.files(path)

#Read in forward and reverse fastq files
fnFs <- sort(list.files(path, pattern="R1_001.fastq", full.names = TRUE))
fnRs <- sort(list.files(path, pattern="R2_001.fastq", full.names = TRUE))

# Extract sample names, assuming filenames have format: xxx_SAMPLENAME_XXX.fastq
sample.names <- sapply(strsplit(basename(fnFs), "_"), `[`, 2)

#FWD <- "GTGCCAGCMGCCGCGGTAA"  ## forward primer sequence
#REV <- "GGACTACHVGGGTWTCTAAT"  ## reverse primer sequence

FWD <- "GTGYCAGCMGCCGCGGTAA"  ## forward primer sequence
REV <- "GGACTACNVGGGTWTCTAAT"  ## reverse primer sequence

#Function to create all orientations of the input sequence
allOrients <- function(primer) {
  require(Biostrings)
  dna <- DNAString(primer)  # The Biostrings works w/ DNAString objects rather than character vectors
  orients <- c(Forward = dna, Complement = complement(dna), Reverse = reverse(dna), 
               RevComp = reverseComplement(dna))
  return(sapply(orients, toString))  # Convert back to character vector
}

#Apply function on primer sequence
FWD.orients <- allOrients(FWD)
REV.orients <- allOrients(REV)
FWD.orients
REV.orients

#The presence of ambiguous bases (Ns) in the sequencing reads makes accurate mapping of short primer sequences difficult. Next we are going to "pre-filter" the sequences just to remove those with Ns, but perform no other filtering.

fnFs.filtN <- file.path(path, "filtN", basename(fnFs)) # Put N-filterd files in filtN/ subdirectory
fnRs.filtN <- file.path(path, "filtN", basename(fnRs))

#filterAndTrim(fnFs, fnFs.filtN, fnRs, fnRs.filtN, maxN = 0, multithread = TRUE)

#We are now ready to count the number of times the primers appear in the forward and reverse read, while considering all possible primer orientations. Identifying and counting the primers on one set of paired end FASTQ files is sufficient, assuming all the files were created using the same library preparation, so we'll just process the first sample.

# Function to count number of reads in which the primer is found
primerHits <- function(primer, fn) {
  nhits <- vcountPattern(primer, sread(readFastq(fn)), fixed = FALSE)
  return(sum(nhits > 0))
}

#Apply function to check for primers
rbind(FWD.ForwardReads = sapply(FWD.orients, primerHits, fn = fnFs.filtN[[1]]), 
      FWD.ReverseReads = sapply(FWD.orients, primerHits, fn = fnRs.filtN[[1]]), 
      REV.ForwardReads = sapply(REV.orients, primerHits, fn = fnFs.filtN[[1]]), 
      REV.ReverseReads = sapply(REV.orients, primerHits, fn = fnRs.filtN[[1]]))

