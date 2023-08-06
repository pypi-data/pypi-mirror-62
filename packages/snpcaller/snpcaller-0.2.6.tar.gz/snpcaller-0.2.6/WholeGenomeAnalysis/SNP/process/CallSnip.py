def getSnipPosition(bam,jsondata):
    for sequence in bam:
        if (hasattr(sequence, 'reference_name')):
            print(sequence.reference_name)
            for snp in jsondata['SNP']:
                if(snp['chrom'] == sequence.reference_name):
                    print


    for sequence in bam:
        if (hasattr(sequence, 'reference_name')):
            start=sequence.pos
            end=sequence.pos+len(sequence.seq)
            for snp in data['SNP']:
                if(snp['chrom'] == sequence.reference_name):
                    chromStart=snp['chromStart']
                    chromEnd=snp['chromEnd']
                    if(start < chromStart <  end and start < chromEnd < end):
                        AmpliconName=sequence.query_name.split('#')[2]
                        rawReads = sequence.query_name.split('#')[4]
                        targetPositionStart=chromStart-start
                        targetPositionEnd=chromEnd-start

                        rawbases=sequence.seq[targetPositionStart:targetPositionEnd]
                        print(BlotName+','+SampleName+','+AmpliconName+','+rawReads+','+snp['name']+','+snp['chrom']+','+str(chromStart)+','+str(chromEnd)+','+snp['refNCBI']+','+snp['refUCSC']+','+snp['observed']+','+rawbases)

def CigarCalculation(targetPositionStart, targetPositionEnd, cigar):
    calPositionStart = 1
    returnStart = targetPositionStart
    returnEnd = targetPositionEnd

    targetBaseCount = targetPositionEnd - targetPositionStart

    baseMark = 'M'

    #if(len(cigar) > 1):
    #    print(cigar)
    # Cigar value 0 is mutation, 1 is Insertion , 2 is Deletion.
    for arrCigar in cigar:
        #Check is Instance because sometimes bamnostic return (('BAM_CMATCH',0),1) like this.
        if(isinstance(arrCigar[0],list)):
            mutationType=arrCigar[0][1]
        else:
            mutationType=arrCigar[0]

        value=arrCigar[1]

        if(returnStart == calPositionStart and targetBaseCount == 0):
            if (mutationType == 1):
                # returnStart = targetPositionStart + value
                returnEnd = returnEnd + value
                calPositionStart = calPositionStart + value
                baseMark='I'

            return returnStart, returnEnd, baseMark
        elif (returnStart+1 == calPositionStart and targetBaseCount == value and mutationType == 2):
            if (mutationType == 2):
                # returnStart = targetPositionStart + value
                baseMark = 'D'

            return returnStart, returnEnd, baseMark
        elif(returnStart > calPositionStart):
            if(mutationType==0):
                calPositionStart=calPositionStart+value
            elif(mutationType==1):
                returnStart = returnStart + value
                returnEnd = returnEnd + value
                calPositionStart = calPositionStart+value
            elif(mutationType==2):
                returnStart=returnStart-value
                returnEnd=returnEnd-value
                #calPositionStart=calPositionStart-value
        else:
            return returnStart,returnEnd,baseMark

    return returnStart, returnEnd, baseMark

def CigarInsertionCount(cigar):
    # Cigar value 0 is mutation, 1 is Insertion , 2 is Deletion.

    insertionCount = 0
    for arrCigar in cigar:
        if(isinstance(arrCigar[0],list)):
            mutationType=arrCigar[0][1]
        else:
            mutationType=arrCigar[0]

        if (mutationType == 1):
            insertionCount = insertionCount + 1

    return insertionCount

def filterSnipObject(snip_dic,snip_totalReads, trimpercentage):
    final_snp_list = {}
    snip_result = {}
    # Filter Rawreads by Cut Off
    for snip, snip_observe  in snip_dic.items():
        cutoff = snip_totalReads[snip] * trimpercentage
        for observe, snp in snip_observe.items():
            if(float(snp.rawReads) < cutoff):
                snp.isValid = 0

    for snip, snip_observe  in snip_dic.items():
        # If snip position is more than two, we will not allow to have
        #if (len(snip_observe.keys()) < 3):
        for observe, snp in snip_observe.items():
            validCount=0
            for tempobserve, tempsnp in snip_observe.items():
                if(tempsnp.isValid==1):
                    validCount = validCount+1
                else:
                    print("isValid == 0 : " + str(tempsnp.seqName))

            if(validCount > 2):
                continue

            #If It is not valid sequence, It is skipped.
            if(snp.isValid == 0):
                continue

            if (snip in final_snp_list):
                dicSnipDetail = final_snp_list[snip]
                if (observe in dicSnipDetail):
                    getSnip = dicSnipDetail[observe]
                    dicSnipDetail[observe] = getSnip

                else:
                    dicSnipDetail[observe] = snp
            else:
                dicSnipDetail = {}
                dicSnipDetail[observe] = snp
                final_snp_list[snip] = dicSnipDetail

    return final_snp_list



