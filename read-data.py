import sys

def readData(file):
    data = None
    try:
        data = open(file)
    except: 
        print("Error: file " + file + " could not be opened")
    print("printed")

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Usage: python3 read-data.py [file name]")
        sys.exit()
        
    data = readData(sys.argv[1])