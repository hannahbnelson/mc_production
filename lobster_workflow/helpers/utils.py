import re
import subprocess

# Match strings using one or more regular expressions
def regex_match(lst,regex_lst):
    # NOTE: We don't escape any of the regex special characters!
    # TODO: Add whitelist/blacklist option switch
    matches = []
    if len(regex_lst) == 0:
        return lst[:]
    for s in lst:
        for pat in regex_lst:
            m = re.search(r"%s" % (pat),s)
            if m is not None:
                matches.append(s)
                break
    return matches

# Pipes subprocess messages to STDOUT
def run_process(inputs,verbose=True,indent=0):
    # Note: This will hold the main thread and wait for the subprocess to complete
    indent_str = "\t"*indent
    p = subprocess.Popen(inputs,stdout=subprocess.PIPE)
    stdout = []
    while True:
        l = p.stdout.readline()
        if l == '' and p.poll() is not None:
            break
        if l:
            stdout.append(l.strip())
            if verbose: print indent_str+l.strip()
    return stdout