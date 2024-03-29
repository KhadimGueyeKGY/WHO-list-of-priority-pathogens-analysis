import argparse, os,sys
from datetime import datetime
#import pandas as pd
#import random

def get_args():
    parser = argparse.ArgumentParser(prog='download_data.py', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="""
        + ============================================================ +
        |  European Nucleotide Archive (ENA): WHO PL ==> Bactopia      |
        |                                                              |
        + ============================================================ +
        """)
    parser.add_argument('-i', '--input', help='Input directory', type=str, required=True)
    #parser.add_argument('-o', '--output', help='Output directory', type=str, required=True)
    parser.add_argument('-p', '--platform', help='Platform', choices=['ILLUMINA','ONT'], required=True)
    args = parser.parse_args()
    return args
args = get_args()
#os.system('mkdir -p '+str(args.output))
fastq_file = os.popen('cd '+str(args.input)+'; ls *fastq.gz').read().split("\n")
if args.platform == 'ILLUMINA':
    for i in range(0,len(fastq_file),2):        
        if fastq_file != '':
                start = datetime.now()
                id1 = fastq_file[i].split('.')[0]
                id2 = fastq_file[i+1].split('.')[0]
                if str(id1).find('_')!= -1 :
                    id =str(id1).split('_')[0]
                else:
                    id = id1
                #os.system('mkdir -p '+str(args.output)+'/'+str(id))
                time = open(str(id)+'_time.txt','w')
                try :
                    R1 = str(args.input)+'/'+str(fastq_file[i])
                    R2 = str(args.input)+'/'+str(fastq_file[i+1])
                    SAMPLE = str(id)
                    os.system('singularity exec staphopia_20200127.sif staphopia.py --fq1 '+R1+' --fq2 '+R2+' --sample '+SAMPLE)
                except:
                    print('Error '+str(id))
                end = datetime.now()
                time.write(str(start)+'\t'+str(end)+'\n')
        time.close()
else :
    for i in range(len(fastq_file)):
        if fastq_file != '':
            start = datetime.now()
            id = fastq_file[i].split('.')[0]
            if str(id).find('_')!= -1 :
                id = str(id).split('_')[0]
            #os.system('mkdir -p '+str(args.output)+'/'+str(id))
            time = open(str(id)+'_time.txt','w')
            try :
                R = str(args.input)+'/'+str(fastq_file[i])
                SAMPLE = str(id)
                os.system('singularity exec staphopia_20200127.sif staphopia.py --fq1 '+R+' --sample '+SAMPLE)
            except:
                print('Error '+str(id))
            end = datetime.now()
            time.write(str(start)+'\t'+str(end)+'\n')
        time.close()




