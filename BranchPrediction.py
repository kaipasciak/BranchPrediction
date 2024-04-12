# Branch Prediction Assignment
# CS 3220
# Programming Assignment #4
# Author: Kai Pasciak

# Global variables and arrays to be set later
MIN_COUNTER = 0
MAX_COUNTER = 0
filename = ""
counterBits = 0
addresses = []
counters = []

def prompt():
    filename = input("Enter the file name to test: ")
    while (counterBits < 0 and counterBits > 3):
        counterBits = int(input("Enter the number of bits to use: "))
    if counterBits == 1:
        MAX_COUNTER = 2
    if counterBits ==
def main():
    print("Branch Prediction Simulator")
    prompt()

main()