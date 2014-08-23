'''
Created on Apr 12, 2014

@author: aliowka
'''
import time
import unittest
import math
import random

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
        self.assertEqual(self.parity_1(0b1), 1)
        self.assertEqual(self.parity_1(0b11), 0)
        self.assertEqual(self.parity_1(0b101), 0)
        self.assertEqual(self.parity_1(0b111), 1)
        self.assertEqual(self.parity_1(0b1101), 1)
 
    def test_parity_2(self):
        self.precompute()
        for i in [0, 1, 2, 3, 65323, 4323321, 1241241243]:
            self.assertEqual(self.parity_1(i), self.parity_2(i))
 
    def test_timeit(self):
  
        self.precompute()
         
        st = time.time()
        for i in xrange(1 << 20):
            self.parity_1(i)
        print "Raw parity", time.time() - st
        st = time.time()
        for i in xrange(1 << 20):
            self.parity_2(i)
        print "Cached parity", time.time() - st
         
    def swap_bits(self, x, i, j):
        
        if (x >> i) & 1 == (x >> j) & 1:
            return x
        
        x ^= (1 << i) | (1 << j)
        return x
        
    def test_swap_bits(self):
        self.assertEqual(self.swap_bits(0b10101, 1, 0), 0b10110)
        self.assertEqual(self.swap_bits(0b10101, 2, 0), 0b10101)
        self.assertEqual(self.swap_bits(0b10101, 2, 3), 0b11001)

    def reverse_bits_with_shift(self, x):
        res = 0
        for i in xrange(65):
            bit = x & 1
            x >>= 1
            res = (res << 1) + bit
        return res
        
    def reverse_bits_with_swap(self, x):
        for i in xrange(32):
            x = self.swap_bits(x, i, 64 - i)
        return x
        
    def reverse_bits_with_log(self, x):
        res = 0
        while x:
            bit = x & ~(x - 1)
            x = x & (x - 1)
            offset = 64 - int(math.log(bit, 2))
            res |= (1 << offset)
        return res
        
    def test_reverse_bit(self):
        self.assertEqual(self.reverse_bits_with_shift(1), 2 ** 64)
        self.assertEqual(self.reverse_bits_with_shift(2), 2 ** 63)
        self.assertEqual(self.reverse_bits_with_swap(1), 2 ** 64)
        self.assertEqual(self.reverse_bits_with_swap(2), 2 ** 63)
        self.assertEqual(self.reverse_bits_with_log(1), 2 ** 64)
        self.assertEqual(self.reverse_bits_with_log(2), 2 ** 63)
        
        for i in xrange(100):
            x = random.randint(0, 2 ** 63)
            self.assertEqual(self.reverse_bits_with_log(x) ==\
                             self.reverse_bits_with_shift(x) ==\
                             self.reverse_bits_with_swap(x), True)
        
        bulk_size = 10000

        st = time.time()
        for i in xrange(bulk_size):
            self.reverse_bits_with_shift(random.randint(0, 2 ** 63))
        print "Reverse bits with shift:", (time.time() - st)

        st = time.time()
        for i in xrange(bulk_size):
            self.reverse_bits_with_swap(random.randint(0, 2 ** 63))
        print "Reverse bits with swap:", (time.time() - st)

        st = time.time()
        for i in xrange(bulk_size):
            self.reverse_bits_with_log(random.randint(0, 2 ** 63))
        print "Reverse bits with log:", (time.time() - st)
        

        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testParity']
    unittest.main()
