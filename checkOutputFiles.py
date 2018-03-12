import os, sys
import ROOT as r
r.gROOT.SetBatch(True)
r.PyConfig.IgnoreCommandLineOptions = True
import optparse
import glob
from splitTrees import processCmd, isRootFileOk


parser = optparse.OptionParser()
parser.add_option('-d',dest ='inDir', type = str,default  = "output_T1tttt", help="Input directory with the split trees.")
parser.add_option('--resubmit',action="store_true", default=False, help = 'Resubmit failed jobs.')
options,args = parser.parse_args()



def main():


    models = glob.glob(os.path.join(options.inDir,'*'))

    failed = open("submitFailedJobs","wb")

    for aModel in models:
        model = aModel.split('/')[-1]
        filePath = os.path.join(os.path.abspath(aModel),'treeProducerSusyAlphaT','tree.root')

        if not os.path.exists(filePath) or not isRootFileOk(filePath): 
            print "File {0} is corrupted or not existing".format(filePath)
            submitScript = "/".join(filePath.split("/")[:-1]+['submitSplit'])
            failed.write('bash {0}\n'.format(submitScript))

            if options.resubmit:                
                print " ==> resubmitting the job..."
                out,err = processCmd('bash {0}'.format(submitScript))
                print out,err

    failed.close()
            
if __name__ == "__main__":
    main()
