import unittest
import scipy.stats as st
from main import *

class UnitTests(unittest.TestCase) :
    def test_distribution(self) : 
        mean = 0
        for i in range(100) :
           ll, val, uu = mean_with_errors(5)
           mean = mean + val
        mean = mean / 100

        var = 1/12
        bar = np.sqrt(var/100)*st.norm.ppf( (0.99 + 1) / 2 )
        self.assertTrue( np.fabs( mean-0.5 )<bar, "your mean appears to be sampled from the wrong distribution" )

  def test_errors(self) : 
      ll, val, uu = mean_with_errors(5)
      self.assertTrue( ll<val and val<uu, "the 5th percentile is less than the mean or the 9th percentile is greater than the mean.  This makes no sense"  )
      self.assertTrue( ((val-ll)-(uu-val))<1e-7, "the percentiles should be the same distance from the mean as the distribution is symmetric" )

  def test_errormag(self) : 
      # Do some resampling
      samples = 100*[0]
      for i in range(100) : 
          samples[i], mean = 0, 0
          for j in range(5) : 
             ll, val, uu = mean_with_errors(5)
             mean = mean + val
             samples[i] = samples[i] + val*val
          mean = mean / 5
          samples[i] = ( 5 / 4 )*( samples[i] / 5 - mean*mean )
  
      samples.sort()
      ll, val, uu = mean_with_errors(5)
      sd = ( val - ll ) / st.norm.ppf(0.05) * np.sqrt(5)
      self.assertTrue( samples[1]<sd*sd and sd*sd<samples[98], "the 5th percentile you have output does not appear to be sampled from the correct distribuion" )
      sd = ( uu - val ) / st.norm.ppf(0.95) * np.sqrt(5)
      self.assertTrue( samples[1]<sd*sd and sd*sd<samples[98], "the 95th percentile you have output does not appear to be sampled from the correct distribuion" )
