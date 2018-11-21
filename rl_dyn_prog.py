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
    
    def policy_iteration(self,theta):
        policy_stable = False
        
        while not policy_stable:
            self.evaluat_policy(theta)
            self.grid.draw_grid_result(self.policy, self.V_s)
            policy_stable = self.policy_improvement()
            
            
        self.grid.draw_grid_result(self.policy, self.V_s)
        print(self.policy)

    def evaluat_policy(self, theta):
        """ Evaluate the current policy """
        " theta is an accuracy parameter. "

        if self.policy is None:
            raise Exception('From evaluate_policy(...): policy is None')

        # Iitialize delta
        k = 0
        ts_m, ts_n = self.terminal_state[0]
        ts_m2, ts_n2 = self.terminal_state[1]
        # Iterate as long as delta is greater than theta
        while 1:
            # iterate through all states
            # self.print_V(self.V_s)
            D = 0
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
                    
                    self.V_s[m][n] = round(self.calculate_value(s),2)
                    # Calculate termination critarion
                    #print(self.V_s[m][n], v, abs(v - self.V_s[m][n]))
                    D = max(D, abs(v - self.V_s[m][n]))
            k = k + 1
            if abs(D) < theta:
                print("D: ", D)
                break

            if k > 1000:
                print("D: ", D)
                break
        print("Evaluated policy, took ", k, "Iterations")

    def policy_improvement(self):
        """ Improve policy """
        
        policy_stable = True

        # For each state
        for m in range(0, self.size[0]):
            for n in range(0, self.size[1]):
                old_action = self.policy[m][n]
                s = [m, n]
                self.policy[m][n] = self.best_action(s)
                if old_action != self.policy[m][n]:
                    policy_stable = False
        print("Improved policy")
        if policy_stable:
            print("Policy is stable")
            return True
        else:
            print("Policy is unstable")
            return False
        
    def best_action(self,s):
        m,n = s
        ts_m, ts_n = self.terminal_state[0]
        ts_m2, ts_n2 = self.terminal_state[1]
        actionDict = { (0, -1) : 'l',
                       (0, 1) : 'r' ,
                       (-1, 0) : 'u',
                       (1, 0) : 'd'  
                      }
        # Run through all possible successor states:
        m, n = s
        s_prime = [[m+1, n],
                   [m-1, n],
                   [m, n+1],
                   [m, n-1]]
        action_list = []
        for s_ in s_prime:
            if (s_[0] in range(0, self.size[0])) and \
               (s_[1] in range(0, self.size[1])) and \
               not ((ts_m == m and ts_n == n) or \
                    (ts_m2-1 == m and ts_n2-1 == n)):
                    action_list.append([self.V_s[s_[0]][s_[1]], s_])
        
        if action_list is None:
            print("From best_action(..), action_list is None")
            
        # Sort action_list
        if len(action_list) > 1:
            action_list.sort(key=lambda elem: elem[0], reverse=True)
            for idx, a in enumerate(action_list[1:]):
                if a[0] < action_list[idx][0]:
                    action_list = action_list[0:idx+1]
                    break
        
        actions = dict()
        if len(action_list) > 0:
            value = 1 / len(action_list)
            for al in action_list:
                s_ = al[1]
                m_p, n_p = s_
                tmp_dic = {actionDict[(m_p - m, n_p - n)] : value}
                actions.update(tmp_dic)
            
        return actions

        
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

        currentDir = [m_p - m, n_p - n]
        if (currentDir[0] == actionDir[0] and currentDir[1] == actionDir[1]):
            return 1
        else:
            return 0

    def calculate_value(self, s):
        # get current distribution from policy
        distribution = self.get_policyDistribution(s)
        V_s_tmp = 0
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

                if (s_[0] not in range(0, self.size[0])) or \
                   (s_[1] not in range(0, self.size[1])):
                        s_ = s
                
                v_s_p = v_s_p +  p * \
                        (self.reward + self.gamma *
                         self.V_s[s_[0]][s_[1]])
                
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
    
    print("1st")
    rl.policy_iteration(1)
    rl.print_V(rl.V_s)
    rl.reset_v_s()
#    
#    print("2nd")
#    rl.evaluat_policy(0.1)
#    rl.print_V(rl.V_s)
#    rl.reset_v_s()
#    
#    print("3rd")
#    rl.evaluat_policy(0.0001)
#    rl.print_V(rl.V_s)
#    rl.reset_v_s()
#    
#
#    print("4th")    
#    rl.evaluat_policy(0.0001)
#    rl.print_V(rl.V_s)
##    
