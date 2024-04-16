# Branch Prediction Assignment
# CS 3220
# Programming Assignment #4
# Author: Kai Pasciak, Walter Clay
# Example: Type "python3 BranchPrediction.py -f curl1m.btrace.out -b 2 -s 1000" into the command line
# -f filename = curl1m.btrace.out, gcc.btrace.out, or java1m.btrace.out
# -b counterBits = 0, 1, 2, or 3
# -s bufferSize = total size of the BHT in bits

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
        description='Simulate branch prediction based on branch instruction outcomes',
        epilog='')

    # Add flags with constraints, descriptions, etc.
    parser.add_argument('-f', '--filename', required=True, help='Input trace file containing branch outcomes')
    parser.add_argument('-b', '--counterBits', type=int, choices=[0, 1, 2, 3], required=True, help='Number of bits per counter (0, 1, 2, 3)')
    parser.add_argument('-s', '--bufferSize', type=int, required=True, help='Total size of the Branch Prediction Buffer in bits')

    # Parse arguments
    args = parser.parse_args()

    # Put arguments from command line into variables
    filename = args.filename
    counterBits = args.counterBits
    totalBHTSizeInBits = args.bufferSize

    # Calculate number of counters in the BHT based on total size and counter bits
    if counterBits > 0:
        bufferSize = totalBHTSizeInBits // counterBits
    else:
        bufferSize = 1

    return [filename, counterBits, bufferSize]

def main():
    global MAX_COUNTER, MIN_COUNTER
    print("Branch Prediction Simulator")
    flags = arguments()
    filename, counterBits, bufferSize = flags

    # Adjust MAX_COUNTER based on counterBits
    if counterBits == 0:
        MAX_COUNTER = 0  # Not used in static prediction, but initialized for consistency
    elif counterBits == 1:
        MAX_COUNTER = 1
    elif counterBits == 2:
        MAX_COUNTER = 3
    elif counterBits == 3:
        MAX_COUNTER = 7

    print(f'Reading file {filename}')
    print(f'Branch History Table Size (counters): {bufferSize}')
    print(f'Number of bits per entry: {counterBits}')
    print("--------------------------------")

    # Initialize BHT with zeros
    BHT = [0] * bufferSize

    try:
        with open(filename, "r") as file:
            correctPredictions = 0
            numLines = 0
            for line in file:
                parts = line.split()
                if len(parts) == 2:
                    hexAddress, branchTaken = parts
                    branchTaken = int(branchTaken)
                    address = int(hexAddress, 16)  # Convert hex address to integer

                    # Calculate BHT index
                    counterIndex = address % bufferSize

                    # Prediction logic
                    if counterBits > 0:
                        prediction = (BHT[counterIndex] > (MAX_COUNTER // 2))
                    else:
                        prediction = False

                    # Update correct predictions count
                    if prediction == bool(branchTaken):
                        correctPredictions += 1

                    # Update BHT
                    if branchTaken:
                        BHT[counterIndex] = min(BHT[counterIndex] + 1, MAX_COUNTER)
                    else:
                        BHT[counterIndex] = max(BHT[counterIndex] - 1, MIN_COUNTER)

                    numLines += 1

            # Calculate and print prediction statistics
            percentage = (correctPredictions / numLines) * 100 if numLines > 0 else 0
            print(f'{correctPredictions} out of {numLines} correctly predicted.')
            print(f'Percentage = {percentage:.2f}%')
    except FileNotFoundError:
        print("Specified File Not Found")

if __name__ == "__main__":
    main()
