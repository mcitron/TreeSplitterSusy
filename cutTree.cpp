// usage: 
// ./cutTreeSusy <input_tree> <out_dir> <m_SUSY_min> <m_SUSY_max> <m_LSP_min> <m_LSP_max>

#include "TFile.h"
#include "TROOT.h"
#include "TTree.h"
#include "TChain.h"
#include "TObjString.h"

#include <iostream>
#include <fstream>
#include <string>
#include <stdlib.h>


// main
int main(int argc, char *argv[]){
  
  TString inFileName = argv[1];
  TString outDir = argv[2];
  TString susyBName = argv[3];
  TString susyMassMin = argv[4];
  TString susyMassMax = argv[5];
  TString lspMassMin = argv[6];
  TString lspMassMax = argv[7];

  TChain *chain = new TChain("tree");
  chain->Add(inFileName);
  chain->GetEntry(0); 
  
  int nentries = int(chain->GetEntries());
  std::cout << "+++++ No. of entries in the input tree: " << nentries << std::endl;

  TString susyMassCut = susyBName + " > "+susyMassMin+" && " + susyBName + " < "+susyMassMax;
  TString lspMassCut = "GenSusyMNeutralino > "+lspMassMin+" && GenSusyMNeutralino < "+lspMassMax;
  TString cut = susyMassCut+" && "+lspMassCut;

  TString outFileName = ((TObjString*)(inFileName.Tokenize("/"))->Last())->String();

  TFile* fileTreeOut = TFile::Open(outDir+"/"+outFileName,"RECREATE");
  fileTreeOut->cd();
  
  // TTree *newtree = chain->CopyTree(cut,"",maxEntries); // use a sub-sample this when debugging
  TTree *newtree = chain->CopyTree(cut);
  newtree->AutoSave();

  nentries = int(newtree->GetEntries());
  std::cout << "+++++ No. of entries in the output tree: " << nentries << std::endl;

  fileTreeOut->Write();
  fileTreeOut->Close();

  delete chain;

  
  return 0;
}
