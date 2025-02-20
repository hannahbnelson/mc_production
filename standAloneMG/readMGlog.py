import os
import argparse

def skim_MGlog(inFile, outFile):
    
    with open(outFile, "w") as output: 
        with open(inFile, "r") as input: 
            for line in input:
                
                if "Summary" in line.strip("\n"):
                    ### strip and lstrip also remove "S" from the SM point name so I switched to the .find method
                    ### line=line.strip("tag: tag_1 ===") works interactively but not when run in the script 
                    ### I have no clue why so instead just use line.find
                    # line=line.lstrip("=== Results Summary for run:")
                    # line=line.rstrip("tag: tag_1 ===")

                    index=line.find("run:")+5   #find index for first character after "Results Summary for run: "
                    line=line[index:]           #shorten line to remove those characters
                    line=line[:line.find("tag")]+'\n'   #remove "tag: tag_1 ===" from the end
                    output.write(line)

                if "Cross-section :" in line.strip("\n"):
                    line=line.strip("     Cross-section :   ")
                    output.write(line)

    print(f"saving to {outFile}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command Line options parser")
    parser.add_argument("logFile", help="MG log file to be read")
    parser.add_argument("--outname", '-o', default="MG_xsec", help="output file name")
    args = parser.parse_args()

    logFile = args.logFile
    outname = args.outname

    outFile = f"{outname}.txt"

    skim_MGlog(logFile, outFile)
