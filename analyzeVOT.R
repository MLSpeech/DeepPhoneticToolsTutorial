########################################################
### Examine data from AutoVOT

# Code for BigPhon tutorial, July 2016
# Emily Cibelli, emily.cibelli@northwestern.edu

# Last updated: 7/12/16
#######################################################

# ----------------------------------------------------

#############################
# ......... Setup ..........#
#############################

library(lattice)

dfVOT = read.csv("sampleFiles/vot.csv", head = T)
colnames(dfVOT)[1] = "file"
dfWord = read.csv("sampleFiles/word_durations.csv", head = T)
colnames(dfWord) = c("file", "duration", "start_time", "end_time")

### Remove all path and extension info from filenames
dfVOT[,1] = gsub(".*/","",dfVOT[,1])
dfVOT[,1] = gsub(".wav","",dfVOT[,1])
dfWord[,1] = gsub(".*/","",dfWord[,1])
dfWord[,1] = gsub(".wav","",dfWord[,1])

### Merge
dfVOT = merge(dfVOT, dfWord, by = "file")

### Convert VOT to ms
dfVOT$vot = dfVOT$vot*1000

### Calculate VOT as a proportion of word duration
dfVOT$votRatio = dfVOT$vot/dfVOT$duration

### Add info about items
colnames(dfVOT)[1] = "file" 
dfVOT$word = as.factor(as.character(gsub("(.*)_.*", "\\1", dfVOT$file))) 
dfVOT$sex = as.factor(as.character(gsub(".*_(.*)", "\\1", dfVOT$file))) 

### Remove m-initial words and add info about initial consonant
dfVOT = dfVOT[!dfVOT$word %in% c("mop", "moat", "mop2", "moat2"),] 
dfVOT$word = factor(dfVOT$word) 
dfVOT$consonant = "" 
dfVOT[dfVOT$word %in% c("beach", "booth", "box"),]$consonant = "b" 
dfVOT[dfVOT$word %in% c("deep", "dot", "dupe"),]$consonant = "d" 
dfVOT[dfVOT$word %in% c("geese", "god", "goose"),]$consonant = "g" 
dfVOT[dfVOT$word %in% c("peach", "pooch", "pot"),]$consonant = "p" 
dfVOT[dfVOT$word %in% c("teeth", "tooth", "top"),]$consonant = "t" 
dfVOT[dfVOT$word %in% c("cop", "keep", "kook"),]$consonant = "k" 
dfVOT$consonant = as.factor(as.character(dfVOT$consonant)) 

### Add voicing
dfVOT$voicing = ifelse(dfVOT$consonant %in% c("b", "d", "g"), "voiced", "voiceless") 
dfVOT$voicing = as.factor(as.character(dfVOT$voicing)) 

### Add place of articulation
dfVOT$poa = ifelse(dfVOT$consonant %in% c("b", "p"), "bilabial",  
                   ifelse(dfVOT$consonant %in% c("t", "d"), "alveolar", "velar")) 
dfVOT$poa = as.factor(as.character(dfVOT$poa)) 
dfVOT$poa = ordered(dfVOT$poa, levels = c("bilabial", "alveolar", "velar")) 

# -----------------------------------------------------------

#############################
# ......... Plots ..........#
#############################

### Plot VOT and VOT ratio by voicing
par(mfrow = c(1,2))
boxplot(vot ~ voicing, data = dfVOT,
        main = "VOT by voicing", ylab = "Duration (ms)")
boxplot(votRatio ~ voicing, data = dfVOT,
        main = "VOT ratio by voicing", ylab = "Proportion of word dur.")


### Plot VOT by voicing by place of articulation
bwplot(vot ~ voicing | poa, data = dfVOT, ylab = "Duration (ms)")
# Velar VOTs expected to be longer - holds in this case

### The same, with VOT ratio
bwplot(votRatio ~ voicing | poa, data = dfVOT, ylab = "Duration (ms)")
