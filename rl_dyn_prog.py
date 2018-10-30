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
        self.V_s = self.v_fct_0()
        
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
                         # policy for current state
                         pi_as = self.policy[m][n][a]
                         # Possible successor states
                         s_prime = [[m+1,n],
                                    [m-1,n],
                                    [m,n+1],
                                    [m,n-1]]
                         # Second sum with p_s_a in the bellman equation
                         v_s_p = 0 
                         for s_ in s_prime
                             # Get transition probability
                             m_,n_ = s_
                             p = self.p_s_a(s_,s,a)
                             v_s_prime = self.V_s[m_][n_]
                             v_s_p = v_s_p + p * (self.r + self.gamma * v_s_prime)
        
    def v_fct_0(self):
        v = [[0 for n in range(self.size[1]) for m in range(self.size[0])]]
        return v
    
    def p_s_a(self,s_prime,s,a):
        """ Transition probability for s to s_prime"""
        "In this scenario the current action 'a' does not matter for p_s_a,"
        "Because all reachable states s' are specified in a list." 
        "Therefore this whole function is more obsolete but should remind,"
        "on the bellman equation."
        
        x,y = s
        x_p, y_p = s_prime
        if (abs(x-x_p) <= 1.0 and abs(y-y_p) <= 1.0):
            return 1
        else:
            return 0
        
if __name__ == '__main__':   
  
    
    pi = {'r': .25,
          'l': .25,
          'u': .25,
          'd': .25
          } 
    # build policy
    policy = [[[pi for n in range(self.size[1])] for m in range(self.size[0])]
    
  