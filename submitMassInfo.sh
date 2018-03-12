#!/bin/sh

inDir=$1
outDir=$2
model=$3
sparticle=$4

mkdir -p $outDir

for i in $( ls -d ${inDir}/*${model}* | xargs -n 1 basename); do 
# for i in SMS-T1tttt_mGluino-1525to1550_mLSP-1to1300_25ns; do
    echo "Will submit mass info for dataset ${i}"
    inSubDir=${inDir}/${i}
    outSubDir=${outDir}/${i}
    mkdir -p $outSubDir
    qsub -q hep.q -o ${outSubDir}/STDOUT -e ${outSubDir}/STDERR -v dir=${inSubDir},atdir=${ALPHATOOLSDIR},out=${outSubDir},sparticle=${sparticle} getMassInfo.pbs
done

