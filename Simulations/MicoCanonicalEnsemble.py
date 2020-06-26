import sys
sys.path.append('C:\\Users\\nikit\\AppData\\Local\\Programs\\Python\\python38\\lib\\site-packages')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import gridspec


class Vec2:

    def __init__(self, x, y):
        self.x=x
        self.y=y

    def __add__(self, other):
        if(isinstance(other, Vec2) == False):
            print("Cannot add 2 non vec2")
            return None
        return Vec2(self.x+other.x, self.y+other.y)

    def __mul__(self, other):
        if(isinstance(other, float) or isinstance(other, int)):
            return Vec2(self.x*other, self.y*other)
        if(isinstance(other, Vec2)):
            return Vec2(self.x * other.x, self.y*other.y)
        return None

    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y) + "]"

    def sqrMag(self):
        return self.x*self.x + self.y*self.y

    def mag(self):
        return np.sqrt(self.x*self.x + self.y*self.y)


class Vec2i:
    def __init__(self, x, y):
        if((isinstance(x,int) or isinstance(y, int)) == False):
            print("Vec2i must be constructed from integer values")
        self.x=x
        self.y=y

    def __hash__(self):
        return self.x<<16 + self.y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)

    @staticmethod
    def RoundVec2(vec2):
        return Vec2i(int(vec2.x), int(vec2.y))


class Particle:
    def __init__(self, position, velocity, mass):
        self.position = position
        self.velocity = velocity
        self.mass = mass


class AnimationSystem:
    def __init__(self, size=(12, 8), dt=0.1, maxEnergy=10, energyLevels=9):
        self.size = size
        self.dt = dt
        self.fig = plt.figure(figsize=size)
        self.energyLevels = np.linspace(1, maxEnergy, energyLevels)
        print(self.energyLevels)
        spec = gridspec.GridSpec(ncols=1, nrows=3, height_ratios=[2, 1, 1])

        self.simPlot = self.fig.add_subplot(spec[0])
        self.energyPlot = self.fig.add_subplot(spec[1])
        self.particleCountPlot = self.fig.add_subplot(spec[2])

        self.totalEnergyData = []
        self.totalParticleCountData = []
        self.time = [0]

        self.particles = []

        self.energyLevelParticles = {self.energyLevels[i]: [] for i in range(len(self.energyLevels)) }

        self.grid = {Vec2i(x_, y_): [] for x_ in range(size[0]) for y_ in range(size[1])}

        self.partPosX = []
        self.partPosY = []


    def addRandomParticles(self, count):

        for i in range(count):
            # Randomly choose position
            x = np.random.rand() * an.size[0]
            y = np.random.rand() * an.size[1]

            energy = self.energyLevels[int(np.random.rand() * len(self.energyLevels))]
            print(energy)
            # Particle velocity must be such that its KE is equal to this energy
            # -> 0.5*|v|^2 = energy
            # -> 0.5* (v.x*v.x + v.z*v.z) = energy
            # -> 0.5 * r^2 = energy
            # -> Polar coordinates -> r = (2*energy)**0.5, theta=random
            r = (2*energy)**0.5
            theta = np.random.rand()*2*np.pi
            vx = r * np.cos(theta)
            vy = r * np.sin(theta)
            part = Particle(Vec2(x,y), Vec2(vx,vy), 1)
            self.addParticle(part, energy)


    def addParticle(self, particle, energy):
        vec2i = Vec2i.RoundVec2(particle.position)
        self.grid[vec2i].append(particle)
        self.partPosX.append(particle.position.x)
        self.partPosY.append(particle.position.y)

        self.energyLevelParticles[energy].append(particle)

    def inBounds(self, vec2):
        '''
        Checks if the given position lies within our system
        :type vec2: Vec2
        :param vec2: The position to check
        :return: True if the position lies between (0,0) inclusive, and (size[0],size[1]) exclusive,  false otherwise
        '''
        return 0 <= vec2.x <= vec2.y and vec2.x < self.size[0] and vec2.y < self.size[1]

    def initSimulation(self):
        plt.xlim(0, self.size[0])
        plt.ylim(0, self.size[1])
        self.scat = self.simPlot.scatter(self.partPosX, self.partPosY)
        return self.scat

    def initEnergyPlot(self):
        totalEnergy = 0
        partCount = 0
        # iterate every grid point
        for pos in self.grid:
            # If we currently have at least 1 particle in this grid point
            if(len(self.grid[pos])!=0):
                partCount+=1
                # iterate all particles within this grid point
                for part in self.grid[pos]:
                    totalEnergy += part.mass * 0.5 * part.velocity.sqrMag()

        self.totalEnergyData.append(totalEnergy/partCount)
        self.test = [1]
        #plt.xlim([0, 20])
        #plt.ylim([0, int(totalEnergy) * 2])
        self.energy = self.energyPlot.plot(self.time, np.array(self.totalEnergyData)/partCount)
        self.energyPlot.set_title("Energy")
        self.energyPlot.set_xlim([0, 20])
        self.energyPlot.set_ylim([0, int(totalEnergy) * 2])

        return self.energy


    def initParticleCountPlot(self):
        partCount = 0
        for pos in self.grid:
            # If we currently have at least 1 particle in this grid point
            partCount += len(self.grid[pos])

        self.totalParticleCountData.append(partCount)


        self.particleCount = self.particleCountPlot.plot(self.time, self.totalParticleCountData)
        self.particleCountPlot.set_title("Particle Count")
        self.particleCountPlot.set_xlim([0, 20])
        self.particleCountPlot.set_ylim([0, partCount * 2])
        return self.particleCount

    def updateSimulation(self, frame):

        self.time.append(frame * self.dt)

        self.partPosX.clear()
        self.partPosY.clear()

        dt = 0.1

        totalEnergy=0
        totalPart = 0
        #Data set to hold next data
        nextGrid = {Vec2i(x,y):[] for x in range(self.size[0]) for y in range(self.size[1])}
        for pos in self.grid:
            #If we currently have at least 1 particle in this grid point
            if(len(self.grid[pos])!=0):
                #iterate all particles within this grid point
                for part in self.grid[pos]:
                    totalPart+=1
                    nPart, dEn= self.updateParticle(part, dt)
                    totalEnergy+=dEn
                    nVec2i = Vec2i.RoundVec2(nPart.position)
                    nextGrid[nVec2i].append(nPart)
                    self.partPosX.append(nPart.position.x)
                    self.partPosY.append(nPart.position.y)

        self.totalEnergyData.append(totalEnergy)
        self.totalParticleCountData.append(totalPart)
        self.grid = nextGrid
        self.scat.set_offsets(np.c_[self.partPosX, self.partPosY])
        return self.scat

    def updateEnergy(self, frame):
        if len(self.time)*self.dt > 20:
            self.energyPlot.set_xlim([len(self.time)*self.dt - 20*self.dt, len(self.time)*self.dt])

        self.energy = self.energyPlot.plot(self.time, self.totalEnergyData, color='g')
        return self.energy



    def updateParticleCount(self, frame):

        if len(self.time) * self.dt > 20:
            self.particleCountPlot.set_xlim([len(self.time) * self.dt - 20 * self.dt, len(self.time) * self.dt])
        self.particleCount = self.particleCountPlot.plot(self.time, self.totalParticleCountData, color='g')
        return self.particleCount

    def updateParticle(self, particle, dt):

        nPos = particle.position + particle.velocity*dt
        nVel = particle.velocity
        # If particle moves outside bounds, we must reflect
        if(self.inBounds(nPos) == False):
            if(nPos.x < 0):
                nPos.x=0
                nVel.x *= -1
            elif(nPos.x >= self.size[0]):
                nPos.x = self.size[0] - 0.001
                nVel.x *= -1

            if (nPos.y < 0):
                nPos.y = 0
                nVel.y *= -1
            elif (nPos.y >= self.size[1]):
                nPos.y = self.size[1] - 0.001
                nVel.y *= -1



        energy = particle.mass * 0.5 * nVel.sqrMag()
        return Particle(nPos, nVel, particle.mass), energy

    def totalEnergy(self, frame=-1):
        if frame == -1:
            return self.totalEnergyData[len(self.totalEnergyData)-1]
        return self.totalEnergyData[frame]

    def totalParticleCount(self, frame=-1):
        if frame == -1:
            return self.totalParticleCountData[len(self.totalParticleCountData)-1]
        return self.totalParticleCountData[frame]


    def averageEnergy(self, frame=-1):
        return self.totalEnergy(frame)/self.totalParticleCount(frame)



    def runSimulation(self, frames):
        interval = int(1/self.dt)
        mainSim = animation.FuncAnimation(self.fig, self.updateSimulation, init_func=self.initSimulation, frames=frames,
                                          interval=interval)

        energyPlot = animation.FuncAnimation(self.fig, self.updateEnergy, init_func=self.initEnergyPlot, frames=frames,
                                             interval=interval)

        particlePlot = animation.FuncAnimation(self.fig, self.updateParticleCount, init_func=self.initParticleCountPlot,
                                               frames=frames, interval=interval)
        plt.show()



partPos = []

for i in range(20):
    partPos.append(Vec2(i*0.2, i*0.5))


an = AnimationSystem(size=(18, 11))

an.addRandomParticles(20)
an.runSimulation(400)