import json
import socket
import time
import random
import uuid

class Animal:
    def __init__(self, attack, health, speed):
        self.attack = attack
        self.health = health
        self.speed = speed


class Predator(Animal):
    def __init__(self, attack, health, speed):
        super().__init__(attack, health, speed)

class Wolf(Predator):
    def __init__(self, attack, health, speed):
        super().__init__(attack, health, speed)
        self.guid = generateUUID()

class Jaguar(Predator):
    def __init__(self, attack, health, speed):
        super().__init__(attack, health, speed)
        self.guid = generateUUID()


class Prey(Animal):
    def __init__(self, attack, health, speed):
        super().__init__(attack, health, speed)

class Rabbit(Prey):
    def __init__(self, attack, health, speed):
        super().__init__(attack, health, speed)
        self.guid = generateUUID()

class Deer(Prey):
    def __init__(self, attack, health, speed):
        super().__init__(attack, health, speed)
        self.guid = generateUUID()


def generateUUID():
    return str(uuid.uuid4())


def init_population():

    wolfList = [Wolf(random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)).__dict__ for i in range(2)]
    jaguarList = [Jaguar(random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)).__dict__ for i in range(2)]
    rabbitList = [Rabbit(random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)).__dict__ for i in range(2)]
    deerList = [Deer(random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)).__dict__ for i in range(2)]
    
    listOfPred = [{"wolves": wolfList}, {"jaguars": jaguarList}]
    listOfPrey = [{"rabbits": rabbitList}, {"deer": deerList}]
    animalList = {"preyList": listOfPrey, "predList": listOfPred}
    return animalList