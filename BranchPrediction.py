# Branch Prediction Assignment
# CS 3220
# Programming Assignment #4
# Author: Kai Pasciak
# Example: Type "python3 BranchPrediction.py -f curl1m.btrace.out -b 2 -s 1000" into command line

# Import argparse module to enable command line flags
import argparse

# Global variables and arrays to be set later
MIN_COUNTER = 0
MAX_COUNTER = 0
filename = ""
counterBits = 0
bufferSize = 0
addresses = []
counters = []


def arguments():
    # Create instance of argparse
    parser = argparse.ArgumentParser(
        prog='BranchPrediction',
        description='Read results of branch instructions and whether they were taken to simulate branch prediction',
        epilog='')

    # Add flags
    parser.add_argument('-f', '--filenameFlag')
    parser.add_argument('-b', '--counterBitsFlag')
    parser.add_argument('-s', '--bufferSizeFlag')

    # Parse arguments
    args = parser.parse_args()

    # Modify variables based on flags
    filename = str(args.filenameFlag)

    # Ask for and validate number of bits per counter
    counterBits = int(args.counterBitsFlag)
    if counterBits < 0 and counterBits > 3:
        counterBits = int(input("Enter the number of bits to use: "))

    # Ask for branch-prediction buffer size
    bufferSize = int(args.bufferSizeFlag)

    # Represent buffer table size as number of counters rather than number of bits
    if counterBits != 0:
        bufferSize = int(bufferSize // counterBits)

    return [filename, counterBits, bufferSize]


def main():
    print("Branch Prediction Simulator")
    flags = arguments()
    filename = flags[0]
    counterBits = flags[1]
    bufferSize = flags[2]

    if counterBits == 0:
        MAX_COUNTER = 0
    if counterBits == 1:
        MAX_COUNTER = 1
    if counterBits == 2:
        MAX_COUNTER = 3
    if counterBits == 3:
        MAX_COUNTER = 7

    # Create BHT, initialize all values to 0
    BHT = []
    for i in range(bufferSize):
        BHT.append(0)

    # Open file to simulate running program
    with open(filename, "r") as file:
        correctPredictions = 0
        numLines = 0
        for line in file:
            # Read address, update BHT based on branch taken value
            parts = line.split()
            hexAddress = str(parts[0])
            branchTaken = int(parts[1])

            # Convert hex to binary
            address = int(hexAddress, 16) # For address size of 48 bits


            # Calculate index in BHT
            counterIndex = address % bufferSize

            prediction = False
            # See if prediction was correct
            if counterBits == 0: # 0-bit case
                prediction = True
            else:
                if (BHT[counterIndex] > MAX_COUNTER // 2):
                    prediction = True

            # Update number of correct predictions
            if (prediction == True and branchTaken == 1):
                correctPredictions += 1

            if (prediction == False and branchTaken == 0):
                correctPredictions += 1


            # Update BHT
            if (branchTaken == 1):
                BHT[counterIndex] = max(BHT[counterIndex] + 1, MAX_COUNTER)
            if (branchTaken == 0):
                BHT[counterIndex] = min(BHT[counterIndex] - 1, MIN_COUNTER)

            # Increment line counter
            numLines += 1

        # Calculate percentage
        if numLines > 0:
            percentage = (correctPredictions / numLines) * 100
        else:
            percentage = 0

        print(correctPredictions, " out of ", numLines, " correctly predicted.")
        print(f'Percentage = {percentage:.2f}')


main()