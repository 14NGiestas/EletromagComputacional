from numpy import array
import time

class Point(tuple):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.x = x
        self.y = y

class PaintBucket:
    def __init__(self, sx, sy, N=100, eps=1e-8):
        self.charges = []
        self.size = (sx, sy)
        self.step = (sx/N, sy/N) 
        self.eps  = eps

    def add_charge(self, x, y, q=1):
        '''
        Place a charge at a given position
        Arguments:
            x (float): x coord.
            y (float): y coord.
        '''
        if not self._is_valid_pos(x,y):
            raise ValueError('Charge must be in the mesh!')
        self.charges.append((x,y,q))

    def _potential_at(self, x, y):
        '''
        Calculates the potential at a given point
        Arguments:
            x (float): x coord.
            y (float): y coord.
        Returns:
            potential (float): The potential at given point 
        '''
        if not self._is_valid_pos(x,y):
            raise ValueError('Position must be in the mesh!')
        
        potential = 0
        for charge in self.charges:
            x0, y0, q = charge
            r = ((x-x0)**2 + (y-y0)**2)**0.5
            if r > 0:
                potential +=  q / r
            else:
                break
        return potential

    def _is_valid_pos(self, x, y):
        '''
        Checks if the given position is in the mesh 
        '''
        size_x, size_y = self.size
        step_x, step_y = self.step
        pos_x, pos_y = int(x/step_x), int(y/step_y)
        lim_x, lim_y = int(0.5*size_x/step_x), int(0.5*size_y/step_y)

        return (-lim_x < pos_x < lim_x and
                -lim_y < pos_y < lim_y)

    def _draw_equipotential(self, x, y):
        if not self._is_valid_pos(x,y):
            raise ValueError('Start position must be in the mesh!')

        curve      = []
        visited    = []
        visit_next = []

        N = array((+0,+1))
        S = array((+0,-1))
        E = array((+1,+0))
        W = array((-1,+0))

        directions = [N,N+W,N+E,S,S+W,S+E,E,W] 

        sx, sy = self.step

        V_0 = self._potential_at(x,y)
        start = int(x/sx), int(y/sy)
        visit_next.append(start)

        while True:
        #for _ in range(1000):

            if visit_next:
                i, j = visit_next.pop()
            else:
                break

            # Select valid movements
            valid_moves = [
                (i+di, j+dj)
                for di, dj in directions
                if self._is_valid_pos((i+di)*sx,(j+dj)*sy)
                and (i+di,j+dj) not in visited
            ]
            # Calculates the pot. absolute diff. to all valid moves  
            potential = [
                abs(V_0 - self._potential_at(i*sx,j*sy))
                for i, j in valid_moves
            ] 
            print(potential)

            # Visit next
            visit_next = [
                valid_moves[idx]
                for idx, val in enumerate(potential)
                if val < 0.16
            ]
            print(visit_next)

            curve.append((i*sx,j*sy))
            visited += visit_next
        return curve, V_0

    def show(self):
        import numpy as np
        import matplotlib.pyplot as plt
        # plt.style.use('seaborn')

        size_x, size_y = self.size
        pts, V0 = self._draw_equipotential(0.5, 0.0)
        pts = np.array(pts)
        x = pts[:,0]
        y = pts[:,1]
        plt.scatter(x,y)
        plt.show()
