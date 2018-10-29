#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 15:13:19 2018

@author: martinbensch
"""
import grid_world.grid_world as gw

class rl_dyn_prog:
    def __init__(self):
        self.policy
        
        
if __name__ == '__main__':   
    a = gw.grid()
    # build value function
    idx = 0
    V = [ [0 for n in range(8)] for m in range(8)]
    for m in range(8):
        for n in range(8):
            V[m][n] = n + idx
        idx += 10
    
    q = V[:]
    pi = [ [['r'] for n in range(8)] for m in range(8)]
            
    a.draw_grid_result(pi,value_fct=V,q_fct=q)
