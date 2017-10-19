## Compiling some results

library(tidyverse)
library(stringr)

n = 9 # number of vertices

df <- tibble()

for (i in 1:9) {
  
  filename <- str_c("results", n, "_", i, "of", n, ".csv")
  current.df <- read_csv(filename) 
  
  df <- rbind(df, current.df)
}

# write csv