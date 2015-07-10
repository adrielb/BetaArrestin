library(ggplot2)# {{{
library(dplyr)
library(tidyr)
library(rstan) # }}}

# data {{{
N <- 10
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
qplot( x=l, y=MI, data=df, color=Expression, geom="point")

# }}}

# data list {{{
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
fit <- optimizing( dso
                  ,data=dataList
                  ,iter=1e1
                  ,save_iterations=TRUE
                  )
fit$value

names(fit$par)

toCol <- function (p) {
  txt <- function(i) paste(p,i,"]",sep="")
  cols <- sapply(1:10, txt)
  fit$par[cols] 
}

dfo <- data.frame( df$l
                  ,df$Expression
                  ,MI.F      = toCol("MI[")
                  ,MI.B      = df$MI
                  ,Scyto.F   = toCol("Scyto[1,")
                  ,Scyto.B   = toCol("Scyto[2,")
                  ,Smem.F    = toCol("Smem[1,")
                  ,Smem.B    = toCol("Smem[2,")
                  ,Sves.F    = toCol("Sves[1,")
                  ,Sves.B    = toCol("Sves[2,")
                  ,MAPKpp.F  = toCol("MAPKpp[1,")
                  ,MAPKpp.B  = toCol("MAPKpp[2,")
                  ,eqSmem.F  = toCol("eqSmem[1,")
                  ,eqSmem.B  = toCol("eqSmem[2,")
                  ,eqScyto.F = toCol("eqScyto[1,")
                  ,eqScyto.B = toCol("eqScyto[2,")
                  )
print(dfo)

dfog <- dfo %>% 
  gather( param, value, -df.l, -df.Expression) %>% 
    separate( param, c("param","side"))
print(dfog)

ggplot( data=dfog, aes(x=df.l, y=value, color=side)) +
geom_line() +
facet_wrap( ~param, scales="free_y" )

# }}}

# MCMC Parameter Estimation # {{{

fit <- sampling(dso,
            data=dataList,
            chains=1,
            iter=1e3,
            init='random'
            )

print(fit)

plot(fit)

fit@model_pars

traceplot(fit, "lp__")

traceplot(fit, "w")

str(fit, max.level=2)


samps <- extract(fit)
str(samps)

df.MI <- data.frame(t(samps$MI))
df.MI$l <- df$l
df.MI <- df.MI %>% gather( param, MI, -l )
df.MI$param <- "samples"
df.MI <- rbind( df.MI, data.frame( l=df$l, param="data", MI=df$MI))
qplot( x=l, y=MI, data=df.MI, color=param, geom="point")

df.Sves <- data.frame(t(samps$Sves[,1,])) %>% 
  mutate(l=df$l) %>% 
    gather( param, Sves, -l ) 
qplot( x=l, y=Sves, data=df.Sves, color=param, geom="line")



df.Sves %>% tail()

qplot( x=1:nrow(samps$lp__), y=exp(samps$lp__), geom="line")

qplot( x=samps$w, geom="histogram")   

qplot( x=samps$b, geom="histogram")   

# }}}
