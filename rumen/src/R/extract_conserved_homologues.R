df_pi <- read.csv("~/master/rumen/dataflow/04-analysis-tables/selected_genomes_rbh_90pi.csv")
df_pi$X <- NULL

unique(df_pi$file1)

df_pi_hom <- df_pi %>%
  group_by(qseqid) %>%
  mutate(ngenomes = length(unique(file2))) %>%
  mutate(mean_pi_gene = mean(mean_pi)) %>%
  ungroup() %>%
  select(qseqid, ngenomes, mean_pi_gene) %>%
  distinct() %>%
  filter(ngenomes > 36) %>%
  filter(mean_pi_gene > 97)

write.csv(df_pi_hom, "dataflow/00-meta/df_conserved_homologues.csv")