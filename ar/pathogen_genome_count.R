pathogens = c('staphylococcus_aureus', 'campylobacter_coli', 'campylobacter_jejuni', 'clostridioides_difficile', 'salmonella_typhimurium', 'salmonella_newport', 'staphylococcus_pseudintermedius', 'streptococcus_agalactiae', 'enterococcus_faecium', 'erysipelothrix_rhusiopathiae', 'streptococcus_suis')
location <- "~/master/ar/dataflow/01-dbs/pathogens/"

count_list <- list()

for (pathogen in pathogens){
    folder <- paste(location, pathogen, '/', sep = '')
    n_files <- length(list.files(folder, pattern = "\\.fasta$"))
    count_list[[pathogen]] <- n_files
}

df_count <- t(as.data.frame(count_list))
write.csv(df_count, '~/master/ar/dataflow/00-meta/pathogen_genome_count.csv')

