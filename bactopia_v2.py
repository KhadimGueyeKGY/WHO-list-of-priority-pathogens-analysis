import argparse, os,sys
from datetime import datetime
#import pandas as pd
#import random

VERSION = "2.0.0"
PROGRAM = "bactopia"

def get_args():
    parser = argparse.ArgumentParser(prog='bactopia_v2.py', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="""
        + ============================================================ +
        |  European Nucleotide Archive (ENA): WHO PL ==> Bactopia V.2  |
        |                                                              |
        + ============================================================ +
        """)
    parser.add_argument('-i', '--input', help='Input directory', type=str, required=True)
    parser.add_argument('-o', '--output', help='Output directory', type=str, required=True)
    parser.add_argument('--version', action='version', help='show program\'s version number and exit ', version=f'{PROGRAM} v{VERSION}')
    args = parser.parse_args()
    return args
args = get_args()

input = args.input
output = args.output

os.system('bactopia prepare '+input+' > '+input+'/ID.txt')
os.system('bactopia --fastqs --samples '+input+'/ID.txt --datasets datasets --outdir '+output+' --genome_size 2200000 --min_reads 1 --bactopia '+output+' --wf amrfinderplus')
os.system('rm '+input+'/ID.txt')




