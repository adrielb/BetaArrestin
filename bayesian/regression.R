# libs # {{{
library(ggplot2)
library(dplyr)
library(tidyr)
library(rstan) 
# }}}

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
dfOE$MI=2*(dfOE$l - 0.4)+0*rnorm(N,0,df.sigma)
# df <- rbind( dfN, dfOE)
df <- dfOE
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

# covariance matrix Sigma # {{{
x <- seq(0,10)/100.
o <- outer(x,x, FUN="-")
S <- exp( -o^2 ) + exp( -o^2*100 )
chol(S)

chol(outer(x,x))

max(S*lower.tri( S ))

tail(x,-1) - head(x,-1) 
# }}}

dso.gp.fit <- stan_model( stanc_ret=stanc(file="./gp-fit.stan") )

# df.biphasic {{{
biphasicCurve <- function (x) {
  a <- 6.06
  b <- 1.02e3
  c <- -4.54
  d <- 5.
  g <- 1.65e-1
  g + (a + b*x)/(1 + exp(-c + d*x))
}

df.biphasic <- data.frame( s=seq(0,2,0.1) ) 
df.biphasic$y <- biphasicCurve( df.biphasic$s )

qplot( x=s, y=y, data=df.biphasic, geom="line") +
  geom_point()
# }}}

# gp.params optimiztion {{{
fitlist = list( N=nrow(df.biphasic)
               ,x=df.biphasic$s
               ,y=df.biphasic$y
               )
gp.params <-NULL
gp.params <- optimizing( dso.gp.fit
                  ,data=fitlist
                  ,iter=1e3
                  ,save_iterations=TRUE
                  )
gp.params

# R> gp.params
# $par
#     eta_sq     rho_sq     sig_sq
# 1.83226244 0.38441566 0.01130754

# $value
# [1] 44.31785

gp.params$par["eta_sq"]

# }}}

# gp.params sampling {{{

gp.params.sampling <- NULL
gp.params.sampling <- sampling(dso.gp.fit
                , data=fitlist
                , chains=8
                , iter=1e3
                )
samps <- extract(gp.params.sampling)
str(samps)

print(gp.params.sampling)

traceplot(gp.params.sampling)

traceplot(gp.params.sampling, "lp__")

qplot( x=samps$eta_sq, geom="density", xlim=c(0,10)) +
  stat_function(fun=dcauchy, arg=list(scale=5), geom="line", color="blue" ) +
  geom_vline( xintercept=gp.params$par["eta_sq"], size=2, color='red')

df.fit <- data.frame( samps ) %>% 
  filter( eta_2 < 100, eta_sq < 500 ) %>% 
  gather( param, value ) %>% 
  transform( param=factor(param, levels=c("eta_2","rho_2","sig_sq","eta_sq","rho_sq","lp__")))
ggplot( data=df.fit, aes(x=value)) +
  geom_density(fill="black", alpha=0.5 ) +
  facet_wrap( ~param, scales="free" ) +
  geom_vline( aes(xintercept=x)
             ,data=data.frame(x=gp.params$par, param=names(gp.params$par))
             ,size=2, color='red', alpha=0.5)

df.fit %>% 
  group_by(param) %>% 
    summarize( val=median(value))

# }}}

dso.gp.sim <- stan_model( stanc_ret=stanc(file="./gp-regression.stan") )

# simulation sampling # {{{
dplist <- c( list( N=2*nrow(df.biphasic) 
                  ,x=c( df.biphasic$s, head(df.biphasic$s,1)+0.1)) 
  , as.list(gp.params$par) )
dplist$N <- length(dplist$x)

dplist <- list( 
   N=51
  ,x=seq(-10,10,.4)
  , rho_sq = 1./10000
  , eta_sq = 100
  , sig_sq = 1e-3
)

with( dplist,
     qplot(c(0, 1)
           , stat = "function"
           , fun=function(x) eta_sq*exp(-rho_sq*(x^2)) 
           , geom = "line"
           , ylim = c(0,eta_sq)
           ) +
     geom_hline( yintercept=eta_sq, size=2, color='red', alpha=0.5)
)

qplot(sort(df$l),1,geom="point")


gp.sampling <- NULL
gp.sampling <- 
  sampling(dso.gp.sim
           , data=dplist
           , chains=8e0
           , iter=1000
           , warmup=990
           )
samps <- NULL
samps <- extract(gp.sampling)
str(samps)

print(gp.sampling)

traceplot(gp.sampling)

str(samps$y)

df.gp.sim <- NULL
df.gp.sim <- data.frame( 
  l=dplist$x
  ,t(samps$y)
  ) %>% 
  gather( y, value, -l)
str(df.gp.sampling)
qplot( x=l, y=value, data=df.gp.sim, color=y, geom="line", alpha=0.9) +
  theme(legend.position="none")

qplot( x=df$l, y=samps$Sves[,], geom="line")

# }}}

# state optimiztion {{{
toCol <- function (p) {
  txt <- function(i) paste(p,i,"]",sep="")
  cols <- sapply(1:10, txt)
  fit$par[cols] 
}

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

str(samps$Sves)

qplot(x=as.vector(t(samps$Sves[,1,])), y=as.vector(t(samps$MAPKpp[,1,])), geom="jitter") +
geom_jitter( position=position_jitter(width=0.01, height=0.01), alpha=0.01)

qplot(x=as.vector(t(samps$Sves[,1,])), y=as.vector(t(samps$Sves[,2,])), geom="point") +
  geom_abline( intercept=0, slope=1, size=2, color='red')

qplot(x=as.vector(t(samps$MAPKpp[,1,])), y=as.vector(t(samps$MAPKpp[,2,])), geom="point") +
  geom_abline( intercept=0, slope=1, size=2, color='red')

df.Sves <- data.frame(t(samps$Sves[,2,])) %>% 
  mutate(l=df$l) %>% 
    gather( param, Sves, -l ) 
qplot( x=l, y=Sves, data=df.Sves, color=param, geom="line") +
  theme(legend.position="none")

df.MAPKpp <- data.frame(t(samps$MAPKpp[,1,])) %>% 
  mutate(l=df$l) %>% 
    gather( param, MAPKpp, -l ) 
qplot( x=l, y=MAPKpp, data=df.MAPKpp, color=param, geom="line", ylim=c(0,1)) +
  theme(legend.position="none")

df.MI <- data.frame(t(samps$MI)) %>% 
  mutate(l=df$l) %>% 
  gather( param, MI, -l ) %>% 
  rbind( data.frame( l=df$l, param="data", MI=df$MI))
qplot( x=l, y=MI, data=df.MI, color=param, geom="line") +
  theme(legend.position="none")

qplot( x=1:nrow(samps$lp__), y=exp(samps$lp__), geom="line")

qplot( x=samps$b, geom="histogram", binwidth=0.01)

qplot( x=samps$dX, geom="density", xlim=c(0,1)) +
  stat_function(fun=dnorm, arg=list(sd=1e-1), geom="path", color="blue" )

qplot( x=samps$b, geom="density", xlim=c(0,1)) +
  stat_function(fun=dnorm, arg=list(sd=1e-1), geom="path", color="blue" )

qplot( x=samps$b2, geom="density", xlim=c(0,1), fill="#FF6666", alpha=0.2) +
  stat_function(fun=dnorm, arg=list(sd=1e-1), geom="path", color="blue" )

qplot( x=samps$w, geom="density", xlim=c(-2,2)) +
  stat_function(fun=dnorm, arg=list(sd=1e-1), geom="path", color="blue" )

qplot( x=as.vector(samps$MI), geom="density", xlim=c(-0.5,1.5)) + 
  stat_function(fun=dnorm, arg=list(mean=1,sd=df.sigma), geom="path", color="blue" )


summary(samps$dX)

qplot( x=samps$w, y=samps$b )
qplot( x=samps$b, y=samps$b2 )

# }}}

dso.pred.ana <- stan_model( stanc_ret=stanc(file="./gp-predict-analytic.stan") )

# gp-predict-analytic {{{
datalist=list(
              N1=fitlist$N
              , x1=fitlist$x
              , y1=fitlist$y
              , N2=0
              , x2=seq(0,2,0.001)
              , rho=0.5/(0.11)^2
              )
datalist$N2 <- length(datalist$x2)

gp.pred.ana <- NULL
gp.pred.ana <- sampling(dso.pred.ana
                        , data=datalist
                        , chains=8
                        , iter=1e1
                        )
samps <- NULL
samps <- extract(gp.pred.ana)
str(samps)

df.fit <- NULL
df.fit <- data.frame( x=datalist$x2, t(samps$y2) ) %>% 
  gather( y2, value, -x ) 
ggplot( data=df.fit, aes(x=x, y=value)) +
  geom_path(alpha=0.3) +
  geom_point( data=df.biphasic, aes( x=s, y=y), color="red", size=4, alpha=0.5)

df.fit %>% filter( x>0.05, x<0.15 )
# }}}
