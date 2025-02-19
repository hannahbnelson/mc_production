import os
import argparse

def skim_MGlog(inFile, outFile):
    
    with open(outFile, "w") as output: 
        with open(inFile, "r") as input: 
            for line in input:
                if "Summary" in line.strip("\n"):
                    line=line.strip("  === Results Summary for run:")
                    line=line.strip("tag: tag_1 ===")
                    output.write(line)
                if "Cross-section :" in line.strip("\n"):
                    line=line.strip("     Cross-section :   ")
                    output.write(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command Line options parser")
    parser.add_argument("logFile", help="MG log file to be read")
    parser.add_argument("--outname", '-o', default="MG_xsec", help="output file name")
    args = parser.parse_args()

    logFile = args.logFile
    outname = args.outname

    outFile = f"{outname}.txt"

    skim_MGlog(logFile, outFile)
