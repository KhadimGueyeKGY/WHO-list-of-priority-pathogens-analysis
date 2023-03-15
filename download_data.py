import argparse, os, sys
import pandas as pd
import random

def get_args():
    parser = argparse.ArgumentParser(prog='download_data.py', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="""
        + ============================================================ +
        |  European Nucleotide Archive (ENA): WHO PL                   |
        |                                                              |
        + ============================================================ +
        """)
    #parser.add_argument('-t', '--taxo', help='Taxonomy ID', type=int, required=True)
    parser.add_argument('-f', '--file', help='Taxonomy ID', type=str, required=True)
    ''' Tab file
        scientific name   Taxon
    '''
    #parser.add_argument('-n', '--name', help='Scientific name', type=str, required=False)
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











