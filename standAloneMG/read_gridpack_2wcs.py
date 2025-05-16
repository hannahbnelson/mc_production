'''
This file reads the section of a gridpack log that lists the reweight points 
and correpsonding cross section. 
The input file should be of the form:
	INFO: Computed cross-section:
	INFO: EFTrwgt0_cHQ3_m10p0_ctGIm_m1p0 : 1.02474572678 +- 0.0539780414803 pb
	INFO: EFTrwgt10_cHQ3_m7p0_ctWRe_m2p0 : 1.86402905804 +- 0.138341576675 pb
	INFO: EFTrwgt11_cHQ3_m7p0_cleQt3Re_5p0 : 1.98565143144 +- 0.0067008932902 pb
	...
The output file will be of the form: 
	cHQ3_m10p0_ctGIm_m1p0
	1.02474572678 +- 0.0539780414803 pb
	cHQ3_m7p0_ctWRe_m2p0
	1.86402905804 +- 0.138341576675 pb
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
					line = line[9:]
					line = line.split(":")

					wc_key = line[0].split("_", 1)
					wc_name = wc_key[1]

					xsec = line[1][1:]

					out += f"{wc_name}\n{xsec}"

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