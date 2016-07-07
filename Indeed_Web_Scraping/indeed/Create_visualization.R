library(ggplot2)
library(maps)
library(openintro)
library(dplyr)

states <- read.csv("state.csv")
states[,'State'] <- tolower(abbr2state(states[,'State']))
states_map <- map_data("state")
states$log <- log(states$NumPostings)
states$percent <- 1 - (states$log-min(states$log)) / (max(states$log)-min(states$log))

# -------------------- plot state count map ---------------------
ggplot(states, aes(map_id = State)) +
  geom_map(aes(fill = -NumPostings), map = states_map) +
  expand_limits(x = states_map$long, y = states_map$lat) + theme_bw() + 
  theme(axis.line=element_blank(),axis.text.x=element_blank(),
        axis.text.y=element_blank(),axis.ticks=element_blank(),
        axis.title.x=element_blank(),
        axis.title.y=element_blank(),legend.position="none",
        panel.background=element_blank(),panel.border=element_blank(),panel.grid.major=element_blank(),
        panel.grid.minor=element_blank(),plot.background=element_blank())
ggsave('state.pdf', path = paste(getwd(),"/usa-map",sep=''), width = 14, height = 10)

# ------------------ plot overall skill profile -------------
skill <- read.csv("skill.csv")
skill$Skill <- factor(skill$Term, levels = skill$Term)
ggplot(skill, aes(Skill, NumPostings, fill='pink')) + theme_bw() + 
  geom_bar(stat = 'identity') + theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(legend.position="none")

ggsave('skill.pdf', path = paste(getwd(),"/usa-map",sep=''), width = 14, height = 10)

# ------------------- plot skill profile by state ----------------
for (state in state2abbr(states$State)) {
  skill <- read.csv(paste(state,'.csv',sep=''))
  skill$Skill <- factor(skill$Term, levels = skill$Term)
  ggplot(skill[1:10,], aes(Skill, NumPostings, fill='pink')) + theme_bw() + 
    geom_bar(stat = 'identity') + theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
    theme(legend.position="none") + theme(axis.text=element_text(size=22),
                                        axis.title=element_text(size=24,face="bold"))
  ggsave(paste(state,'.pdf',sep=''), path = paste(getwd(),"/usa-map",sep=''), width = 14, height = 10)
}



