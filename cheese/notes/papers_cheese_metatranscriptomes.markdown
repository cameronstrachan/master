| Cheese metatranscriptomes | 27-11-2018 |
| -------------------- | ---------- |

### Investigation of the Activity of the Microorganisms in a Reblochon-Style Cheese by Metatranscriptomic Analysis

_Monnet_

**paper**

- The cheese were produced using  two lactic acid bacteria (Streptococcus thermophilus and Lactobacillus delbrueckii ssp. bulgaricus), one ripening bacterium (Brevibacterium aurantiacum), and two yeasts (Debaryomyces hansenii and Geotrichum candidum).
- Also want to deplete fungal rRNA.
- TruSeq library prep and 50 bp size.
- The most reads by far mapped to the yeast (80% of the reads)


**method**

- 500mg of sample
- The main method was taken from a 2008 paper (55 citations), focused on RNA extraction from cheese.
- Mention how careful they are to use RNAase-free everything.

1. Add sample to tube containing 800 mg beads and then all 1.25 ml of TRIzol right way.
2. Bead beating using 3 x 60s sequences, with ice cooling before each time
3. Spin 10 min at 12,000 at 4C, then transfer supernatant to a 2mL tube containing 300uL of Phase Lock Gel (additional red layer also transferred, however the fat layer at the top of the liquid phase was left).
4. Tubes incubated for 5 min before adding chloroform.
5. Tubes shaken for 15s, incubated 3 mins at room then 2 min on ice.
6. Centrifuged for 10 min at 12,000 at 4C.
7. Approximately 700uL of the aqueous phase was recovered, careful not to recover the organic phase.
8. Add 700 uL of phenol-chlorophron-isoamyl alcohol (125:24:1, ph 4.7)
9. Shake 15s, 10 min 12,000 at 4C sping.
10. Remove aqueous phase (550uL), don't remove any of the orgaanic phase.
11. 3 replicates pooled and 55% volume of 100% alcohol added.
12. Load 700 uL on RNeasy spin column, which is centrifuged at 12,000 at room temp.
13. Remove flow through and spin the rest of the sample through.
14. Washed with RW1 buffer then 2 washes with 500uL RPE buffer, with extra centrifuging to remove buffer.
15. RNA recovered with RNA free water.

- DNA quatified with Quibit and quality checked with bioanalyzer.
- 10ug of the total RNA was then subjected to rRNA depletion using the epicentre ribo zero kit.

*experiment*

- 70-90 million reads for each of 12 cheese rind samples (3 replicates at four sampling times)
- DAN quality really decreased at later days (day 35)

[paper link](https://www.frontiersin.org/articles/10.3389/fmicb.2016.00536/full)

### Metatranscriptomics reveals temperature-driven functional changes in microbiome impacting cheese maturation rate

_Defilippis_

- Also observed "non-starter" lac acid bacteria
- Cheese manufacturing is characterized by successions of different lactic acid bacteria. Mesophilic non started lactic acid bacteria take over later.
- Looked at genes for lactose breakdown (LacZ), Leloir and tagastose pathways.
- Measured SCFA
- Used the PowerMicrbiome RNA isolation kit
- Used Bowtie2 to map to the RefSeq genome ORFs
