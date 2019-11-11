import numpy as np
import math

class Mesh:
    def __init__(self, m=100, n=100):
        # Attributes (Parameters)
        self._dim = [m, n] # Dimension [m, n]
        self._updateOriginPos()
        self._elem = [] # Actived (non-zero values) elements of mesh

    @property
    def scale(self):
        (x_scale, y_scale) = self._scale
        (x_min, x_sup) = x_scale
        (y_min, y_sup) = y_scale

        return self._scale

    @scale.setter
    def scale(self, scale):
        (x_scale, y_scale) = scale
        (x_inf, x_sup) = x_scale
        (y_inf, y_sup) = y_scale

        if (x_sup - x_inf) > 0 and (y_sup - y_inf) > 0:
            self._scale = scale
            self._updateUnit()
        else:
            raise ValueError('The followed rules must be satisfied: x_sup > x_inf and y_sup > y_inf')

    def squareScale(self, l_side):
        if l_side > 0:
            self.scale = [[-l_side, l_side], [-l_side, l_side]]

    def rectScale(self, lx_side, ly_side):
        if l_side > 0:
            self.scale = [[-lx_side, lx_side], [-ly_side, ly_side]]

    @property
    def dim(self):
        (m, n) = self._dim
        return self._dim

    @dim.setter
    def dim(self, dim):
        (m, n) = dim

        if m > 0 and n > 0:
            self._dim = dim
            self._updateUnit()
            self._updateOriginPos()
        else:
            raise ValueError('The dimensions m and n (dim = [m, n]) must be positive numbers')

    @property
    def unit(self):
        (x_unit, y_unit) = self._unit
        return self._unit

    @unit.setter
    def unit(self, unit):
        (x_unit, y_unit) = unit

        if x_unit > 0 and y_unit > 0:
            self._unit = unit 

            m = math.ceil((self.scale[0][1] - self.scale[0][0]) / self.unit[0]) + 1
            n = math.ceil((self.scale[1][1] - self.scale[1][0]) / self.unit[1]) + 1

            self._dim = [m, n]
            self._updateOriginPos()
        else:
            raise ValueError('The units x_unit and y_unit (unit = [x_unit, y_unit]) must be positive numbers')

    def _updateUnit(self):
        x_unit = (self.scale[0][1] - self.scale[0][0]) / self.dim[0]
        y_unit = (self.scale[1][1] - self.scale[1][0]) / self.dim[1]
        self._unit = [x_unit, y_unit]

    def _updateOriginPos(self):
        j_p0 = math.ceil(self._dim[0] / 2)
        i_p0 = math.ceil(self._dim[1] / 2)
        self._p0 = (i_p0, j_p0)

    def getMeshArr(self):
        meshArr = np.zeros(self.dim)
        
        for a in self._elem:
            meshArr[a[0]][a[1]] = a[2]
        
        return meshArr

    # Position Coordinate in Mesh
    def posCoord(self, r):
        (x, y) = r
        p = list(self._p0)

        for i, ri in enumerate(r):
            if ri > self.scale[i][1] or ri < self.scale[i][0]:
                raise ValueError('Position out of range')
            else:
                if ri < 0:
                    while p[i] > 0:
                        if ri >= (p[i] - self._p0[i])*self.unit[i]:
                            break
                        else:
                            p[i] -= 1
                else:
                    while p[i] < self.dim[i]:
                        if ri <= (p[i] - self._p0[i])*self.unit[i]:
                            break
                        else:
                            p[i] += 1

        return [p[1], p[0]]

    def clear(self):
        self._elem = []

class MeshEE(Mesh):
    def __init__(self, m=100, n=100):
        Mesh.__init__(self, m, n)

        # Number of charges that produce 1 volt to 1 meter of distance
        self._chargeUnit = 694461548.1 # coulombs

        self._mapPts = []
        self._charges = []
        self._cycleStoppingRegion = 1
        self._elem = []
        self.ptLen = 1
        self._horSym = 0
        self._verSym = 0

    @property
    def mapPts(self):
        return self._mapPts

    @property
    def charges(self):
        return self._charges

    @property
    def cycleStoppingRegion(self):
        return self._cycleStoppingRegion

    @cycleStoppingRegion.setter
    def cycleStoppingRegion(self, s):
        if s > 0:
            self._cycleStoppingRegion = s
    
    @property
    def ptLen(self):
        return self._ptLen
    
    @ptLen.setter
    def ptLen(self, ptLen):
        if ptLen >= 1:
            self._ptLen = int(ptLen)

    def getNumPts(self):
        return len(self._elem)

    def addCharge(self, x, y, q):
        charge = [x, y, q]
        if x <= self.scale[0][1] and x >= self.scale[0][0]:
            if y <= self.scale[1][1] and y >= self.scale[1][0]:
                if q > 0 or q < 0:
                    self._charges.append([x, y, q])
                else:
                    raise ValueError('q must be non-zero value')
            else:
                raise ValueError('y position must be into scale')
        else:
            raise ValueError('x position must be into scale')

    def potential(self, i, j):
        V = 0

        for c in self.charges:
            dx = ((j - self._p0[1])*self.unit[1] - c[0])
            dy = ((i - self._p0[0])*self.unit[0] - c[1])
            d = math.sqrt(dx**2 + dy**2)
            if d > 0: V += c[2] / d
            else: V = 0; break
        return V

    def heatmapArr(self):
        mesh = np.zeros(self.dim)

        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                mesh[i][j] = self.potential(i, j)

        return np.array(mesh)

    def horSym(self, act, antsym=False):
        if act:
            if antsym == True: self._horSym = -1
            else: self._horSym = 1
        else:
            self._horSym = 0

    def verSym(self, act, antsym=False):
        if act:
            if antsym == True: self._verSym = -1
            else: self._verSym = 1
        else:
            self._verSym = 0

    def mapPtsLines(self, delta_i=0, delta_j=0):
        sr = self.cycleStoppingRegion

        if self._horSym > 0 or self._horSym < 0:
            i_dim = (math.ceil(self.dim[0]/2))
        else: i_dim = self.dim[0]

        if self._verSym > 0 or self._verSym < 0:
            j_dim = (math.ceil(self.dim[1]/2)) 
        else: j_dim = self.dim[1]

        if delta_i > 0:
            ref_i = 1

            while ref_i < (i_dim - 2):
                checkPos = True

                for c in self.charges:
                    i_c, j_c = self.posCoord((c[0], c[1]))
                    mapPt = [ref_i, self._p0[1]]

                    if mapPt[0] < (i_c + sr) and \
                    mapPt[0] > (i_c - sr) and \
                    mapPt[1] < (j_c + sr) and \
                    mapPt[1] > (j_c - sr):
                        checkPos = False        
                    
                if checkPos:
                    if mapPt[0] < i_dim and mapPt[1] < j_dim:
                        self._mapPts.append(mapPt)

                ref_i += int(delta_i)

        if delta_j > 0:
            ref_j = 1

            while ref_j < (j_dim - 2):
                checkPos = True

                for c in self.charges:

                    i_c, j_c = self.posCoord((c[0], c[1]))
                    mapPt = [self._p0[0], ref_j]

                    if mapPt[0] < (i_c + sr) and \
                    mapPt[0] > (i_c - sr) and \
                    mapPt[1] < (j_c + sr) and \
                    mapPt[1] > (j_c - sr):
                        checkPos = False        
                    
                if checkPos:
                    if mapPt[0] < i_dim and mapPt[1] < j_dim:
                        self._mapPts.append(mapPt)
                ref_j += int(delta_j)

    def trace(self, pt, side):
        i, j = pt # Initial Point
        ref_pt = [i, j] # Reference Point
        last_pt = [i, j] # Last Point
        pts_ctr = 0 # Points Counter
        sr = self.cycleStoppingRegion
        lim_pts = int(1e4)
        V0 = self.potential(pt[0], pt[1])

        if self._horSym > 0 or self._horSym < 0:
            i_dim = (math.ceil(self.dim[0]/2))
        else: i_dim = self.dim[0]

        if self._verSym > 0 or self._verSym < 0:
            j_dim = (math.ceil(self.dim[1]/2)) 
        else: j_dim = self.dim[1]
        
        meshBorder = False
        stoppingCond = False
        checkChargePt = True

        for c in self.charges:
            pos = self.posCoord([c[0], c[1]])

            if i < (pos[0] + sr) and i > (pos[0] - sr) \
            and j < (pos[1] + sr) and j > (pos[1] - sr):
                checkChargePt = False

        if checkChargePt:
            self._elem.append([pt[0], pt[1], V0])

            while (not meshBorder) and (not stoppingCond) and (pts_ctr < lim_pts):
                pts = []
                for di in range(-1,2):
                    for dj in range(-1,2):

                        if not((dj == 0) and (di == 0)):
                            ref_pt[0] += di
                            ref_pt[1] += dj

                            if not ((pts_ctr > 0) and (ref_pt[0] == last_pt[0]) and (ref_pt[1] == last_pt[1])):
                                Vf = self.potential(ref_pt[0], ref_pt[1])
                                pts.append([abs(Vf - V0), int(ref_pt[0]), int(ref_pt[1])])

                            ref_pt[0] -= di
                            ref_pt[1] -= dj
                
                pts.sort()

                if side == 1 or pts_ctr > 0:
                    aux_pt = pts[0]
                elif side == -1:
                    aux_pt = pts[1]

                if aux_pt[1] > (i_dim - 1) or aux_pt[2] > (j_dim - 1) or aux_pt[1] < 0 or aux_pt[2] < 0:
                    meshBorder = True
                    break
                elif aux_pt[1] <= (i + sr) and aux_pt[1] >= (i - sr) and aux_pt[2] <= (j + sr) and aux_pt[2] >= (j - sr) and pts_ctr > sr:
                    stoppingCond = True
                    break
                else:
                    for m in range(self._ptLen):
                        for n in range(self._ptLen):
                            if (aux_pt[1] + m) < i_dim and (aux_pt[2] + n) < j_dim:
                                self._elem.append([aux_pt[1]+m, aux_pt[2]+n, V0])
                    last_pt = list(ref_pt)
                    ref_pt = [aux_pt[1], aux_pt[2]]
                    pts_ctr += 1

    def drawEquip(self, pt):
        self.trace(pt, 1)
        self.trace(pt, -1)

    def drawAllEquip(self):
        for pt in self._mapPts:
            self.drawEquip(pt)

        if self._horSym > 0 or self._horSym < 0:
            symElem = []
            for e in self._elem:
                if e[0] < self._p0[0]:
                    symElem.append([self.dim[0] - e[0] - 1, e[1], self._horSym*e[2]])

            for e in symElem:
                self._elem.append(e)

        if self._verSym > 0 or self._verSym < 0:
            symElem = []
            for e in self._elem:
                if e[1] < self._p0[1]:
                    symElem.append([e[0], self.dim[1] - e[1] - 1, self._verSym*e[2]])

            for e in symElem:
                self._elem.append(e)

    def clear(self):
        Mesh.clear(self)
        self._mapPts = []

    def clearCharges(self):
        self.clear()
        self._charges = []