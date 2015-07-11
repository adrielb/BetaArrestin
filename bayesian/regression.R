library(ggplot2)# {{{
library(dplyr)
library(tidyr)
library(rstan) # }}}

# data {{{
N <- 30
df.sigma=0.1
dfN <- data.frame( l=runif( N, 0.1, 1)
                 ,MI=rnorm(N, 1, df.sigma)
                 ,Expression=as.factor( rep( 'Native', N))
                 )
dfOE <- data.frame( l=runif( N, 0.1, 1)
                 ,Expression=as.factor( rep( 'OE', N))
                 )
dfOE$MI=2*(dfOE$l - 0.4)+rnorm(N,0,df.sigma)
# df <- rbind( dfN, dfOE)
df <- dfN
qplot( x=l, y=MI, data=df, color=Expression, geom="point", ylim=c(-0.5,1.3))


dataList <- list(  dX=0.0001
                 , eps=1e-6
                 , N=nrow(df)
                 , l=df$l
                 , MI_obs=df$MI
                 , Sexp=as.integer(df$Expression)
                 , sigma=df.sigma
                 )
str(dataList)
# }}}

# dso {{{
dso <- stan_model( stanc_ret=stanc(file="./regression.stan") )
# }}}

# optimiztion {{{
toCol <- function (p) {
  txt <- function(i) paste(p,i,"]",sep="")
  cols <- sapply(1:10, txt)
  fit$par[cols] 
}

fit <- c()
dfo <- c()
dfog <- c()
fit <- optimizing( dso
                  ,data=dataList
                  ,init=list(w=1e2,b=0,b2=1e-3,dX=0.01)
                  ,iter=1e3
                  ,save_iterations=TRUE
                  )
fit$value
dfo <- data.frame( df$l
                  ,df$Expression
                  ,MI.F      = toCol("MI[")
                  ,MI.B      = df$MI
                  ,Sves.F    = toCol("Sves[1,")
                  ,Sves.B    = toCol("Sves[2,")
                  ,MAPKpp.F  = toCol("MAPKpp[1,")
                  ,MAPKpp.B  = toCol("MAPKpp[2,")
                  )
# print(dfo)
dfog <- dfo %>% 
  gather( param, value, -df.l, -df.Expression) %>% 
    separate( param, c("param","side"))
# print(dfog)

ggplot( data=dfog, aes(x=df.l, y=value, color=side)) +
geom_line() +
facet_wrap( ~param, scales="free_y" )

names(fit$par)

fit$par['w']
fit$par['b']
fit$par['b2']
fit$par['dX']

N

sort(dfo[,'Sves.F'])

plot(dfo[,'df.l'], dfo[,'Sves.F'])

plot(1:N, sort(dfo[,'Sves.F']))

# }}}

# MCMC Parameter Estimation # {{{

fit <- sampling(dso,
            data=dataList,
            chains=2e1,
            iter=2e2,
            init='random'
            )
samps <- extract(fit)
str(samps)

print(fit)

fit@model_pars

traceplot(fit, "lp__")

traceplot(fit, "w")

traceplot(fit, "b2")

str(fit, max.level=2)


df.Sves <- data.frame(t(samps$Sves[,1,])) %>% 
  mutate(l=df$l) %>% 
    gather( param, Sves, -l ) 
qplot( x=l, y=Sves, data=df.Sves, color=param, geom="line") +
  theme(legend.position="none")

df.MAPKpp <- data.frame(t(samps$MAPKpp[,1,])) %>% 
  mutate(l=df$l) %>% 
    gather( param, MAPKpp, -l ) 
qplot( x=l, y=MAPKpp, data=df.MAPKpp, color=param, geom="line") +
  theme(legend.position="none")

df.MI <- data.frame(t(samps$MI)) %>% 
  mutate(l=df$l) %>% 
  gather( param, MI, -l ) %>% 
  rbind( data.frame( l=df$l, param="data", MI=df$MI))
qplot( x=l, y=MI, data=df.MI, color=param, geom="line")

qplot( x=1:nrow(samps$lp__), y=exp(samps$lp__), geom="line")

qplot( x=samps$w, geom="histogram") + 
  geom_line(aes(x=seq(-1,1,.1), y=dnorm(seq(-1,1,0.1),0,1e-1)))

qplot( x=seq(-1,1,.01), y=dnorm(seq(-1,1,0.01),0,1e-1))

qplot( x=samps$dX, geom="density", xlim=c(0,1)) +
  stat_function(fun=dnorm, arg=list(sd=1e-1), geom="path", color="blue" )

qplot( x=samps$b, geom="density", xlim=c(0,1)) +
  stat_function(fun=dnorm, arg=list(sd=1e-1), geom="path", color="blue" )

qplot( x=samps$b2, geom="density", xlim=c(0,1)) +
  stat_function(fun=dnorm, arg=list(sd=1e-1), geom="path", color="blue" )

qplot( x=samps$w, geom="density", xlim=c(0,1)) +
  stat_function(fun=dnorm, arg=list(sd=1e-1), geom="path", color="blue" )

qplot( x=as.vector(samps$MI), geom="density", xlim=c(0.5,1.5)) + 
  stat_function(fun=dnorm, arg=list(mean=1,sd=df.sigma), geom="path", color="blue" )


summary(samps$b2)

qplot( x=samps$w, y=samps$b )
qplot( x=samps$b, y=samps$b2 )

# }}}
