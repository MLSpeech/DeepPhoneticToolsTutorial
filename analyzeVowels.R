########################################################
### Examine data from AutoVowelDuration and DeepFormants

# Code for BigPhon tutorial, July 2016
# Emily Cibelli, emily.cibelli@northwestern.edu

# Last updated: 7/12/16
#######################################################

# ----------------------------------------------------

#############################
# ......... Setup ..........#
#############################

library(lattice)
library(reshape2)

### Read in data
dfDuration = read.csv("sampleFiles/vowel_durations.csv", head = T)
dfFormant = read.csv("sampleFiles/formants.csv", head = T)

### Remove all path and extension info from filenames
dfFormant[,1] = gsub(".*/","",dfFormant[,1])
dfFormant[,1] = gsub(".wav","",dfFormant[,1])
dfDuration[,1] = gsub(".*/","",dfDuration[,1])
dfDuration[,1] = gsub(".wav","",dfDuration[,1])

### Combine formant and duration data
durCol1 = colnames(dfDuration)[1]
formCol1 = colnames(dfFormant)[1]
dfVowel = merge(dfDuration, dfFormant, by.x = durCol1, by.y = formCol1)
colnames(dfVowel)[1] = "file"
colnames(dfVowel)[2] = "duration"
colnames(dfVowel)[3] = "start_time"
colnames(dfVowel)[4] = "end_time"

### Add info about items
dfVowel$word = as.factor(as.character(gsub("(.*)_.*", "\\1", dfVowel$file)))
dfVowel$sex = as.factor(as.character(gsub(".*_(.*)", "\\1", dfVowel$file)))

### Add vowel information
dfVowel$vowel = ""
dfVowel[dfVowel$word %in% c("box", "cop", "dot", "god", "mop", "mop2", "pot", "top"),]$vowel = "a"
dfVowel[dfVowel$word %in% c("beach", "deep", "geese", "keep", "peach", "teeth"),]$vowel = "i"
dfVowel[dfVowel$word %in% c("booth", "dupe", "goose", "kook", "pooch", "tooth"),]$vowel = "u"
dfVowel[dfVowel$word %in% c("moat", "moat2"),]$vowel = "ou"
dfVowel$vowel = as.factor(as.character(dfVowel$vowel))


# -----------------------------------------------------

#############################
# ..... Simple plots  ......#
#############################

# ........................
## Plot duration by sex by vowel
bwplot(duration ~ sex | vowel, data = dfVowel,
        main = "Duration  by sex by vowel", ylab = "Duration (ms)")

# ........................
## Relationship in vowel duration between the speakers
dfVowelCast <- dcast(dfVowel[,c("duration", "word", "sex")], 
                     word ~ sex, value.var = "duration") 
plot(male ~ female, data = dfVowelCast, pch = 16, cex = 1.25,
     main = "Duration by speaker", xlab = "Duration: female speaker (ms)", 
     ylab = "Duration: male speaker (ms)")
abline(lm(male ~ female, data = dfVowelCast), lty = 2)
text(250, 220, sprintf("r = %s", round(cor.test(dfVowelCast$male, dfVowelCast$female)$estimate, 3)))

# ........................
## Plot vowel spaces by speaker

# Add colors for vowels
dfVowel$vowelCol = ifelse(dfVowel$vowel == "a", "blue", 
                          ifelse(dfVowel$vowel == "i", "green",
                                 ifelse(dfVowel$vowel == "u", "red", "purple")))

# Set x and y limits by speaker mins and max

maleYLimMin = min(dfVowel[dfVowel$sex == "male",]$F1) -
  min(dfVowel[dfVowel$sex == "male",]$F1)*.1

maleYLimMax = max(dfVowel[dfVowel$sex == "male",]$F1) +
  min(dfVowel[dfVowel$sex == "male",]$F1)*.1

maleXLimMin = min(dfVowel[dfVowel$sex == "male",]$F2) -
  min(dfVowel[dfVowel$sex == "male",]$F2)*.1

maleXLimMax = max(dfVowel[dfVowel$sex == "male",]$F2) +
  min(dfVowel[dfVowel$sex == "male",]$F2)*.1

femaleYLimMin = min(dfVowel[dfVowel$sex == "female",]$F1) -
  min(dfVowel[dfVowel$sex == "female",]$F1)*.1

femaleYLimMax = max(dfVowel[dfVowel$sex == "female",]$F1) +
  min(dfVowel[dfVowel$sex == "female",]$F1)*.1

femaleXLimMin = min(dfVowel[dfVowel$sex == "female",]$F2) -
  min(dfVowel[dfVowel$sex == "female",]$F2)*.1

femaleXLimMax = max(dfVowel[dfVowel$sex == "female",]$F2) +
  min(dfVowel[dfVowel$sex == "female",]$F2)*.1


#Plot
par(mfrow = c(1,2))
plot(F1 ~ F2, data = dfVowel[dfVowel$sex == "male",],
     log = "xy",
     main = "Male speaker", ylab = "F1", xlab = "F2",
     ylim = c(maleYLimMax, maleYLimMin), xlim = c(maleXLimMax, maleXLimMin),
     pch = 16, col = dfVowel$vowelCol)
legend("topleft", c("a", "i", "u"), col = c("red", "green", "blue"), pch = 16) 

plot(F1 ~ F2, data = dfVowel[dfVowel$sex == "female",],
     log = "xy",
     main = "Female speaker", ylab = "F1", xlab = "F2",
     ylim = c(femaleYLimMax, femaleYLimMin), xlim = c(femaleXLimMax, femaleXLimMin),
     pch = 16, col = dfVowel$vowelCol)
legend("topleft", c("a", "i", "u"), col = c("red", "green", "blue"), pch = 16) 
