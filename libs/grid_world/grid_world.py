#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 21:32:50 2018

@author: martinbensch
"""
import matplotlib.pyplot as plt

class grid:
    def __init__(self, size=None):
        if size is None:
            self.size = (8,8)
        else:
            self.size = size

    def draw_grid_result(self,policy, value_fct=None, q_fct=None):
        """ Gets policy and visualizes it"""
        " policy,value_fct and q_fct are 2-dim lists. An entry of the policy"
        "consists of a discrete probability distribution"
        "value_fct and q_fct are just matrices."
        if len(policy[0]) == self.size[1] and len(policy) == self.size[1]:
            #Step through all fields
            self.build_grid()
            # step through all policy rows
            for m in range(len(policy)):
                # step through all policy columns
                for n in range(len(policy[0])):
                    # draw direction from policy
                    x,y, direction = m,n,policy[m][n]
                    for d in direction:
                        self.draw_dir([x,y],d)

            if not (value_fct is None):
                # step through all value rows
                for m in range(len(value_fct)):
                    # step through all policy columns
                    for n in range(len(value_fct[0])):
                        # draw direction from policy
                        x,y, v = m,n,value_fct[m][n]
                        self.draw_txt([x,y],v,'v')

            if not (q_fct is None):
                # step through all value rows
                for m in range(len(q_fct)):
                    # step through all policy columns
                    for n in range(len(q_fct[0])):
                        # draw direction from policy
                        x,y, q = m,n,q_fct[m][n]
                        self.draw_txt([x,y],q,'q')
            plt.axis('equal')
            s = 'v values in upper left corner, q values in lower left corner'
            plt.text(-0.5,self.size[1],s)
            plt.show()
        else:
            raise Exception('From draw_grid_result(...): policy dimension \
                            may be unequal to grid dimension')



    def build_grid(self):
        """ Build a (n,n) grid with matplotlip """
        print(self.size)
        # Build horizontal lines
        # x coorinates list  is a tupel (0,1)
        h_lines = [[n-.5,n-.5] for n in range(self.size[0]+1)]
        for l in h_lines:
            plt.plot([-.5,self.size[1]+.5-1],l,'black')
        # Build vertical lines
        # y coordinates list is tupel (0,1)
        v_lines = [[n-.5,n+.5] for n in range(self.size[1]+1)]
        for l in h_lines:
            plt.plot(l,[-.5,self.size[0]+.5-1],'black')

    def draw_txt(self,cords, value, f):
        """Draw text to fields"""
        "Third argument specifies if it is the value of a value-function or "
        "of the action-value-function. State values are printed to the upper"
        "left corner of a field while an action-value is printed to the lower"
        "right corner. f: 'v' or 'q'"
        if  (cords[0] in range(0,self.size[0])) and \
            (cords[1] in range(0,self.size[1])) and \
            (f in ['v', 'q']):
                if f == 'v':
                    x = cords[0] - 0.4
                    y = cords[1] + 0.25
                    plt.text(x, y,str(value),fontsize=6)
                elif f == 'q':
                    x = cords[0] - 0.4
                    y = cords[1] - 0.35
                    plt.text(x, y,str(value),fontsize=6)
                else:
                    raise Exception('From draw_tx(...): function type not \
                                    specified.')
        else:
            raise Exception('From draw_txt(...): cords may be out of grid range')


    def draw_dir(self,cords, direction):
        """Draws an direction to the grid"""
        " Cords is the field tupel and direction is a character r,l,u,d "
        x_dir = {
                'l': self.l_dir,
                'r': self.r_dir,
                'u':self.up_dir,
                'd':self.dw_dir,
                }

        if  (cords[0] in range(0,self.size[0])) and \
            (cords[1] in range(0,self.size[1])) and \
            (direction in ['l','r','u','d']):
                x_dir[direction](cords)
        else:
            raise Exception('From draw_arrow(...): cords out of grid range')


    def l_dir(self, cords):
        x,y = cords
        x_l, y_l = x - 0.4, y
        plt.plot([x,x_l],[y,y_l],'b')
        #plt.show()

    def r_dir(self,cords):
        x,y = cords
        x_l, y_l = x + 0.4, y
        plt.plot([x,x_l],[y,y_l],'r')
        #plt.show()

    def up_dir(self,cords):
        x,y = cords
        x_l, y_l = x, y+0.4
        plt.plot([x,x_l],[y,y_l],'orange')
        #plt.show()

    def dw_dir(self,cords):
        x,y = cords
        x_l, y_l = x, y-0.4
        plt.plot([x,x_l],[y,y_l],'green')
        #plt.show()


if __name__ == '__main__':
    a = grid()
    # build value function
    idx = 0
    V = [ [0 for n in range(8)] for m in range(8)]
    for m in range(8):
        for n in range(8):
            V[m][n] = n + idx
        idx += 10

    q = V[:]
    pi = [ [['r','u'] for n in range(8)] for m in range(8)]

    a.draw_grid_result(pi,value_fct=V,q_fct=q)
