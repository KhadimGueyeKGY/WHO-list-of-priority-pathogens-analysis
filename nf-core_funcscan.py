import argparse, os, sys
from datetime import datetime

def get_args():
    parser = argparse.ArgumentParser(prog='nf-core_funcscan.py', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="""
        + ============================================================ +
        |  European Nucleotide Archive (ENA): WHO PL                   |
        |    *Dep                                                      |
        |     -> singularity                                           |
        |     -> nextflow                                              |
        |     -> spades                                                |
        + ============================================================ +
        """)
    parser.add_argument('-i', '--InDir', help='Input Directory', type=str, required=True)
    parser.add_argument('-o', '--OutDir', help='Outout Directory', type=str, required=True)
    parser.add_argument('-p', '--platform', help='Platform', choices=['ILLUMINA','ONT'], required=True)
    args = parser.parse_args()
    return args
args = get_args()

os.system('mkdir -p '+args.OutDir)
input = args.InDir
output = args.OutDir
platform = args.platform
time = open(output+'/time.txt','w')
time.write('start\tend\n')
#-----------------------------------genome assembly
id2 = []
if platform == 'ILLUMINA':
    id = os.popen("cd "+input+"; ls *fastq.gz | cut -d '_' -f1 | sort | uniq",'r').read().split('\n')
    for i in id:
        if i != '':
            try :
                start = datetime.now()
                id2.append(i)
                R1 = input+"/"+i+"_1.fastq.gz"
                R2 = input+"/"+i+"_2.fastq.gz"
                out = output+"/"+i
                os.system("spades.py -1 "+R1+" -2 "+R2+" -o "+out)
                end = datetime.now()
                time.write(str(start)+'\t'+str(end)+'\n')
            except:
                print ("Error "+i)
else: # ONT
    id = os.popen("cd "+input+"; ls *fastq.gz",'r').read().split('\n')
    for i in id :
        if i != '':
            try:
                start = datetime.now()
                id2.append(i.split('.fastq')[0])
                R= input+"/"+i
                out = output+"/"+str(i.split('.fastq')[0])
                os.system("spades.py -s "+R+" -o "+out)
                end = datetime.now()
                time.write(str(start)+'\t'+str(end)+'\n')
            except:
                print ("Error "+i)

#-----------------------samplesheet
spt = open(output+'/samplesheet.csv','w')
spt.write('sample,fasta\n')
for i in id2:
    list = ' '.join([str(e) for e  in os.popen('ls '+output+'/'+i,'r').read().split('\n')])
    if list.find('scaffolds') != -1:
        spt.write(i+','+i+'/scaffolds.fasta\n')
spt.close()

#-----------------run nf-core/funcscan
start = datetime.now()
try:
    os.system ("cd "+output+"; nextflow run nf-core/funcscan --input samplesheet.csv --outdir nf-core_funcscan_output -profile singularity --run_amp_screening --run_arg_screening --amp_hmmsearch_models https://raw.githubusercontent.com/nf-core/test-datasets/funcscan/hmms/mybacteriocin.hmm --arg_skip_deeparg --arg_fargene_hmmmodel class_a,class_b_1_2 --igenomes_ignore")

except:
    print('Error on the nf-core/funcscan')

end = datetime.now()
time.write(str(start)+'\t'+str(end)+'\n')  
time.close()

