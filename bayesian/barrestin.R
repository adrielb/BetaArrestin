library(ggplot2)# {{{
library(dplyr)
library(tidyr)
library(rstan) # }}}

# data {{{
N <- 10
dfN <- data.frame( l=runif( N, 0.1, 1)
                 ,MI=rnorm(N, 1, 0.1)
                 ,Expression=as.factor( rep( 'Native', N))
                 )
dfOE <- data.frame( l=runif( N, 0.1, 1)
                 ,Expression=as.factor( rep( 'OE', N))
                 )
dfOE$MI=2*(dfOE$l - 0.4)+rnorm(N,0,0.1)
# df <- rbind( dfN, dfOE)
df <- dfN
qplot( x=l, y=MI, data=df, color=Expression, geom="point")

# }}}

# data list {{{
dataList <- list( Di=0.0001
                 , grad=1
                 , maxdose=1
                 , dX=0.0001
                 , eps=1e-6
                 , N=nrow(df)
                 , l=df$l
                 , MI_obs=df$MI
                 , Sexp=as.integer(df$Expression)
                 )
str(dataList)
# }}}

# dso {{{
dso <- stan_model( stanc_ret=stanc(file="./steady-state-model.stan") )
# }}}

# fixed param {{{
initList=list( Stot=c(1,5)
              ,p2=1
              ,p3=c(1,1)
              ,p4=1
              ,p5=1
              ,sigma=1
              ,S=matrix(1./6,N,6)
              )

fit <- sampling(dso
                , data=c(dataList,initList)
                , chains=1
                , iter=1
                , warmup=0
                , algorithm="Fixed_param"
            )
str(fit, max.level=2)

fit <- sampling(dso
                , data=dataList
                , chains=1
                , iter=1
                , warmup=0
                , algorithm="Fixed_param"
                , init=list(initList)
            )
str(fit, max.level=2)

maxidx <- 10
idx <- 1:maxidx

fit@model_pars

params     <- extract(fit)
df$p1      <- params$p1[maxidx,1,]
df$MI      <- params$MI[maxidx,]
df$eqScyto <- params$eqScyto[maxidx,1,]
df$eqSmem  <- params$eqSmem[maxidx,1,]
df$MAPKpp  <- params$MAPKpp[maxidx,1,]
df$Sves    <- params$Sves[maxidx,1,]
df$Smem    <- params$Smem[maxidx,1,]
df$Scyto   <- params$Scyto[maxidx,1,]
df$Sves    <- params$Sves[maxidx,2,]
df$Smem    <- params$Smem[maxidx,2,]
df$Scyto   <- params$Scyto[maxidx,2,]

# individual state plots {{{
qplot( x=l, y=p1, data=df, color=Expression, geom="line")

qplot( x=l, y=MI, data=df, color=Expression, geom="line")

qplot( x=l, y=eqScyto, data=df, color=Expression, geom='line')

qplot( x=l, y=eqSmem, data=df, color=Expression, geom='line')

qplot( x=l, y=Sves, data=df, color=Expression, geom='line')

qplot( x=l, y=Smem, data=df, color=Expression, geom='line')

qplot( x=l, y=Scyto, data=df, color=Expression, geom='line')

qplot( x=l, y=MAPKpp, data=df, color=Expression, geom='line')
# }}}
# facet state plot {{{
dfg <- df %>% gather( param, value 
                     , p1, eqScyto, eqSmem, Sves, Smem, Scyto, MAPKpp, MI)
ggplot( data=dfg, aes(x=l, y=value, color=Expression)) +
  geom_line() +
  facet_wrap( ~param, scales="free_y" )
# }}}

# parameter plot {{{
dfp <- data.frame( iter=1:maxidx
                  , Stot.Native=params$Stot[,1]
                  , Stot.OE=params$Stot[,2]
                  , lp=params$lp__
                  , p2=params$p2
                  , p4=params$p4
                  , p5=params$p5
                  , sigma=params$sigma
                  )
dfpg <- dfp %>% gather( param, value
                       , Stot.Native, Stot.OE, p2, p4, p5, sigma, lp )
qplot( x=iter, y=value, data=dfpg, color=param, geom="line")

ggplot( data=dfpg, aes(x=iter, y=value, color=param)) +
geom_line() +
facet_wrap( ~param, scales="free_y" )
# }}}

# }}}

# optimiztion {{{
fit <- optimizing( dso, data=dataList, init=initList)

fit <- optimizing( dso
                  ,data=c( dataList, initList)
                  ,iter=1e5
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


# }}}

# MCMC Parameter Estimation # {{{

fit <- sampling(dso,
            data=c(dataList,initList),
            chains=10,
            iter=1e2,
            init='random'
            )

fit <- sampling(dso,
            data=dataList,
            chains=10,
            iter=1e2,
            init='random'
            )

print(fit)

plot(fit)

fit@model_pars

traceplot(fit, "lp__")

str(fit, max.level=2)

str(fit@sim, max.level=2)

samps <- extract(fit)
str(samps)

qplot( x=1:nrow(samps$lp__), y=exp(samps$lp__), geom="line")

hist( samps$sigma, breaks=30 )
quantile( samps$sigma )

plot( samps$sigma, samps$lp__ )

plot( samps$sigma, exp(samps$lp__) )

samps$Stot[,1]

qplot( x=samps$Stot[,1], geom="histogram")

qplot( x=samps$Stot[,2], geom="histogram")

params$S[200,1,] %>% sum()

params$StotExp

# }}}
