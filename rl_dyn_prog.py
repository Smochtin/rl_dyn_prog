#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 15:13:19 2018

@author: martinbensch
"""
import libs.grid_world.grid_world as gw

class rl_dyn_prog:
    def __init__(self, size=None, terminal_state=None):
        if size is None:
            self.size = (8,8)
        else:
            self.size = size
        
        if terminal_state is None:
            self.terminal_state = [(0,0), (self.size[0]-1, self.size[1]-1)]
        else:
            self.terminal_state = terminal_state
        
        # Create grid object
        self.grid = gw.grid(self.size)
        
        # Initialize arbitrary value function
        self.v_s = self.v_fct_0()
        
        # Current policy
        self.policy = None
    
    def set_policy(self, policy):
        self.policy = policy
    
    def policy_return(self,s,a):
        """Returns the value of current policy for a given state and action pair"""
        # Get current action probability values
        pi_s = self.policy[s[0]][s[1]]
        
        
    def evaluate_policy(self, theta):
        """ Evaluate the current policy """
        " theta is an accuracy parameter "
        delta = 0
        # Iterate as long as delta is greater than theta
        while delta > theta:
             # iterate through all states
             for m in range(0,self.size[0]):
                 for n in range(0,self.size[1]):
                     # current state 
                     s = [m,n]
                     # get current action set from policy
                     actions = ['r','l','u','d']
                     V_s = 0
                     for a in actions:
                         pi_as = self.policy[m][n][a]
                         for s_ in s_prime
                             # Get transition probability
                             p = self.p_s_a(s,a)        
        
    def v_fct_0(self):
        v = [[0 for n in range(self.size[1]) for m in range(self.size[0])]]
        return v
    
    def p_s_a(self,s,a):
        x,y = s
        if x in range(0,self.size[0]) and y in range(0,self.size[1]):
            s_prime_dic = {'r': [x+1, y],
                           'l': [x-1, y],
                           'u': [x, y +1],
                           'd': [x, y -1]
                           }
            s_prime = s_prime_dic[a]
            if s_prime[0] in range(0,self.size[0]) and \
               s_prime[1] in range(0,self.size[1]) and \
               abs(s_prime[0] - x) <= 1.0 and \
               abs(s_prime[1] - y) <= 1.0:
                return 1
            else:
                return 0
             
        else:
            raise Exception("From p_s_a(...): current state isn't on the grid")
    
if __name__ == '__main__':   
  
    
    pi = {'r': .25,
          'l': .25,
          'u': .25,
          'd': .25
          } 
    # build policy
    policy = [[[pi for n in range(self.size[1])] for m in range(self.size[0])]
    
  