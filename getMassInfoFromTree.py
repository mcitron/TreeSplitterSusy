# FIXME: so far assume gluino models

#!/usr/bin/python
import optparse
import os, sys
import ROOT as r
r.gROOT.SetBatch(True)
r.PyConfig.IgnoreCommandLineOptions = True
import pickle


parser = optparse.OptionParser()
parser.add_option('-d',dest ='inDir', type = str,default  = None, help="Input directory with the tree")
parser.add_option('-o',dest ='outDir', type = str,default  = None, help="Output directory where the pkl file will be stored")
parser.add_option('--sparticle',dest ='sparticle', type = str,default  = None, help="Sparticle (needed to get the right branch in the tree).")
options,args = parser.parse_args()



def main():

    if not os.path.exists(options.outDir): os.mkdir(options.outDir)

    # Check if the file already exists...
    outFile = os.path.join(options.outDir,'susyMassInfo.pkl')
    if os.path.exists(outFile):
        print 'File already exists! {0}, will remove it'.format(outFile)
        os.remove(outFile)
    

    outDict = {}
    
    treeFilePath = os.path.join(options.inDir,'treeProducerSusyAlphaT','tree.root')
    if not os.path.exists(treeFilePath):
        print 'File {0} not found!'.format(treeFilePath)
        sys.exit(1)
    tree = r.TChain('tree')
    tree.Add(treeFilePath)
    tree.SetBranchStatus('*',0)
    susyBranch = 'GenSusyM{0}'.format(options.sparticle)
    tree.SetBranchStatus(susyBranch,1)
    tree.SetBranchStatus('GenSusyMNeutralino',1)

    iEntry = 0
    while tree.GetEntry(iEntry):
        if iEntry%10000==0: print 'Processing evt {0}'.format(iEntry)
        mSusy = getattr(tree,susyBranch)
        mLSP = tree.GenSusyMNeutralino

        if not mSusy in outDict.keys(): outDict[mSusy] = {}
        if not mLSP in outDict[mSusy].keys(): outDict[mSusy][mLSP] = 0
        outDict[mSusy][mLSP] += 1

        iEntry += 1


    pickle.dump(outDict,open(outFile,'wb'))
    print 'Output file created: {0}'.format(outFile)

    return True
    

if __name__ == "__main__": main()
