from collections import namedtuple

info = namedtuple("info","sparticle baseInDir baseOutDir genEvtsFile massInfoDir")


info_T2tt = info(
    sparticle = "Stop",
    baseInDir = "/vols/cms04/RA1/74X/MC/20160504_JetPtThr_SignalModels/20160504_AtLogic_SelStudies_MC_SignalModels_25ns",
    baseOutDir = "/vols/cms02/ace09/alphat/signalModels",
    genEvtsFile = "/home/hep/ace09/alphat/cmgtools/AlphaTools/macros/TreeSplitterSusy/genEvtsPerMass_T2tt.root",
    massInfoDir = "/home/hep/ace09/alphat/cmgtools/AlphaTools/macros/TreeSplitterSusy/massInfo/"
    )


info_T2qq = info(
    sparticle = "Squark",
    baseInDir = "/vols/cms04/RA1/74X/MC/20160504_JetPtThr_SignalModels/20160504_AtLogic_SelStudies_MC_SignalModels_25ns",
    baseOutDir = "/vols/cms02/ace09/alphat/signalModels",
    genEvtsFile = "/home/hep/ace09/alphat/cmgtools/AlphaTools/macros/TreeSplitterSusy/genEvtsPerMass_T2qq.root",
    massInfoDir = "/home/hep/ace09/alphat/cmgtools/AlphaTools/macros/TreeSplitterSusy/massInfo/"
    )

info_T2bb = info(
    sparticle = "Sbottom",
    baseInDir = "/vols/cms04/RA1/74X/MC/20160504_JetPtThr_SignalModels/20160504_AtLogic_SelStudies_MC_SignalModels_25ns",
    baseOutDir = "/vols/cms02/ace09/alphat/signalModels",
    genEvtsFile = "/home/hep/ace09/alphat/cmgtools/AlphaTools/macros/TreeSplitterSusy/genEvtsPerMass_T2bb.root",
    massInfoDir = "/home/hep/ace09/alphat/cmgtools/AlphaTools/macros/TreeSplitterSusy/massInfo/"
    )

info_T1bbbb = info(
    sparticle = "Gluino",
    baseInDir = "/vols/cms04/RA1/74X/MC/20160504_JetPtThr_SignalModels/20160504_AtLogic_SelStudies_MC_SignalModels_25ns",
    baseOutDir = "/vols/cms02/ace09/alphat/signalModels",
    genEvtsFile = "/home/hep/ace09/alphat/cmgtools/AlphaTools/macros/TreeSplitterSusy/genEvtsPerMass_T1bbbb.root",
    massInfoDir = "/home/hep/ace09/alphat/cmgtools/AlphaTools/macros/TreeSplitterSusy/massInfo/"
    )


