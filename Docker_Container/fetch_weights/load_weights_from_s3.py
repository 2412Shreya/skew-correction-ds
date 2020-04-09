import os
import subprocess
import csv
import sys
# import gsutil

def loadWeights(path, outputPath):
    print ("Weights Loading started")
    command = ['gsutil', 'ls', path]
    output = subprocess.check_output(command).splitlines()
    print ("output", output)
    # Get file name from fixed path for weights
    # Assuming only one csv file should be present
    file_name = str(str(output[1]).split("/")[-1])[0:-1]
    print ("file_name", file_name)
    assert file_name.endswith(".csv") and file_name.startswith("part-")
    if not os.path.exists(outputPath):
        print ("Making download directory")
        os.mkdir(outputPath)
    FILE_PATH = outputPath + "/weights.csv"
    print ("#####################")
    print ("FILE_PATH", FILE_PATH)
    subprocess.call(["gsutil", "cp", path + "/" + file_name, FILE_PATH])
    print ("Weights loading finished")
def main(argv):
    inputPath = argv[0]
    outputPath = argv[1]
    loadWeights(inputPath, outputPath)
if __name__ == "__main__":
   main(sys.argv[1:])