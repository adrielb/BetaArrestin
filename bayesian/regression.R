# libs # {{{
library(gridExtra)
library(ggplot2)
library(dplyr)
library(tidyr)
library(rstan) 
options(dplyr.print_min=45)
# }}}

# data {{{
N <- 40
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

# covariance matrix Sigma # {{{
x <- seq(0,10)/100.
o <- outer(x,x, FUN="-")
S <- exp( -o^2 ) + exp( -o^2*100 )
chol(S)

chol(outer(x,x))

max(S*lower.tri( S ))

tail(x,-1) - head(x,-1) 

library(MASS)

Sigma=matrix(c(
 1,1,
 1,1
 ), 2,2)
qplot( x=X1, y=X2, data=data.frame(mvrnorm( n=10000, mu=c(0,0), Sigma=Sigma)))
chol(Sigma)
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

df.biphasic <- data.frame( s=seq(0,2,0.01) ) 
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
    x=df$l
  , rho_sq = 1e1
  , eta_sq = 1
  , sig_sq = 1e-6
)
dplist$N=length(dplist$x)
print(dplist)

dplist <- list( 
    N=100
  , rho_sq = 1e0
  , eta_sq = 2e-3
  , sig_sq = 1e-8
  , mu = 0.1
  , k1 = 1e7
)
dplist$x=0:(dplist$N-1)/(dplist$N-1)
print(dplist)

with( dplist,
     qplot(c(0, 1)
           , stat = "function"
           , fun=function(x) eta_sq*exp(-rho_sq*(x^2)) 
           , geom = "line"
           , ylim = c(0,eta_sq)
           ) +
     geom_hline( yintercept=eta_sq, size=2, color='red', alpha=0.5) +
     geom_hline( yintercept=sig_sq, size=2, color='blue', alpha=0.5)
)

gp.sampling <- NULL
gp.sampling <- 
  sampling(dso.gp.sim
           , data=dplist
           , chains=8e0
           , iter=220
           , warmup=197
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
qplot( x=l, y=value, data=df.gp.sim, color=y, geom="line", alpha=0.9) +
  theme(legend.position="none")

samps$y %>% sd()

sqrt(200)

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
              , rho=0.5/(7.91)^2
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
ggplot( data=df.fit, aes(x=x, y=value, color=y2)) +
  geom_path(alpha=0.3) +
  geom_point( data=df.biphasic, aes( x=s, y=y), color="red", size=4, alpha=0.5) +
  ylim( 0, 1)

df.fit %>% filter( x>0.05, x<0.15 )
# }}}

dso.pred.sim <- stan_model( stanc_ret=stanc(file="./gp-predict-sim.stan") )

# gp-predict-sim {{{
datalist <- list( 
                x1=c(0.0,2.0)
              , x2=seq(0,2,0.1)
              , rho=0.5/(2.11)^2
              )
datalist$N1 <- length(datalist$x1)
datalist$N2 <- length(datalist$x2)
with( c(datalist, list(eta_sq=1)),
     qplot(c(0,1)
           , stat = "function"
           , fun=function(x) eta_sq*exp(-rho*(x^2)) 
           , geom = "line"
           , ylim = c(0,eta_sq)
           ) +
     geom_hline( yintercept=eta_sq, size=2, color='red', alpha=0.5)
)

gp.pred.sim <- NULL
gp.pred.sim <- sampling(dso.pred.sim
                        , data=datalist
                        , chains=8
                        , iter=1e2
                        , warmup=1e2-1
                        )
samps <- NULL
samps <- extract(gp.pred.sim)
str(samps)
df.samps <- as.data.frame(samps) %>% 
  mutate( sample=factor(1:length(samps$lp__)) ) %>% 
  gather( param, value, -sample) %>% 
  separate( param, into=c("param","idx"), convert=TRUE) %>% 
  mutate( x=0 )
df.samps[df.samps$param=='y1','x'] <- df.samps %>% filter( param=='y1' ) %>% mutate( x=datalist$x1[idx] ) %>% select( x ) 
df.samps[df.samps$param=='y2','x'] <- df.samps %>% filter( param=='y2' ) %>% mutate( x=datalist$x2[idx] ) %>% select( x ) 

df.samps %>% select( param ) %>% distinct()

ggplot( data=df.samps %>% filter( param=='y2' ), aes(x=x, y=value, color=sample)) +
  geom_line( ) + 
  geom_line( data=df.samps %>% filter( param=='y1' ) ) + geom_point( data=df.samps %>% filter( param=='y1' ),  size=4) +
  theme(legend.position="none")

df.fit <- NULL

df.fit1 <- data.frame( x=datalist$x1, t(samps$y1), param=1 ) %>% 
  gather( sample, y, -x, -param ) 

df.fit <- data.frame( x=datalist$x2, t(samps$y2), param=2 ) %>% 
  gather( sample, y, -x, -param )

    rbind(df.fit, df.fit1 )

ggplot( data=df.fit, aes(x=x, y=y2, color=sample)) +
  geom_path(alpha=0.3) +
  geom_point( data=df.biphasic, aes( x=s, y=y), color="red", size=4, alpha=0.5) +
  ylim(-3,3) +
  theme(legend.position="none")

df.fit %>% filter( x>0.05, x<0.15 )
# }}}

dso.gp.barr  <- stan_model( stanc_ret=stanc(file="./gp-barrestin.stan") )

# gp-barr {{{
datalist=list(  N=nrow(df)
              , l=df$l
              , dl=0.001
              , MI_obs=df$MI
              , Sexp=as.integer(df$Expression)
              , sigma=df.sigma
              , SvesMu=dplist$mu
              , rho_sq=dplist$rho_sq
              , eta_sq=dplist$eta_sq
              , sig_sq=dplist$sig_sq
              , dXmin=1e-3
              , dXmax=1e3
              , k1=dplist$k1
              )
print(datalist)
df.l <- with( datalist,
  rbind( data.frame(side=1, idL=1:length(l), l=l),
         data.frame(side=2, idL=1:length(l), l=l+dl) )
)
df.l <- df.l %>% mutate( side=factor(side) )
df.l %>% sample_n(50)

gp.barr <- NULL
gp.barr <- 
  sampling(dso.gp.barr
           , data=datalist
           , chains=8
           , iter=1e2
           , warmup=1e2-10
           )
samps <- NULL
samps <- extract(gp.barr)
str(samps)

df.samps <- NULL
df.samps <- samps %>% as.data.frame() %>% tbl_df() %>%
  mutate( sample=factor(1:length(samps$lp__)) ) %>% 
  gather( param, value, -sample, -dX, -lp__) %>% 
  separate( param, into=c("param","side","idL"), convert=TRUE, extra="merge") %>%
  filter( param!="SvesVec" ) %>%
  filter( param!="z" ) %>% 
  mutate( side=factor(side) )
df.samps[df.samps$param=='MI','idL'] <- df.samps[df.samps$param=='MI','side']
df.samps[df.samps$param=='MI','side'] <- 1
df.samps <- left_join( df.samps, df.l, by=c("side","idL") ) %>% 
  spread( param, value )
MAXSAMPLES <- df.samps$sample %>% as.numeric() %>% max()
# df.samps <- df.samps %>% filter(sample==sample.int(size=1, n=MAXSAMPLES))
df.samps %>% print()
ggSves <- NULL
ggSves <- ggplot( data=df.samps, aes(x=l, y=Sves, color=sample, group=sample )) +
  geom_line(alpha=0.9) +
  # geom_point(aes(alpha=0.1,color=side,shape=side, size=2)) +
  coord_flip() +
  # ylim(0,2.5) +
  theme(legend.position="none")
ggMAPKpp <- NULL
ggMAPKpp <- ggplot( data=df.samps %>% mutate(side=factor(side)), aes(x=l, y=MAPKpp, color=sample )) +
  geom_line(alpha=0.9) +
  # geom_point(aes(alpha=0.1,color=side,shape=side, size=2)) +
  ylim(0,1) +
  theme(legend.position="none")
ggMS <- NULL
ggMS <- ggplot( data=df.samps, aes(x=Sves, y=MAPKpp, color=sample)) +
  geom_line(alpha=0.9) +
  geom_jitter( position=position_jitter(width=0.1, height=0.01)) +
  geom_point() +
  ylim(0,1) +
  theme(legend.position="none")
ggMI <- NULL
ggMI <- ggplot() + 
  geom_line(data=df.samps %>% filter(side==1), aes(x=l, y=MI, color=sample, group=sample  ) ) +
  geom_point( data=df, aes(x=l, y=MI, size=3, group=NULL, color=NULL)) +
  theme(legend.position="none")
grid.arrange( ggMAPKpp, ggMS, ggMI, ggSves, ncol=2)

qplot( x=log10(samps$dX), geom="density", xlim=c(-3,3), fill="black")

qplot( x=log10(samps$dX), geom="bar")

qplot( x=l, y=Sves, data=df.samps, color=side, geom="point")

qplot( data=
      df.samps %>% select( idL, side, Sves) %>% spread( side, Sves) %>% left_join( df.l %>% filter( side==1) %>% select( -side), by="idL" ) %>% arrange( l )
      , x=`1`, y=`2`, geom="path", color=l) +
  geom_abline( intercept=0, slope=1, size=2, color='red', alpha=0.5) +
  geom_point(size=3)

qplot( data=
      df.samps %>% select( idL, side, MAPKpp) %>% spread( side, MAPKpp) %>% left_join( df.l %>% filter( side==1) %>% select( -side), by="idL" ) %>% arrange( l )
      , x=`1`, y=`2`, geom="path", color=l) +
  geom_abline( intercept=0, slope=1, size=2, color='red', alpha=0.5) +
  geom_point(size=3)


qplot( x=l, y=dSves, data=
df.samps %>% select( idL, side, Sves) %>% spread( side, Sves) %>% mutate( dSves=`2` - `1`) %>% left_join( df.l %>% filter( side==1) %>% select( -side), by="idL" ) %>% arrange( l )
      , color=l, geom="line") + geom_point()

qplot( x=l, y=diff, data=
df.samps %>% select( idL, side, MAPKpp) %>% spread( side, MAPKpp) %>% mutate( diff=`2` - `1`) %>% left_join( df.l %>% filter( side==1) %>% select( -side), by="idL" ) %>% arrange( l )
      , color=l, geom="line")

# }}}

