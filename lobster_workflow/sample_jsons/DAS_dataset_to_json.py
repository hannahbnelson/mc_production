import os
import json
import argparse
import subprocess
import shlex

def make_json_file(dataset, fileName):
    outputFile = fileName+'.json'
    print(f"Using output filename: {outputFile}")
    if os.path.exists(outputFile):
        assert not os.path.exists(outputFile), "Output file will not be overwritten! Backup the file and try again."

    dbs_out = []
    dbs_out.extend(
        subprocess.run(
            shlex.split(f'dasgoclient -query "file dataset={dataset}"'),
            stdout = subprocess.PIPE,
            universal_newlines = True).stdout.split("\n")[:-1]
        )

    print("length of dbs file list: ", len(dbs_out))

    ## Dump datasets/files dict to JSON
    with open(outputFile, "w") as f:
        json.dump(
            {'DAS dataset': dataset, 'files':dbs_out},
            f,
            indent = 4,
            sort_keys=True
        )
        print(f"Dumped JSON to {outputFile}!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command line options parser")
    parser.add_argument("jsonFile", help="Json that holds datasets and output file pairs: {outputFile_name: DAS dataset}")
    args = parser.parse_args()

    jsonFile = args.jsonFile
    with open(jsonFile) as jf: 
        datasets = json.load(jf)

    for item in datasets: 
        make_json_file(datasets[item], item)


