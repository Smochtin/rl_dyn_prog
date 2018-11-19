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
            self.size = (8, 8)
        else:
            self.size = size

        if terminal_state is None:
            self.terminal_state = [(0, 0), (self.size[0], self.size[1])]
        else:
            self.terminal_state = terminal_state

        # Create grid object
        self.grid = gw.grid(self.size)

        # Initialize arbitrary value function
        self.V_s = self.v_fct_0()

        # Current policy. Implemented as a grid, where each field is made up
        # of dictionaries. A dictionary looks like
        # {'l':.25, 'r':.25, 'u':.25, 'd':.0.25}
        # for example and represents a discrete distribution.
        self.policy = None

        # Reward
        self.reward = -1

        # Discount rate
        self.gamma = None

    def set_policy(self, policy):
        self.policy = policy

    def set_gamma(self, gamma):
        self.gamma = gamma

    def get_policyDistribution(self, s):
        """Returns the distribution of current policy for a given state
           and action pair"""
        # Get current action probability values
        return self.policy[s[0]][s[1]]

    def evaluat_policy(self, theta):
        """ Evaluate the current policy """
        " theta is an accuracy parameter. "

        if self.policy is None:
            raise Exception('From evaluate_policy(...): policy is None')

        # Iitialize delta
        D = 0
        k = 0
        ts_m, ts_n = self.terminal_state[0]
        ts_m2, ts_n2 = self.terminal_state[1]
        # Iterate as long as delta is greater than theta
        while 1:
            # iterate through all states
           # self.print_V(self.V_s)
            for m in range(0, self.size[0]):
                for n in range(0, self.size[1]):
                    # Check for terminal state
                    if (ts_m == m and ts_n == n) or \
                       (ts_m2-1 == m and ts_n2-1 == n):
                           continue

                    # current state
                    s = [m, n]

                    # Current value of state m,n
                    v = self.V_s[m][n]

                    # Calculate new value for state m,n
                    
                    self.V_s[m][n] = self.calculate_value(s)
                    # Calculate termination critarion
                    D = max(D, abs(v - self.V_s[m][n]))
            k = k + 1
            if D < theta:
                print("D: ", D)
                break
            
            if k > 1000:
                break
            
        print("Evaluated policy and took ", k, "Iterations")

    def print_V(self, v):
        print("--")
        for m in v:
            nl = [round(m_,2) for m_ in m]
            print(nl)
        print("--")

    def v_fct_0(self):
        v = [[0 for n in range(self.size[1])] for m in range(self.size[0])]

        return v

    def reset_v_s(self):
        self.V_s = [[0 for n in range(self.size[1])] for m in range(self.size[0])]
        
    def p_s_a(self, s_prime, s, a):
        """ Transition probability for s to s_prime"""
        "In this scenario the current action 'a' does not matter for p_s_a,"
        "Because all reachable states s' are specified in a list."
        "Therefore this whole function is more obsolete but should remind"
        "on the bellman equation."
        actionDict = {'l' : [0, -1],
                      'r' : [0, 1],
                      'u' : [-1, 0],
                      'd' : [1, 0]
                      }
        actionDir = actionDict[a]
        m, n = s
        m_p, n_p = s_prime

        currentDir = [m - m_p, n_p - n]
        if (currentDir[0] == actionDir[0] and currentDir[1] == actionDir[1]):
            return 1
        else:
            return 0

    def calculate_value(self, s):
        # get current distribution from policy
        distribution = self.get_policyDistribution(s)
        V_s_tmp = 0
        tmp_lst = []
        tmp_lst2 = []
        for a in distribution:
            # First summation in bellman equation (value function)
            # value of pi(a|s)
            pi_as = distribution[a]
            # Possible successor states
            m, n = s
            s_prime = [[m+1, n],
                       [m-1, n],
                       [m, n+1],
                       [m, n-1]]

            # Second sum with p(s',r |s, a) in the bellman equation
            v_s_p = 0
            
            for s_ in s_prime:
                p = self.p_s_a(s_, s, a)
                tmp_lst2.append((s_,s,a))
                
                if (s_[0] not in range(0, self.size[0])) or \
                   (s_[1] not in range(0, self.size[1])):
                        s_ = s
                
                v_s_p = v_s_p +  p * \
                        (self.reward + self.gamma *
                         self.V_s[s_[0]][s_[1]])
                
                tmp_lst.append(self.p_s_a(s_, s, a) * \
                        (self.reward + self.gamma *
                         self.V_s[s_[0]][s_[1]]))
                
            V_s_tmp = V_s_tmp + pi_as * v_s_p

        return V_s_tmp



if __name__ == '__main__':

    size = [4, 4]
    # Build policy
    pi = {'r': .25,
          'l': .25,
          'u': .25,
          'd': .25
          }
    policy = [[pi for n in range(size[1])] for m in range(size[0])]

    # Initilize rl
    rl = rl_dyn_prog(size)
    rl.set_policy(policy)
    rl.set_gamma(1)
    
  #  rl.evaluat_policy(0.1)
  #  print("1st")
  #  rl.print_V(rl.V_s)
    rl.evaluat_policy(0.001)
    print("2nd")
    rl.print_V(rl.V_s)
    rl.v_fct_0()
    rl.evaluat_policy(0.0001)
    print("3rd")
    rl.print_V(rl.V_s)
    rl.v_fct_0()
    print("4th")
    rl.v_fct_0()
    rl.evaluat_policy(0.0001)
    rl.print_V(rl.V_s)
    
