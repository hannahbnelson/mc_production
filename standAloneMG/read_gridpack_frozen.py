'''
This file reads the section of a gridpack log that lists the reweight points 
and correpsonding cross section. 
The input file should be of the form:
	INFO: Computed cross-section:
	INFO: EFTrwgt0_cHQ3_10p0 : 15.2787947689 +- 0.688037899777 pb
	INFO: EFTrwgt1_cHQ3_2p0 : 7.44511134545 +- 0.335269820113 pb
	...
The output file will be of the form: 
	cHQ3=10.0
	15.2787947689 +- 0.688037899777 pb
	cHQ3=2.0
	7.44511134545 +- 0.335269820113 pb
	...

This output file is then of the form to be 
read by plotting_tools_histEFT.read_MGstandalone_txt()
which turns these points into a usable dictionary of wc and xsec values
'''

import os
import argparse

def skim_gridpack_log(inFile, outFile):

	with open(outFile, "w") as output: 
		with open(inFile, "r") as input: 
			out = ''
			for line in input:
				if "EFTrwgt" in line.strip("\n"):
					line = line[15:]
					line = line.split(":")

					wc_name = line[0].split("_")[0]
					wc_val = line[0].split("_")[1]
					wc_val = wc_val.replace("p", ".")
					wc_val = wc_val.replace("m", "-")

					xsec = line[1][1:]

					out += f"{wc_name}={wc_val}\n{xsec}"

			print(f"saving to {outFile}")
			output.write(out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command Line options parser")
    parser.add_argument("logFile", help="MG log file to be read")
    parser.add_argument("--outname", '-o', default="MG_xsec", help="output file name")
    args = parser.parse_args()

    logFile = args.logFile
    outname = args.outname

    outFile = f"{outname}.txt"

    skim_gridpack_log(logFile, outFile)