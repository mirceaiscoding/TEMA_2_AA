import math
from random import choices

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
            
            self.CROSSOVER_PROBABILITY = float(data.readline()) # probabilitatea de recombinare
            print(f"CROSSOVER_PROBABILITY: {self.CROSSOVER_PROBABILITY}")

            self.MUTATION_PROBABILITY = float(data.readline()) # probabilitatea de mutatie
            print(f"MUTATION_PROBABILITY: {self.MUTATION_PROBABILITY}")

            self.NUMBER_OF_STEPS = int(data.readline()) # numarul de etape al algoritmului
            print(f"NUMBER_OF_STEPS: {self.NUMBER_OF_STEPS}")

    def generateRandomChromosome(self):
        return choices([0, 1], k=self.CHROMOSOME_LENGTH)
        
    def generateRandomPopulation(self):
        return [self.generateRandomChromosome() for i in range(self.POPULATION_SIZE)]
    
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
    
    def getFunctionValue(self, x):
        a, b, c = self.FUNCTION_PARAMS
        return 1.0 * a * (x**2) + b * x + c

alg = Algorithm("data.txt")

# TESTE
# print(alg.getValue([0,0,0,0,0,1,1,1,0,1,0,0,1,0,0,1,1,1,0,0,0,1]))
# print(alg.getFunctionValue(-0.914592))