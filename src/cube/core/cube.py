from .helper import parseFormula
import copy

class Cube:
    """
    An object which models a Rubik's cube and can be moved using formulas that follow the standard cube representation.

    Parameters
    ----------
    faces : string, default="None"
        Set the initial state of the cube to a specific cube faces matrix array.

    Attributes
    ----------
    cube : list of size (6, 3, 3)
        The internal cube faces matrix array for the cube object.
    
    Example
    -------
    >>> cb = Cube()
    >>> cb.doMoves("RUR'U'")
    >>> print(cb)
        YYR
        YYG
        YYG
    BRR GGW OOY BOO
    RRR GGY BOO BBB
    RRR GGG YOO BBB
        WWO
        WWW
        WWW
    """
    
    def __init__(self, faces = "None"):
        self.orientation = [[5, 1, 4, 3], [5, 2, 4, 0], [5, 3, 4, 1], [5, 0, 4, 2], [0, 1, 2, 3], [2, 1, 0, 3]]
        self.rotmap = [[[2, 0], [2, 1], [2, 2], [0, 0], [1, 0], [2, 0], [0, 2], [0, 1], [0, 0], [2, 2], [1, 2], [0, 2]], [[2, 2], [1, 2], [0, 2], [0, 0], [1, 0], [2, 0], [2, 2], [1, 2], [0, 2], [2, 2], [1, 2], [0, 2]], [[0, 2], [0, 1], [0, 0], [0, 0], [1, 0], [2, 0], [2, 0], [2, 1], [2, 2], [2, 2], [1, 2], [0, 2]], [[0, 0], [1, 0], [2, 0], [0, 0], [1, 0], [2, 0], [0, 0], [1, 0], [2, 0], [2, 2], [1, 2], [0, 2]], [[2, 0], [2, 1], [2, 2], [2, 0], [2, 1], [2, 2], [2, 0], [2, 1], [2, 2], [2, 0], [2, 1], [2, 2]], [[0, 2], [0, 1], [0, 0], [0, 2], [0, 1], [0, 0], [0, 2], [0, 1], [0, 0], [0, 2], [0, 1], [0, 0]]]
        self.sideTocmap = ["G", "O", "B", "R", "W", "Y"]
        if(faces == "None"):
            self.cube = [[[self.sideTocmap[c]] * 3 for _ in range(3)] for c in range(6)]
        else:
            self.cube = faces

    def __str__(self):
        pstr = ""
        for i in range(3):
            pstr += "    "
            for j in range(3):
                pstr += self.cube[5][i][j]
            pstr += "\n"
        for i in range(3):
            for j in range(3):
                pstr += self.cube[3][i][j]
            pstr += " "
            for j in range(3):
                pstr += self.cube[0][i][j]
            pstr += " "
            for j in range(3):
                pstr += self.cube[1][i][j]
            pstr += " "
            for j in range(3):
                pstr += self.cube[2][i][j]
            pstr += "\n"
        for i in range(3):
            pstr += "    "
            for j in range(3):
                pstr += self.cube[4][i][j]
            if(i != 2):
                pstr += "\n"
        return pstr

    def __rotateClock(self, side):
        temp = [self.cube[side][0][1], self.cube[side][0][2]]
        self.cube[side][0][1] = self.cube[side][1][0]
        self.cube[side][0][2] = self.cube[side][0][0]
        self.cube[side][0][0] = self.cube[side][2][0]
        self.cube[side][1][0] = self.cube[side][2][1]
        self.cube[side][2][0] = self.cube[side][2][2]
        self.cube[side][2][1] = self.cube[side][1][2]
        self.cube[side][1][2] = temp[0]
        self.cube[side][2][2] = temp[1]
        temp = [self.cube[self.orientation[side][0]][self.rotmap[side][0][0]][self.rotmap[side][0][1]], self.cube[self.orientation[side][0]][self.rotmap[side][1][0]][self.rotmap[side][1][1]], self.cube[self.orientation[side][0]][self.rotmap[side][2][0]][self.rotmap[side][2][1]]]
        for i in range(3):
            self.cube[self.orientation[side][0]][self.rotmap[side][0 + i][0]][self.rotmap[side][0 + i][1]] = self.cube[self.orientation[side][3]][self.rotmap[side][9 + i][0]][self.rotmap[side][9 + i][1]]
            self.cube[self.orientation[side][3]][self.rotmap[side][9 + i][0]][self.rotmap[side][9 + i][1]] = self.cube[self.orientation[side][2]][self.rotmap[side][6 + i][0]][self.rotmap[side][6 + i][1]]
            self.cube[self.orientation[side][2]][self.rotmap[side][6 + i][0]][self.rotmap[side][6 + i][1]] = self.cube[self.orientation[side][1]][self.rotmap[side][3 + i][0]][self.rotmap[side][3 + i][1]]
            self.cube[self.orientation[side][1]][self.rotmap[side][3 + i][0]][self.rotmap[side][3 + i][1]] = temp[0 + i]

    def __rotateAntiClock(self, side):
        temp = [self.cube[side][0][1], self.cube[side][0][2]]
        self.cube[side][0][1] = self.cube[side][1][2]
        self.cube[side][0][2] = self.cube[side][2][2]
        self.cube[side][1][2] = self.cube[side][2][1]
        self.cube[side][2][2] = self.cube[side][2][0]
        self.cube[side][2][0] = self.cube[side][0][0]
        self.cube[side][2][1] = self.cube[side][1][0]
        self.cube[side][0][0] = temp[1]
        self.cube[side][1][0] = temp[0]
        temp = [self.cube[self.orientation[side][0]][self.rotmap[side][0][0]][self.rotmap[side][0][1]], self.cube[self.orientation[side][0]][self.rotmap[side][1][0]][self.rotmap[side][1][1]], self.cube[self.orientation[side][0]][self.rotmap[side][2][0]][self.rotmap[side][2][1]]]
        for i in range(3):
            self.cube[self.orientation[side][0]][self.rotmap[side][0 + i][0]][self.rotmap[side][0 + i][1]] = self.cube[self.orientation[side][1]][self.rotmap[side][3 + i][0]][self.rotmap[side][3 + i][1]]
            self.cube[self.orientation[side][1]][self.rotmap[side][3 + i][0]][self.rotmap[side][3 + i][1]] = self.cube[self.orientation[side][2]][self.rotmap[side][6 + i][0]][self.rotmap[side][6 + i][1]]
            self.cube[self.orientation[side][2]][self.rotmap[side][6 + i][0]][self.rotmap[side][6 + i][1]] = self.cube[self.orientation[side][3]][self.rotmap[side][9 + i][0]][self.rotmap[side][9 + i][1]]
            self.cube[self.orientation[side][3]][self.rotmap[side][9 + i][0]][self.rotmap[side][9 + i][1]] = temp[0 + i]

    def __rotateMidClock(self, type):
        if(type == 'E'):
            temp = [self.cube[0][1][0], self.cube[0][1][1], self.cube[0][1][2]]
            for i in range(3):
                self.cube[0][1][0 + i] = self.cube[3][1][0 + i]
                self.cube[3][1][0 + i] = self.cube[2][1][0 + i]
                self.cube[2][1][0 + i] = self.cube[1][1][0 + i]
                self.cube[1][1][0 + i] = temp[0 + i]
        elif(type == 'M'):
            temp = [self.cube[0][0][1], self.cube[0][1][1], self.cube[0][2][1]]
            for i in range(3):
                self.cube[0][0 + i][1] = self.cube[5][0 + i][1]
                self.cube[5][0 + i][1] = self.cube[2][2 - i][1]
                self.cube[2][2 - i][1] = self.cube[4][0 + i][1]
                self.cube[4][0 + i][1] = temp[0 + i]
        elif(type == 'S'):
            temp = [self.cube[5][1][0], self.cube[5][1][1], self.cube[5][1][2]]
            for i in range(3):
                self.cube[5][1][0 + i] = self.cube[3][2 - i][1]
                self.cube[3][2 - i][1] = self.cube[4][1][2 - i]
                self.cube[4][1][2 - i] = self.cube[1][0 + i][1]
                self.cube[1][0 + i][1] = temp[0 + i]

    def __rotateMidAntiClock(self, type):
        if(type == 'E'):
            temp = [self.cube[0][1][0], self.cube[0][1][1], self.cube[0][1][2]]
            for i in range(3):
                self.cube[0][1][0 + i] = self.cube[1][1][0 + i]
                self.cube[1][1][0 + i] = self.cube[2][1][0 + i]
                self.cube[2][1][0 + i] = self.cube[3][1][0 + i]
                self.cube[3][1][0 + i] = temp[0 + i]
        elif(type == 'M'):
            temp = [self.cube[0][0][1], self.cube[0][1][1], self.cube[0][2][1]]
            for i in range(3):
                self.cube[0][0 + i][1] = self.cube[4][0 + i][1]
                self.cube[4][0 + i][1] = self.cube[2][2 - i][1]
                self.cube[2][2 - i][1] = self.cube[5][0 + i][1]
                self.cube[5][0 + i][1] = temp[0 + i]
        elif(type == 'S'):
            temp = [self.cube[5][1][0], self.cube[5][1][1], self.cube[5][1][2]]
            for i in range(3):
                self.cube[5][1][0 + i] = self.cube[1][0 + i][1]
                self.cube[1][0 + i][1] = self.cube[4][1][2 - i]
                self.cube[4][1][2 - i] = self.cube[3][2 - i][1]
                self.cube[3][2 - i][1] = temp[0 + i]
    
    def __move(self, type):
        if(type == 'U'):
            self.__rotateClock(5)
        elif(type == 'UP'):
            self.__rotateAntiClock(5)
        elif(type == 'D'):
            self.__rotateClock(4)
        elif(type == 'DP'):
            self.__rotateAntiClock(4)
        elif(type == 'R'):
            self.__rotateClock(1)
        elif(type == 'RP'):
            self.__rotateAntiClock(1)
        elif(type == 'L'):
            self.__rotateClock(3)
        elif(type == 'LP'):
            self.__rotateAntiClock(3)
        elif(type == 'F'):
            self.__rotateClock(0)
        elif(type == 'FP'):
            self.__rotateAntiClock(0)
        elif(type == 'B'):
            self.__rotateClock(2)
        elif(type == 'BP'):
            self.__rotateAntiClock(2)
        elif(type == 'E'):
            self.__rotateMidClock('E')
        elif(type == 'EP'):
            self.__rotateMidAntiClock('E')
        elif(type == 'M'):
            self.__rotateMidClock('M')
        elif(type == 'MP'):
            self.__rotateMidAntiClock('M')
        elif(type == 'S'):
            self.__rotateMidClock('S')
        elif(type == 'SP'):
            self.__rotateMidAntiClock('S')
        elif(type == 'x'):
            self.__move('LP')
            self.__move('MP')
            self.__move('R')
        elif(type == 'xP'):
            self.__move('L')
            self.__move('M')
            self.__move('RP')
        elif(type == 'y'):
            self.__move('U')
            self.__move('EP')
            self.__move('DP')
        elif(type == 'yP'):
            self.__move('UP')
            self.__move('E')
            self.__move('D')
        elif(type == 'z'):
            self.__move('F')
            self.__move('S')
            self.__move('BP')
        elif(type == 'zP'):
            self.__move('FP')
            self.__move('SP')
            self.__move('B')
        elif(type == 'u'):
            self.__move('U')
            self.__move('EP')
        elif(type == 'uP'):
            self.__move('UP')
            self.__move('E')
        elif(type == 'd'):
            self.__move('D')
            self.__move('E')
        elif(type == 'dP'):
            self.__move('DP')
            self.__move('EP')
        elif(type == 'r'):
            self.__move('R')
            self.__move('MP')
        elif(type == 'rP'):
            self.__move('RP')
            self.__move('M')
        elif(type == 'l'):
            self.__move('L')
            self.__move('M')
        elif(type == 'lP'):
            self.__move('LP')
            self.__move('MP')
        elif(type == 'f'):
            self.__move('F')
            self.__move('S')
        elif(type == 'fP'):
            self.__move('FP')
            self.__move('SP')
        elif(type == 'b'):
            self.__move('B')
            self.__move('SP')
        elif(type == 'bP'):
            self.__move('BP')
            self.__move('S')

    def doMoves(self, moves):
        """
        Move or manipulate the cube using formulas.
        """
        # moves is sent to parseFormula() to get the object understandable instructions
        moves = parseFormula(moves)
        for m in moves:
            self.__move(m)

    def getFaces(self):
        """
        Deep copy the cube faces matrix array.
        """
        return copy.deepcopy(self.cube)
