#!/bin/sh

inDir=$1
model=$2

hadd -f genEvtsPerMass_${model}.root $inDir/*${model}*/susyParameterScanAnalyzer/genEvtsPerMass.root