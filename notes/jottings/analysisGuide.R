library('tidyr')
library('dplyr')
library('ggplot2')
setwd("/Users/rhovde/Prospect/WineMixing")

df <- read.csv("white_wines_2weeks.csv")

## We're starting simple, later we can do a cleverer method to take advantage of having
## more information
##
## First, throw out any samples that look completely messed-up.
##
## Then, normalize the data: For each sample, find the median and interquartile range.
## For each datapoint x in that sample, your normalized x will be (x-sample median)/sample IQ range
##
## Then, try some quick diagnostic plots.  Do a boxplot of each sample's GFP levels to check
## variance and to detect outliers (you can throw these out, but note them.)
## Make some qq plots of GFP for each sample to see how far it is from normally distributed. 
## qqnorm is the R command for this.  Send these to me when you get a chance.
##
##
## Start analysis by doing ANOVA (analysis of variance), on each of the strains separately,
## using wine varietal and replicate as the two variables. 
## Here's a useful guide to ANOVA in R: http://www.sthda.com/english/wiki/two-way-anova-test-in-r#compute-two-way-anova-test
## Another good guide to ANOVA concepts: http://www-personal.umich.edu/~gonzo/coursenotes/file4.pdf
## For now, just test pinot against the blends; leave out chard and sb.
##
## fit <- aov(GFP ~ Varietal + Replicate + Varietal:Replicate, data=df)
## For nice diagnostic plots:
## plot(fit) 
## To see variance breakdown and significance test results:
## summary(fit)
## 
## First, check if there is any signficant effect due to the interaction term between 
## replicate and varietal (Varietal:Replicate), and if not, remove it from the analysis:
## fit <- aov(GFP ~ Varietal + Replicate,data=df)
##
## Then, you can check whether replicate number (day+week) and/or varietal have 
## significant effects.
## Effect size of a varietal = (mean of the varietal averaged over replicates) - 
## (mean of pinot averaged over replicates).
##
## Check the signifcance and the effect sizes for each of the strains
## of reporter bacteria, and see if similar trends appear.
##
## Finally, to check if an individual blend is signficantly different from pinot (as opposed)
## to whether there's a difference in any of the blends), use a Tukey HSD test on 
## the varietal variable.  TukeyHSD(fit, which = "varietal")
##
## You could also follow this procedure doing a 3-variables ANOVA with 
## wine varietal, replicate, and strain as your variables, which could increase the power
## if the different strains respond similarly to the different wines, across the different
## replicates.  If you plot GFP for the different replicates, wines, and strains and notice
## similar patterns appearing across the strains, you may want to try this, but it might
## be too complicated a model given the amount of data you have, and I think that treating
## the strains separately is a perfectly reasonable way to do things at this stage.
