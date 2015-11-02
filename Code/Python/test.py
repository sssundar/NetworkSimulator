# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 21:25:33 2015

@author: Sith
"""

class Test:
    val = 0
    def __init__(self):
        self.val = []
    def append(self, m):
        self.val.append(m)
    def getval(self):
        return self.val