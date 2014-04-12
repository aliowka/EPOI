'''
Created on Apr 12, 2014

@author: aliowka
'''
import time
import unittest

class Test(unittest.TestCase):

    precomputed = {}

    def precompute(self):
         
        if len(self.precomputed):
            return
 
        for i in xrange(1 << 16):
            self.precomputed[i] = self.parity_1(i)
 
    def get_last_set_bit(self, x):
        return x & ~(x - 1)
     
    def drope_last_set_bit(self, x):
        return x & (x - 1)
             
    def parity_1(self, x):
 
        parity = 0
 
        while x:
            x = x & (x - 1)
            parity = parity ^ 1
        return parity
 
    def parity_2(self, x):
        return self.precomputed[x & 0b1111111111111111] ^ \
            self.precomputed[(x >> 16) & 0b1111111111111111] ^ \
            self.precomputed[(x >> 32) & 0b1111111111111111] ^ \
            self.precomputed[(x >> 48) & 0b1111111111111111]
 
    def test_parity_1(self):
        self.assertEqual( self.parity_1(0b1),     1 )
        self.assertEqual( self.parity_1(0b11),    0 )
        self.assertEqual( self.parity_1(0b101),   0 )
        self.assertEqual( self.parity_1(0b111),   1 )
        self.assertEqual( self.parity_1(0b1101),  1 )
 
    def test_parity_2(self):
        self.precompute()
        for i in [0, 1, 2, 3, 65323, 4323321, 1241241243]:
            self.assertEqual(self.parity_1(i), self.parity_2(i))
 
    def test_timeit(self):
  
        self.precompute()
         
        st = time.time()
        for i in xrange(1<<20):
            self.parity_1(i)
        print "Raw parity", time.time() - st
        st = time.time()
        for i in xrange(1<<20):
            self.parity_2(i)
        print "Cached parity", time.time() - st
         
    def swap_bits(self, x, i, j):
        
        if (x >> i) & 1 == (x >> j) & 1:
            return x
        
        x = x ^ (1 << i)
        x = x ^ (1 << j)
        return x
        
    def test_swap_bits(self):
        self.assertEqual(self.swap_bits(0b10101, 1, 0), 0b10110)
        self.assertEqual(self.swap_bits(0b10101, 2, 0), 0b10101)
        self.assertEqual(self.swap_bits(0b10101, 2, 3), 0b11001)
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testParity']
    unittest.main()
