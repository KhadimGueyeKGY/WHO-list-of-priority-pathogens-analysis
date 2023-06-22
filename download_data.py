"""
It is more pythonic to import everything on individual lines. For example:
import argparse
import os
import sys
import pandas as pd
import random
"""
import argparse, os, sys
import pandas as pd
import random
#import requests! ####This will be useful
def get_args():
    parser = argparse.ArgumentParser(prog='download_data.py', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="""
        + ============================================================ +
        |  European Nucleotide Archive (ENA): WHO PL                   |
        |                                                              |
        + ============================================================ +
        """)
    parser.add_argument('-f', '--file', help='Taxonomy ID', type=str, required=True)
    parser.add_argument('-p', '--platform', help='Platform', choices=['ILLUMINA','ONT'], required=True)
    args = parser.parse_args()
    return args
args = get_args()
#t = args.taxo
#%22%20AND%20instrument_model=%22Illumina%20MiSeq
if args.platform == 'ILLUMINA':
    pl = 'ILLUMINA'
else :
    pl = 'OXFORD_NANOPORE'
"""
I think alot of this code below would be cleaner if you seperated out some functions and used some more defined naming strategies to make this more readable

For example, you're doing three distinct things here. 1) You're downloading the metadata csv, 2) You're processing the data to get 70 Illumina and 30 Oxford Nanopore sets, 3) You're downloading the data.

Here's an example of how to write 2 of the three functions you need to run this code.

def download_csv(url):
    try:
        return pd.read_csv(url, sep='\t')
    except Exception as e:
        print(f"Error downloading CSV: {e}")
        sys.exit(1)

def process_data(run_accession, platform):
    acc = []
    for accession in run_accession:
        file = download_csv("https://www.ebi.ac.uk/ena/portal/api/filereport?accession="+str(accession)+"&result=read_run&fields=run_accession,fastq_ftp&format=tsv&limit=0")
        fastq_ftp = file['fastq_ftp'][0]
        if platform == 'ILLUMINA' :
            if str (fastq_ftp).find(';') != -1 :
                acc.append([accession, str(fastq_ftp).split(';')])
        else: # ONT
            acc.append([accession, str(fastq_ftp)])
    return acc
    
You can see how I've separated out these functions to make them easier to read and easier to code. I've also used very granular terms to make it easier to read.

I NEED YOU TO WRITE THE 3rd FUNCTION!!

Hint of how to start....

def download_data(taxon, scientific_name, platform):
    ...
    
    
    
"""
def fonc (t,n,p):
    df= pd.read_csv("https://www.ebi.ac.uk/ena/portal/api/search?query=tax_tree("+str(t)+")%20AND%20instrument_platform=%22"+str(p)+"%22&result=read_run&limit=0&format=tsv",sep='\t')
    run_accession = list(df['run_accession'])

    #--------------------------------------selection of ID
    acc = []
    for i in range(len(run_accession)):
        file = pd.read_csv("https://www.ebi.ac.uk/ena/portal/api/filereport?accession="+str(run_accession[i])+"&result=read_run&fields=run_accession,fastq_ftp&format=tsv&limit=0",sep='\t')
        fastq_ftp = file['fastq_ftp'][0]
        if pl== 'ILLUMINA' :
            if str (fastq_ftp).find(';') != -1 :
                acc.append([run_accession[i], str(fastq_ftp).split(';')])
        else: # ONT
            acc.append([run_accession[i], str(fastq_ftp)])
    
    #-------------------------------------download
    n = open('id_'+n+'.txt','w')
    if pl== 'ILLUMINA' :
        if len (acc) > 70:
            random_acc = random.sample(acc, 70)
        else :
            random_acc = acc
        for i in random_acc : 
            n.write(i[0]+'\n')
            os.system('curl -O '+i[1][0])
            os.system('curl -O '+i[1][1])
    else : # ONT
        if len (acc) > 30:
            random_acc = random.sample(acc, 30)
        else :
            random_acc = acc
        for i in random_acc : 
            n.write(i[0]+'\n')
            os.system('curl -O '+i[1])
    n.close()



f = open(args.file,'r').read().split('\n')
for i in range(len(f)):
    if f[i] != '':
        a = f[i].split('\t')
        fonc (int(a[1]),a[0],pl)

"""
You need a main function, you should be writing all your scripts like this.

All python scripts should have a main block at the end which runs the ACTUAL functions you've written.

def main():
    args = get_args()
    .....
    
Finish this function!

Also, to call your main function and use your script directly

if __name__ == "__main__":
    main()
"""









