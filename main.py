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
    
    # Returneaza probabilitatea de selectie a fiecarui cromozon (suma probabilitatilor este 1) si valoarea maxima a functiei
    def getPopulationSelectionProbability(self, population):
        functionValues = [self.getFunctionValue(self.getValue(chromosome)) for chromosome in population]
        sumOfFunctionValues = sum(functionValues)
        return [value / sumOfFunctionValues for value in functionValues], max(functionValues)
    
    # Returneaza o pereche de cromozomi din populatie luand in calcul valorile functiei
    # def selectPairOfChromosomes(self, population, selectionProbability):
    #     return choices(population, weights=selectionProbability, k=2)

    # Returneaza punctul de rupere si cromozonii rezultati prin incrucisarea a 2 cromozomi la un punct random 
    # (ia inceputul primului si finalul celui de-al doilea si invers)
    def crossoverChromosomes(self, chromosomeA, chromosomeB):
        # punctul la care se taie cromozomii, ales random
        crossoverPoint = randint(1, self.CHROMOSOME_LENGTH-1)
        newChromosome1 = chromosomeA[:crossoverPoint] + chromosomeB[crossoverPoint:]
        newChromosome2 = chromosomeB[:crossoverPoint] + chromosomeA[crossoverPoint:]
        return crossoverPoint, newChromosome1, newChromosome2
    
    # Returneaza punctul de rupere si cromozonii rezultati prin incrucisarea a 3 cromozomi la un punct random 
    def threeWayCrossoverChromosomes(self, chromosomeA, chromosomeB, chromosomeC):
        # punctul la care se taie cromozomii, ales random
        crossoverPoint = randint(1, self.CHROMOSOME_LENGTH-1)
        newChromosome1 = chromosomeA[:crossoverPoint] + chromosomeB[crossoverPoint:]
        newChromosome2 = chromosomeB[:crossoverPoint] + chromosomeC[crossoverPoint:]
        newChromosome3 = chromosomeC[:crossoverPoint] + chromosomeA[crossoverPoint:]
        return crossoverPoint, newChromosome1, newChromosome2, newChromosome3
    
    # Returneaza indicii cromozonilor modificati
    def mutateChromosomes(self, population):
        modified = set()
        for i, chromosome in enumerate(population):
            for bit in range(self.CHROMOSOME_LENGTH):
                if random() < self.MUTATION_PROBABILITY:
                    # mutatie = inversam valoarea bitului
                    chromosome[bit] = 1 - chromosome[bit]
                    modified.add(i+1)
        return modified
                    
    def toString(self, chromosome):
        return "".join([str(bit) for bit in chromosome])
                    
    def printPopulation(self, population, outputFile:TextIOWrapper):
        for i, chromosome in enumerate(population):
            value = self.getValue(chromosome)
            outputFile.write("{0:>2}: {1:<25} x = {2:<10} f = {3}\n".format(i+1, self.toString(chromosome), round(value, 6), self.getFunctionValue(value)))
            
    def printPopulationSelectionProbability(self, probabilities, outputFile:TextIOWrapper):
        for i, probability in enumerate(probabilities):
            outputFile.write("{0:>2}: probabilitate = {1}\n".format(i+1, probability))
            
    def printProbabilityIntervals(self, probabilityIntervals, outputFile:TextIOWrapper):   
        for value in probabilityIntervals:
            outputFile.write("{0}\n".format(value))
    
    # Ruleaza algoritmul pentru numarul de pasi specificati si printeaza in fisierul dat informatiile
    def run(self, outputPath, isElitist=True):
        with open(outputPath, "w+") as outputFile:
            # Generam prima populatie random
            population = self.generateRandomPopulation()
            outputFile.write("Populatie initiala\n")
            self.printPopulation(population, outputFile)
            outputFile.write("\n")
            for step in range(1, self.NUMBER_OF_STEPS):
                # Generam noua populatie
                # probabilitatea e calculata in functie de suma totala a cromozonilor
                probabilities, maxFunctionValue = self.getPopulationSelectionProbability(population)
                if step == 1:
                    outputFile.write("Probabilitati selectie\n")
                    self.printPopulationSelectionProbability(probabilities, outputFile)
                    outputFile.write("\n")
                else:
                    outputFile.write(f"Step {step}: {maxFunctionValue}\n")
                    
                # intervalele sunt sume partiale pe probabilitati, suma totala este mereu 1 pentru ca sunt procente
                currentSum = 0.0
                probabilityIntervals = [currentSum]
                for probability in probabilities:
                    currentSum += probability
                    probabilityIntervals.append(currentSum)
                
                if step == 1:
                    outputFile.write("Intervale probabilitati selectie\n")
                    self.printProbabilityIntervals(probabilityIntervals, outputFile)
                    outputFile.write("\n")
                
                chromosomesToSelect = self.POPULATION_SIZE
                selectedChromosomes = [] 
                if isElitist:
                    # daca este elitist pastram cel mai bun cromozon la fiecare pas
                    maxProbability = max(probabilities)
                    i = probabilities.index(maxProbability)
                    eliteChromosome = population[i]
                    selectedChromosomes.append(eliteChromosome)
                    chromosomesToSelect -= 1
                    if step == 1:
                        outputFile.write("Criteriu elitist: Selectam cromozomul {0}\n".format(i+1))
                
                for i in range(chromosomesToSelect):
                    r = random()
                    # caut binar intervalul in care se afla r
                    left = 0
                    right = len(probabilityIntervals) - 1
                    while left <= right:
                        mid = (left + right) // 2
                        if (probabilityIntervals[mid] < r):
                            left = mid + 1
                        else:
                            right = mid - 1
                    if step == 1:
                        outputFile.write("random = {0}: Selectam cromozomul {1}\n".format(round(r, 10), right+1))
                    selectedChromosomes.append(population[right])
                    
                population = selectedChromosomes
                if step == 1:
                    outputFile.write("\nDupa selectie\n")
                    self.printPopulation(population, outputFile)
                    
                    outputFile.write(f"\nProbabilitatea de incrucisare {self.CROSSOVER_PROBABILITY}\n")
                
                # ignor cromozonul elitist la incrucisare
                toCrossover = []
                unchanged = []
                if isElitist:
                    unchanged.append(eliteChromosome)
                for i in range(len(unchanged), self.POPULATION_SIZE):
                    r = random()
                    if r < self.CROSSOVER_PROBABILITY:
                        # participa la incrucisare
                        toCrossover.append((i, population[i]))
                        if step == 1:
                            outputFile.write("{0:>2}: random = {1} < {2} participa\n".format(i+1, round(r, 10), self.CROSSOVER_PROBABILITY))
                    else:
                        unchanged.append(population[i])
                        if step == 1:
                            outputFile.write("{0:>2}: random = {1}\n".format(i+1, round(r, 10)))
                
                population = unchanged
                
                # cat timp avem 2 cromozomi de incrucisat
                while len(toCrossover) >= 2:
                    if len(toCrossover) == 3:
                        # 3 way crossover
                        indexA, a = toCrossover[0]
                        indexB, b = toCrossover[1]
                        indexC, c = toCrossover[2]
                        toCrossover.clear()
                        
                        crossoverPoint, mutatedA, mutatedB, mutatedC = self.threeWayCrossoverChromosomes(a, b, c)
                        population.append(mutatedA)
                        population.append(mutatedB)
                        population.append(mutatedC)
                                                
                        if step == 1:
                            outputFile.write("\nRecombinare dintre cromozonul {0}, {1} si {2}:\n".format(indexA+1, indexB+1, indexC+1))
                            outputFile.write(f"{self.toString(a)} {self.toString(b)} {self.toString(c)} punct {str(crossoverPoint)}\n")
                            outputFile.write(f"Rezultat {self.toString(mutatedA)} {self.toString(mutatedB)} {self.toString(mutatedC)}\n")

                        
                    else:
                        # selectez 2 random si ii scot din populatie
                        indexA, a = toCrossover[randint(0, len(toCrossover)-1)]
                        toCrossover.remove((indexA, a))
                        indexB, b = toCrossover[randint(0, len(toCrossover)-1)]
                        toCrossover.remove((indexB, b))
                        
                        # adaug cromozonii rezultati dupa incrucisare
                        crossoverPoint, mutatedA, mutatedB = self.crossoverChromosomes(a, b)
                        population.append(mutatedA)
                        population.append(mutatedB)
                        
                        if step == 1:
                            outputFile.write("\nRecombinare dintre cromozonul {0} si cromozonul {1}:\n".format(indexA+1, indexB+1))
                            outputFile.write(f"{self.toString(a)} {self.toString(b)} punct {str(crossoverPoint)}\n")
                            outputFile.write(f"Rezultat {self.toString(mutatedA)} {self.toString(mutatedB)}\n")



                if step == 1:
                    outputFile.write("\nDupa recombinare\n")
                    self.printPopulation(population, outputFile)
                    
                    outputFile.write(f"\nProbabilitatea de mutatie pentru fiecare gena {self.MUTATION_PROBABILITY}\n")
                
                mutatedChromosomes = self.mutateChromosomes(population)
                if step == 1:
                    outputFile.write("Au fost modificati cromozomii:\n")
                    for i in mutatedChromosomes:
                        outputFile.write(str(i) + "\n")
                        
                    outputFile.write("\nDupa mutatie\n")
                    self.printPopulation(population, outputFile)
                    
                    outputFile.write("\nEvolutia maximului:\n")
                    outputFile.write(f"Step {step}: {maxFunctionValue}\n")

                # pun inapoi cromozomul elitist
                if isElitist:
                    population = [eliteChromosome] + population[1:]


alg = Algorithm("data.txt")
alg.run("evolutie.txt")
alg.run("evolutieFaraElitism.txt", isElitist=False)

# TESTE
# print(alg.getValue([0,0,0,0,0,1,1,1,0,1,0,0,1,0,0,1,1,1,0,0,0,1]))
# print(alg.getFunctionValue(-0.914592))
# print(alg.crossoverChromosomes([0]*alg.CHROMOSOME_LENGTH, [1]*alg.CHROMOSOME_LENGTH))
