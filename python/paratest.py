from multiprocessing import Pool
import numpy
import time

def f( val ):
  a = 0
  print val
  for i in xrange(int(val)):
    a = a + i
  return a

if __name__ == '__main__':
    x = 1e7*numpy.ones((16))
    pool = Pool(processes=16)
    result = pool.map(f, x)
