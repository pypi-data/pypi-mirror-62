import bamnostic as bs
import argparse
import os.path
import json
import csv

from WholeGenomeAnalysis.SNP.model.AutoTypingResult import AutoTypingResult
from WholeGenomeAnalysis.SNP.model.Sample import Sample
from WholeGenomeAnalysis.SNP.model.Amplicon import Amplicon
from WholeGenomeAnalysis.SNP.model.SequenceObject import SequenceObject
from WholeGenomeAnalysis.SNP.process import CallSnip as callsnip
from WholeGenomeAnalysis.SNP.model.Snp import Snp
from WholeGenomeAnalysis.SNP.process import QualityCalculation as qualityCalculation
from WholeGenomeAnalysis.SNP.reader import reader as reader
from pathlib import Path
from WholeGenomeAnalysis.SNP.writer import writer as write
# from WholeGenomeAnalysis.SNP.model.Vcf import Vcf
from WholeGenomeAnalysis.SNP.process import runConvert

parser = argparse.ArgumentParser(description='Input for Snip program')

parser.add_argument("-s", "--snpJsonpath", help='input snp json file path', required=True, dest="snpJsonpath")
parser.add_argument("-j", "--jsonpath", help='input json file path (output json from the sample processor program', required=True, dest="jsonPath")
parser.add_argument("-b", "--bampath", help='input bam file path', required=True, dest="bamPath")
parser.add_argument("-o", "--outfolder",help='output folder location', required=True, dest="outfolder")
parser.add_argument("-v", "--vcf", help='vcf head information path', required=True, dest="vcfpath")
parser.add_argument("-t", "--trimPercent", help='trim percentage within the sequence', required=True, dest="trimPercent")
parser.add_argument("-c", "--cnvDataPath", help='CNV Json file required as input', required=True, dest="cnvDataPath")

complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}

args = parser.parse_args()

if (os.path.exists(args.snpJsonpath)):
    print("File exist : " + args.snpJsonpath)
else:
    print("Missing json file : " + args.snpJsonpath)
    exit()

if (os.path.exists(args.bamPath)):
    print("File exist : " + args.bamPath)
else:
    print("Missing bam file : " + args.bamPath)
    exit()

#if (os.path.exists(args.jsonPath)):
#    print("File exist : " + args.jsonPath)
#else:
#    print("Missing bam json : " + args.jsonPath)
#    exit()

#os.mkdir(args.outfolder, exist_ok=True)


if (os.path.exists(args.outfolder)):
    print("Folder exist : " + args.outfolder)
else:
    print("Created path : " + args.outfolder)
    os.mkdir(args.outfolder)

if (os.path.exists(args.vcfpath)):
    print("File exist : " + args.vcfpath)
else:
    print("Missing vcf header file : " + args.vcfpath)
    exit()

snpJsonpath = args.snpJsonpath
bamPath = args.bamPath
jsonpath = args.jsonPath
cnvPath = args.cnvDataPath
trimPercent = float(args.trimPercent)

snpData = reader.JsonReader(snpJsonpath)
experimentData = reader.JsonReader(jsonpath)
cnvData = reader.JsonReader(cnvPath)
bam = bs.AlignmentFile(bamPath, 'rb')

# copiedbam = copy.copy(bam)

# for snp in data['SNP']:
#     print('name : ' + snp['name'])

snpVersion = snpData['SNPVERSION']
targetSnpVersion = snpData['VERSION']
jobName = experimentData['jobName']
experimentName = experimentData['experimentName']
sampleID = experimentData['sampleID']
barcodeID = experimentData['barcodeID']
experimentID = experimentData['experimentID']

# Create output path

#outputpath = args.outfolder+'/'+"par"+'.csv'
outputpath = Path(args.outfolder+'/'+sampleID+".csv")
outputpath_vcf = Path(args.outfolder+'/'+sampleID+".vcf")

print("output csv path : " + str(outputpath))
print("output vcf path : " + str(outputpath_vcf))
#outputfile = writer.csvWriter(outputpath)


# sorted_bam = sorted(bam.head(), key=operator.itemgetter(1), reverse=True)

# for reading in enumerate(bamtmp):
#     print(reading)
# Result = {}
# AmpliconList = {}

# for sequence in copiedbam:
#     if (hasattr(sequence, 'reference_name')):
#         if sequence.query_name.startswith('SNP'):
#             AmpliconName = sequence.query_name.split('#')[2]
#             AmpliconList[AmpliconName] = Amplicon(AmpliconName)

autoResult = AutoTypingResult(snpVersion, targetSnpVersion)
smpl = Sample(experimentID, experimentName, '', sampleID)

snip_dic = {}
snip_totalReads = {}


#with open(outputpath, mode='w', newline='') as csv_file:
#    fieldnames = ['experimentName', 'sampleId', 'seqName', 'rawReads', 'snpName', 'chrom', 'chromStart', 'chromEnd',
#                  'refNCBI', 'refUCSC', 'targeted', 'observed', 'minBaseOcurrances', 'minBasePercentages',
#                  'minBaseQualityPercentage']
#    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#    writer.writeheader()

for sequence in bam:
    if (hasattr(sequence, 'reference_name')):
        #if sequence.query_name.startswith('SNP'):
            arrObject = []

            start = sequence.pos
            end = sequence.pos + len(sequence.seq)
            if(sequence.flag == 16):
                strand = '-'
            else:
                strand = '+'

            sObject = SequenceObject(start,end,sequence.cigar,sequence.seq,sequence.reference_name)
            arrObject.append(sObject)

            xa=''
            if "XA" in sequence.tags:
                xa = sequence.tags.get("XA")[1]

            if(";" in xa):
                pair_list = xa.split(";")
                for pair in pair_list:
                    if(pair != ''):
                        comma_list = pair.split(",")
                        newReferenceName=comma_list[0]
                        newstrand=comma_list[1][0:1]
                        newstart=int(comma_list[1][1:])
                        newend=int(comma_list[1][1:]) + len(sequence.seq)
                        newcigar=bs.utils.parse_cigar(comma_list[2])

                        if(strand == newstrand):
                            newSequence = sequence.seq
                        else:
                            newSequence = "".join(complement.get(base,base) for base in reversed(sequence.seq))

                        arrObject.append(SequenceObject(newstart,newend,newcigar,newSequence,newReferenceName))

            # print("1. reference_name: " + sequence.reference_name + " | 1. sequence.query_name: " + sequence.query_name)
            # print("1. sequence.read_name: " + sequence.read_name)
            # dt = {}
            print("Name : " + sequence.query_name)
            AmpliconName = "CYP"
            amp = Amplicon(AmpliconName)

            for matchObject in arrObject:
                matchStart, matchEnd, matchCigar, matchSeq, matchChr = matchObject.get()

                for snip in snpData['SNP']:
                    if (snip['chrom'] == matchChr):
                        # print("2. reference_name: " + sequence.reference_name)v
                        # print("2. sequence.query_name: " + sequence.query_name)
                        if( 'rs16947' in snip['name'] and 'NumReads442' in sequence.query_name):
                            print("rs1135822")

                        chromStart = snip['chromStart']
                        chromEnd = snip['chromEnd']

                        if (matchStart < chromStart < matchEnd and matchStart < chromEnd < matchEnd):
                            # print("1. reference_name: " + sequence.reference_name + " | 1. sequence.query_name: " + sequence.query_name)

                            # AmpliconName = sequence.query_name.split('#')[2]

                            #Noise filtering if insertions are more than 10 in the sequence.
                            #Trim that sequence out.

                            insertionCount = callsnip.CigarInsertionCount(matchCigar)
                            if (insertionCount > 10):
                                continue

                            rawReads = sequence.query_name.split('NumReads')[1]
                            targetPositionStart = chromStart - matchStart
                            targetPositionEnd = chromEnd - matchStart
                            print("targetPositionStart : " + str(targetPositionStart) + " | targetPositionEnd: " + str(targetPositionEnd))
                            calStart, calend,baseMark = callsnip.CigarCalculation(targetPositionStart, targetPositionEnd, matchCigar)
                            print("start : " + str(calStart) + " | end: " + str(calend))

                            rawbases = matchSeq[calStart:calend]

                            if(baseMark=='D'):
                                rawbases='-'
                                #for i in range(calend-calStart):
                                #    rawbases=rawbases+'-'

                            if (calStart == calend and rawbases == ''):
                                rawbases = '-'

                            #minBaseOcurrances, minBasePercentages, minBaseQualityPercentage = qualityCalculation.getQuality(qualityData, rawbases, calStart, calend, sequence.query_name)
                            minBaseOcurrances, minBasePercentages, minBaseQualityPercentage = 100,100,100
                            #rawbases = sequence.seq[targetPositionStart:targetPositionEnd]

                            snps = Snp(1, sequence.query_name, rawReads, snip['name'], snip['chrom'].replace("chr", ""),
                                       str(chromStart), str(chromEnd), snip['refNCBI'], snip['refUCSC'],
                                       snip['observed'], rawbases, str(minBaseOcurrances), str(minBasePercentages),
                                       str(minBaseQualityPercentage), sequence)

                            # dt.update(vars(snps))
                            # dt = json.dumps(dt)

                            if (snip['name'] in snip_dic):
                                dicSnipDetail = snip_dic[snip['name']]
                                if (rawbases in dicSnipDetail):
                                    getSnip = dicSnipDetail[rawbases]

                                    getSnip.rawReads = int(getSnip.rawReads) + int(snps.rawReads)
                                    getSnip.minBaseOcurrances = int(getSnip.minBaseOcurrances) + int(snps.minBaseOcurrances)

                                    if (getSnip.minBasePercentages > snps.minBasePercentages):
                                        getSnip.minBasePercentages = snps.minBasePercentages
                                    if (getSnip.minBasePercentages > snps.minBasePercentages):
                                        getSnip.minBasePercentages = snps.minBasePercentages
                                    if (getSnip.minBaseQualityPercentage > snps.minBaseQualityPercentage):
                                        getSnip.minBaseQualityPercentage = snps.minBaseQualityPercentage

                                    # lstSnip.append(snps)
                                    dicSnipDetail[rawbases] = getSnip
                                else:
                                    # lstSnip = []
                                    # lstSnip.append(snps)
                                    dicSnipDetail[rawbases] = snps
                            else:
                                # lstSnip = []
                                dicSnipDetail = {}
                                # lstSnip.append(snps)
                                dicSnipDetail[rawbases] = snps
                                snip_dic[snip['name']] = dicSnipDetail

                            if (snip['name'] in snip_totalReads):
                                snip_totalReads[snip['name']] = int(snip_totalReads[snip['name']])+int(rawReads)
                            else:
                                snip_totalReads[snip['name']] = int(rawReads)


                            #amp.add(snps)
                            #writer.writerow({'experimentName': experimentName, 'sampleId': sampleID, 'seqName': sequence.query_name, 'rawReads': rawReads, 'snpName': snip['name'], 'chrom': snip['chrom'], 'chromStart': str(chromStart), 'chromEnd': str(chromEnd), 'refNCBI': snip['refNCBI'], 'refUCSC': snip['refUCSC'], 'targeted': snip['observed'], 'observed': rawbases, 'minBaseOcurrances': str(minBaseOcurrances), 'minBasePercentages': str(minBasePercentages), 'minBaseQualityPercentage': str(minBaseQualityPercentage)})

                            print(experimentName + ',' + sampleID + ',' + sequence.query_name + ',' + rawReads + ',' + snip[
                                'name'] + ',' + snip['chrom'] + ',' + str(chromStart) + ',' + str(chromEnd) + ',' + snip[
                                      'refNCBI'] + ',' + snip['refUCSC'] + ',' + snip['observed'] + ',' + rawbases  + ',' + str(minBaseOcurrances) + ',' + str(minBasePercentages) + ',' + str(minBaseQualityPercentage))
                            isTargeted = True


                # AmpliconName = sequence.query_name.split('#')[2]
                # amp = Amplicon(AmpliconName)

                # if AmpliconName in AmpliconList:
                #     amp = AmpliconList[AmpliconName] # Get Amplicon object by AmpliconName
                #     amp.add(dt)

                #if isTargeted == True:
                #    smpl.add(amp)
                #else:
                #    print("None Target List: " + sequence.query_name)

final_snp_list = callsnip.filterSnipObject(snip_dic, snip_totalReads, trimPercent)

############### CNV Logic

isPassed = 0

for cnv in cnvData:
    if(cnv['ExperimentName'] == experimentName and cnv['ClientSampleID'] == sampleID):
        for snip in snpData['SNP']:
            if( cnv['SNPName'] == snip['name'] ):
                snps = Snp(1, '', cnv['CNV'], cnv['SNPName'], snip['chrom'].replace("chr", ""), snip['chromStart'], snip['chromEnd'],
                           snip['refNCBI'], snip['refUCSC'], snip['observed'], '<CNV>',
                           str(0), str(100), str(100), '')

                dicSnipDetail = {}
                # lstSnip.append(snps)
                dicSnipDetail['CNV'] = snps
                final_snp_list[cnv['SNPName']] = dicSnipDetail
                isPassed = 1
                break

    if(isPassed == 1):
        break


#########################


write.csvWriter(outputpath, final_snp_list, experimentName,sampleID)

# print("sampleID", sampleID)
# for name in sorted(final_snp_list):
#     print("name", name)
#     for base, snp in final_snp_list[name].items():
#         print(base, snp.rawReads, snp.snpName, snp.chrom, snp.chromStart, snp.chromEnd, snp.refNCBI, snp.refUCSC, snp.observed, snp.rawBases)


converter = runConvert.Converter()
vcfs = converter.convert(final_snp_list, sampleID)
header = reader.VCFReader(args.vcfpath, sampleID)

write.TextWriter(outputpath_vcf, header)
write.VCFWriter(outputpath_vcf, vcfs)



#autoResult.add(smpl)

#autoResult.autoTyping_dic = {}
#autoResult.autoTyping_dic["snpVersion"] = autoResult.snpVersion
#autoResult.autoTyping_dic["targetSnpVersion"] = autoResult.targetSnpVersion
#autoResult.autoTyping_dic["sample"] = autoResult.sample_list

#Convert_Json = {
#    "autoTypingResult": autoResult.autoTyping_dic
#}

#jsonFormat = json.dumps(Convert_Json, indent=4)
#print(jsonFormat)

