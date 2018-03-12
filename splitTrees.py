import os, sys
import pickle
import subprocess
import shlex
import glob
import optparse
import ROOT as r
r.gROOT.SetBatch(True)
r.PyConfig.IgnoreCommandLineOptions = True

import config_2016 as cfg

# Configurables (see config.py)
modelsDict = {
    # 'T1tttt'  :cfg.info_T1tttt,
    # 'T2bb'    :cfg.info_T2bb
    'T1bbbb'   : cfg.info_T1bbbb,
    'T1qqqq'   : cfg.info_T1qqqq,
    'T2tt'     : cfg.info_T2tt,
    }

exe = os.path.join(os.environ['PWD'],'cutTreeSusy')

templSkimreport =  'Counter SkimReport :\n'
templSkimreport += '	 All Events                                   {0} 	 1.00 	 1.0000\n'
templSkimreport += '	 Sum Weights                                  {0:.4f}  	 0.00 	 1.0000\n'


# Utils

def parse_args():
    parser = optparse.OptionParser()
    parser.add_option('-c',dest ='copyToLocal', default  = False, action="store_true", help="Copy input tree to local node")
    parser.add_option('-n',dest ='dryRun', default  = False, action="store_true", help="Do not submit")
    options,args = parser.parse_args()
    return options 


def isRootFileOk(fileName):

    isOK = False
    if os.path.exists(os.path.abspath(fileName)):
        # r.gErrorIgnoreLevel=r.kError
        r.gErrorIgnoreLevel=r.kSysError
        tf = r.TFile(os.path.abspath(fileName),"READ")
        if not (tf.IsZombie() or tf.TestBit(r.TFile.kRecovered)): isOK = True
        tf.Close()

    return isOK


def processCmd(cmd):

    args = shlex.split(cmd)
    sp = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = sp.communicate()
    if sp.returncode != 0: print out, err

    return out, err


# Stupid function to submit to queue
def submit(inTree,outDir,susyBName,mSusyMin,mSusyMax,mLspMin,mLspMax,exe,dry=False,copyToLocal=False,fromEOS=False):

    stdout = os.path.join(outDir,'split_STDOUT')
    stderr = os.path.join(outDir,'split_STDERR')
    copyCommand = "cp {0} ./inTree.root".format(inTree) if copyToLocal else "ln -fs {0} ./inTree.root".format(inTree)
    if fromEOS: copyCmd = "echo \"Using xrootd from EOS\""
    subCmd = 'qsub -q hep.q -l h_rt=3600 -o {0} -e {1} -v inTree={2},outDir={3},susyBName={4},mSusyMin={5},mSusyMax={6},mLspMin={7},mLspMax={8},atDir={9},exe={10},copyCmd=\"{11}\" {12}'.format(stdout,stderr,inTree,outDir,susyBName,mSusyMin,mSusyMax,mLspMin,mLspMax,os.environ['ALPHATOOLSDIR'],exe,copyCommand,os.path.join(os.environ["PWD"],'split.pbs'))
    if not dry:
        print '  ==> submitting splitting for {0}'.format(outDir.split('/')[-2])
        print '      output directory: {0}'.format(outDir)
        out, err = processCmd(subCmd)
        print out, err
    return subCmd



def main():

    # Parse arguments
    opt = parse_args()

    # Check if the executable exists
    if not os.path.exists(exe):
        print 'The executable does not exist! Did you compile?'
        sys.exit(1)

    for model,info in modelsDict.iteritems():

        # Open root file with gen mass info and read the histogram
        tf_genEvts = r.TFile(info.genEvtsFile,'READ')


        baseOutSplitDir = 'SMS-{0}_m{1}-{2}_mLSP-{3}_25ns'

        hName = 'h_{0}_LSP'.format(info.sparticle)
        h_genEvts = tf_genEvts.Get(hName)

        fromEos = False
        if info.baseInDir.startswith("root://"): fromEos = True
        
        if not fromEos: paths = glob.glob(info.baseInDir+'/*'+model+'*')
        else: paths = info.baseInDir
        datasets = [i.split('/')[-1] for i in paths]
    

        for point in datasets:
        # for point in ['SMS-T1tttt_mGluino-1450to1475_mLSP-50to1075_25ns']:
            
            print 'Running splitting for dataset {0}'.format(point)
        
            # Input tree
            if not fromEos: 
                inDir = os.path.join(info.baseInDir,point)
                inTree = os.path.join(inDir,'treeProducerSusyAlphaT','tree.root')
            else: 
                inDir = info.baseInDir
                inTree = info.baseInDir
    
            # Read the gen mass info
            massInfoPkl = os.path.join(info.massInfoDir,point,'susyMassInfo.pkl')
            massDict = pickle.load( open(massInfoPkl,'rb') )

            for mSusy in massDict.keys():
                for mLSP in massDict[mSusy].keys():
            # for mSusy in [1300]:
            #     for mLSP in [100]:

                    baseDirMassPoint = os.path.join(info.baseOutDir,baseOutSplitDir.format(model,info.sparticle,int(mSusy),int(mLSP)))            

                    # Run the tree splitting
                    outDir = os.path.join(baseDirMassPoint,'treeProducerSusyAlphaT')
                    if not os.path.exists(outDir): os.makedirs(outDir)
                    treePath = os.path.join(outDir,'tree.root')
                    if os.path.exists(treePath) and isRootFileOk(treePath): 
                        print "Skipping point mSusy={0} mLSP={1} because tree already exists".format(mSusy,mLSP)
                        continue
                    susyBName = "GenSusyM{0}".format(info.sparticle)
                    subCmd = submit(inTree,outDir,susyBName,str(mSusy-5),str(mSusy+5),str(mLSP-5),str(mLSP+5),exe,opt.dryRun,opt.copyToLocal,fromEos)
                    # print subCmd

                    # Write the qsub command (useful for resubmission)
                    subCmdPath = os.path.join(outDir,'submitSplit')
                    with open(subCmdPath,"wb") as f: f.write("#!/bin/bash\n"+subCmd+"\n")

                    # Write the skim report
                    outDirSkim = os.path.join(baseDirMassPoint,'skimAnalyzerCount')
                    if not os.path.exists(outDirSkim): os.makedirs(outDirSkim)
                    skimReportPath = os.path.join(outDirSkim,'SkimReport.txt')
                    if os.path.exists(skimReportPath): os.remove(skimReportPath)
                    nGenEvts = h_genEvts.GetBinContent(h_genEvts.FindBin(mSusy,mLSP))
                    skimReportStr = templSkimreport.format(int(nGenEvts),nGenEvts)
                    with open(skimReportPath,'wb') as f: f.write(skimReportStr)
                    print '  Skim report written at {0}'.format(skimReportPath)


    tf_genEvts.Close()


if __name__ == "__main__": main()
