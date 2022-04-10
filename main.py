from io import TextIOWrapper
import math
from random import choices, randint, random

class Algorithm:
    
    def __init__(self, pathToInput):
        with open(pathToInput, "r") as data:
            
            self.POPULATION_SIZE = int(data.readline()) # dimensiunea populatiei = numarul de cromozomi pe etapa
            print(f"POPULATION_SIZE: {self.POPULATION_SIZE}")
            
            x, y = data.readline().split()
            self.DOMAIN = (float(x), float(y)) # in acest domeniu putem cauta rezultate
            print(f"DOMAIN: {self.DOMAIN}")

            x, y, z = data.readline().split()
            self.FUNCTION_PARAMS = (float(x), float(y), float(z)) # parametrii functiei de gradul 2
            print(f"FUNCTION_PARAMS: {self.FUNCTION_PARAMS}")

            self.PRECISION = int(data.readline()) # precizia cu care se lucreaza
            print(f"PRECISION: {self.PRECISION}")

            # cati biti sa contina fiecare cromozon, calculat in functie de precizie si interval
            self.CHROMOSOME_LENGTH = math.ceil(math.log2((self.DOMAIN[1] - self.DOMAIN[0]) * (10 ** self.PRECISION)))
            print(f"CHROMOSOME_LENGTH: {self.CHROMOSOME_LENGTH}")
            
            self.CROSSOVER_PROBABILITY = float(data.readline()) # probabilitatea de incrucisare (crossover)
            print(f"CROSSOVER_PROBABILITY: {self.CROSSOVER_PROBABILITY}")

            self.MUTATION_PROBABILITY = float(data.readline()) # probabilitatea de mutatie
            print(f"MUTATION_PROBABILITY: {self.MUTATION_PROBABILITY}")

            self.NUMBER_OF_STEPS = int(data.readline()) # numarul de etape al algoritmului
            print(f"NUMBER_OF_STEPS: {self.NUMBER_OF_STEPS}")

    # Returneaza un cromozom random
    def generateRandomChromosome(self):
        return choices([0, 1], k=self.CHROMOSOME_LENGTH)
        
    # Returneaza o populatie random
    def generateRandomPopulation(self):
        return [self.generateRandomChromosome() for i in range(self.POPULATION_SIZE)]
    
    # Returneaza valoarea x din domeniu echivalenta cromozonului
    def getValue(self, chromosome):
        value = 0
        bitValue = 1
        for bit in reversed(chromosome):
            if bit == 1:
                value += bitValue
            bitValue *= 2
        # Valoarea trebuie normalizata pe interval
        # https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range
        normalizedValue = 1.0 * (self.DOMAIN[1] - self.DOMAIN[0]) * (value / (2 ** self.CHROMOSOME_LENGTH - 1)) + self.DOMAIN[0]
        return normalizedValue
    
    # Returneaza valuarea functiei pentru x
    def getFunctionValue(self, x):
        a, b, c = self.FUNCTION_PARAMS
        return 1.0 * a * (x**2) + b * x + c
    
    # Returneaza o pereche de cromozomi din populatie luand in calcul valorile functiei
    def selectPairOfChromosomes(self, population, functionValues):
        return choices(population, weights=functionValues, k=2)

    # Returneaza cromozonii rezultati prin incrucisarea a 2 cromozomi la un punct random 
    # (ia inceputul primului si finalul celui de-al doilea si invers)
    def crossoverChromosomes(self, chromosomeA, chromosomeB):
        # punctul la care se taie cromozomii, ales random
        crossoverPoint = randint(1, self.CHROMOSOME_LENGTH-1)
        newChromosome1 = chromosomeA[:crossoverPoint] + chromosomeB[crossoverPoint:]
        newChromosome2 = chromosomeB[:crossoverPoint] + chromosomeA[crossoverPoint:]
        return newChromosome1, newChromosome2
    
    # Returneaza indicii cromozonilor modificati
    def mutateChromosomes(self, population):
        modified = set()
        for i, chromosome in enumerate(population):
            for bit in range(self.CHROMOSOME_LENGTH):
                if random() > self.MUTATION_PROBABILITY:
                    # mutatie = inversam valoarea bitului
                    chromosome[bit] = 1 - chromosome[bit]
                    modified.add(i)
                    
    def toString(self, chromosome):
        return "".join([str(bit) for bit in chromosome])
                    
    def printPopulation(self, population, outputFile:TextIOWrapper):
        for i, chromosome in enumerate(population):
            value = self.getValue(chromosome)
            outputFile.write("{0:>2}: {1:<25} x = {2:<10} f = {3}\n".format(i, self.toString(chromosome), round(value, 6), self.getFunctionValue(value)))
            
                    
    def run(self, outputPath):
        with open(outputPath, "w+") as outputFile:
            population = self.generateRandomPopulation()
            self.printPopulation(population, outputFile)

                
            

alg = Algorithm("data.txt")
alg.run("evolutie.txt")

# TESTE
# print(alg.getValue([0,0,0,0,0,1,1,1,0,1,0,0,1,0,0,1,1,1,0,0,0,1]))
# print(alg.getFunctionValue(-0.914592))
# print(alg.crossoverChromosomes([0]*alg.CHROMOSOME_LENGTH, [1]*alg.CHROMOSOME_LENGTH))
