# Branch Prediction Assignment
# CS 3220
# Programming Assignment #4
# Author: Kai Pasciak

# Global variables and arrays to be set later
MIN_COUNTER = 0
MAX_COUNTER = 0
filename = ""
counterBits = 0
bufferSize = 0
addresses = []
counters = []

def prompt():
    # Ask for desired input file
    filename = input("Enter the file name to test: ")

    # Ask for and validate number of bits per counter
    while (counterBits < 0 and counterBits > 3):
        counterBits = int(input("Enter the number of bits to use: "))
    if counterBits == 1:
        MAX_COUNTER = 1
    if counterBits == 2:
        MAX_COUNTER = 3
    if counterBits == 3:
        MAX_COUNTER = 7

    # Ask for branch-prediction buffer size
    bufferSize = int(input("Enter the branch-prediction buffer size in bits: "))

    # Make buffer size a multiple of number of bits in counter
    bufferSize = (bufferSize // counterBits) * counterBits


def main():
    print("Branch Prediction Simulator")
    prompt()

main()