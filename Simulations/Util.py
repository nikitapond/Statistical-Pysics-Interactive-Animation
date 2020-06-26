import sys
sys.path.append('C:\\Users\\nikit\\AppData\\Local\\Programs\\Python\\python38\\lib\\site-packages')

import numpy as np

class Vec2:
    '''
    A basic 2 dimensional vector object
    ...
    Attributes:
        x : float
            The x coordinate of this vector
        y : float
            The x coordinate of this vector
    '''

    def __init__(self, x, y):
        '''
        Initialised the vector
        Params:
            x - float - The x coordinate of this vector
            y - float - The y coordinate of this vector
        '''
        self.x = x
        self.y = y

    def sqrMag(self):
        '''
        Finds the square magnitude of this vector
        Returns:
            |Vec2|^2
        '''
        return self.x*self.x + self.y*self.y

    def mag(self):
        '''
        Finds the magnitude of this vector
        Returns:
            |Vec2|
        '''
        return np.sqrt(self.x*self.x + self.y*self.y)

    def __add__(self, other):
        '''
        Adds this vector with the other vector, and returns the result
        Params:
            other - Vec2, the other vector to include in this sum
        Returns:
            The sum of this vector with 'other'
        '''
        # Check if the second object is of the correct instance type
        if(isinstance(other, Vec2)):
            #Sum and return
            return Vec2(self.x + other.x, self.y + other.y)
        # Invalid summing
        print("Cannot add 2 non vec2")
        return None

    def __sub__(self, other):
        '''
        Substracts the other vector from this vector, and returns the result
        Params:
            other - Vec2 -  the other vector to subtract away from this vector
        Returns:
            The value 'this-other'
        '''
        # Check if the second object is of the correct instance type
        if(isinstance(other, Vec2)):
            # Subtract and return
            return Vec2(self.x - other.x, self.y - other.y)
        # Invalid subtract
        print("Cannot subtract 2 non vec2")
        return None

    def __mul__(self, other):
        '''
        Multiplies this vector by the value 'other'
        Params:
            Other - float - scales this vector by 'other'
            Other - Vec2 -  scales self.x by other.x, and self.y by other.y
        Returns:
            The product this * other
        '''
        # Check if we are multiplying by a scaler value
        if(isinstance(other, float) or isinstance(other, int)):
            return Vec2(self.x * other, self.y * other)
        # Check if instance of vec2
        if(isinstance(other, Vec2)):
            return Vec2(self.x * other.x, self.y * other.y)
        print("Cannot multiply Vec2 by ", type(other))
        return None

    def __str__(self):
        '''
        Cast function to turn this object to a string
        Returns:
            string format of this object
        '''
        return "[" + str(self.x) + "," + str(self.y) + "]"


class Vec2i:
    '''
    A basic 2 dimensional vector class that only allows integer values
    ...
    Attributes
        x : int
            The x coordinate of this vector
        y : int
            The y coordinate of this vector
    '''

    def __init__(self, x, y):
        '''
        Initialises this Vec2i
        Params:
            x - int - x coordinate of this vector
            y - int - y coordinate of this vector
        '''
        if((isinstance(x,int) or isinstance(y, int)) == False):
            print("Vec2i must be constructed from integer values")
            return
        self.x=x
        self.y=y

    def __hash__(self):
        '''
        Calculates a unique has for Vec2i with x and y coordinates in the range [0, 2^16] to allow use as a dictionary
        key
        Returns:
            The hash for this vec2i
        '''
        return self.x<<16 + self.y

    def __eq__(self, other):
        '''
        Returns true if the other object is of type Vec2i, and has equal coordinates
        Params:
            other - the object the check equality with
        Returns:
            True if the other object is of correct type, and has same coordinates.
            False otherwise
        '''
        if isinstance(other, Vec2i):
            return (self.x, self.y) == (other.x, other.y)
        return False

    def __ne__(self, other):
        '''
        Returns false if the other object is of type Vec2i and has equal coordinates
        Params:
            other - the object the check inequality with
        Returns:
            False if the other object is of correct type, and has same coordinates.
            True otherwise
        '''
        return not (self == other)

    @staticmethod
    def roundVec2(vec2):
        '''
        Converts a given vec2 into a vec2i by casting float coordinates to integers
        Params:
            vec2 - Vec2 - Vector to convert to Vec2i
        Returns:
            Vec2i cast from supplied vec2
        '''
        return Vec2i(int(vec2.x), int(vec2.y))