# Copyright (C) 2018-19 Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
# email contact: christoph.rosemann@desy.de
#
# iintgui is an application for the ADAPT framework
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation in  version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.

# the central control class for interactive processing
# it holds an instance of the batch processing master

try:
    from adapt import processingControl
    from adapt import processData
    from adapt import processBuilder
    from adapt import processingConfiguration
    from adapt import adaptException

    from adapt.processes import specfilereader
    from adapt.processes import fiofilereader
    from adapt.processes import filter1d
    from adapt.processes import subsequenceselection
    from adapt.processes import curvefitting
    from adapt.processes import gendatafromfunction
    from adapt.processes import integratefitresult
    from adapt.processes import backgroundsubtraction
    from adapt.processes import trapezoidintegration
    from adapt.processes import iintdefinition
    from adapt.processes import iintfinalization
    from adapt.processes import iintpolarization
    from adapt.processes import iintcontrolplots
    from adapt.processes import iintscanprofileplot
    from adapt.processes import iintscanplot
except ImportError:
    print("[iintGUIProcessingControl]:: adapt is not available, nothing can be instantiated.")
    pass
try:
    from psio import psioException
except ImportError:
    print("[iintGUIProcessingControl]:: psio is not available, file reading is not available.")
    pass

from PyQt4 import QtGui
import numpy as np
import datetime


class IintGUIProcessingControl():
    '''The central control object for interactive processing.
       It holds the elements to build processes from their description,
       the list of processes to be run and the central data exchange object.'''

    def __init__(self):
        self._procControl = processingControl.ProcessingControl()
        self._procBuilder = processBuilder.ProcessBuilder()
        self._dataList = []
        self._mcaDict = {}
        self._processList = []
        self._nodespike = True
        self._nobkg = True
        self._nosignalprocessing = True
        self._nofinalizing = True
        self._motorName = ""
        self._rawName = "rawdata"
        self._id = "scannumber"
        self._observableName = "intensity"
        self._despObservableName = "despikedIntensity"
        self._backgroundPointsName = "bkgPoints"
        self._backgroundIntegralName = "bkgIntegral"
        self._signalName = "signalIntensity"
        self._fittedSignalName = "signalcurvefitresult"
        self._testfitName = "testfitresult"
        self._fitSignalPointsName = "signalFitPoints"
        self._singleFitPointsName = "singleFitPoints"
        self._trapintName = "trapezoidIntegral"
        self._processNames = ["specread",
                              "fioread",
                              "observabledef",
                              "despike",
                              "bkgselect",
                              "bkgfit",
                              "calcbkgpoints",
                              "bkgsubtract",
                              "bkgintegral",
                              "signalcurvefit",
                              "testfit",
                              "calcfitpoints",
                              "calcsinglefitpoints",
                              "trapint",
                              "finalize",
                              "polana",
                              "inspection",
                              "scanprofileplot",
                              "mcaplot",
                              "scanplot"]
        self._procRunList = []
        self._processParameters = {}
        self._setupProcessParameters()
        self._setupDefaultNames()
        self._outputDirectory = None
        self._trackedHeaderData = []
        self._trackedColumnData = []
        self._readerType = ""

    def resetAll(self):
        for elem in self._dataList:
            elem.clearAll()
        del self._dataList[:]
        self._dataList.clear()
        self._mcaDict.clear()
        del self._processList[:]
        self._trackedHeaderData.clear()
        self._trackedColumnData.clear()
        self._processList.clear()
        self._motorName = ""
        self._rawName = "rawdata"
        self._observableName = "intensity"
        self._despObservableName = "despikedIntensity"
        self._backgroundPointsName = "bkgPoints"
        self._backgroundIntegralName = "bkgIntegral"
        self._signalName = "signalIntensity"
        self._fittedSignalName = "signalcurvefitresult"
        self._testfitName = "testfitresult"
        self._fitSignalPointsName = "signalFitPoints"
        self._singleFitPointsName = "singleFitPoints"
        self._trapintName = "trapezoidIntegral"
        self._setupProcessParameters()
        self._setupDefaultNames()
        self.resetTrackedData()
        self._readerType = ""
        self._nodespike = True

    def resetRAWdata(self):
        for elem in self._dataList:
            try:
                elem.clearCurrent(self._rawName)
            except KeyError:
                pass

    def resetOBSdata(self):
        for elem in self._dataList:
            try:
                elem.clearCurrent(self._observableName)
                elem.clearCurrent(self._despObservableName)
            except KeyError:
                pass

    def resetBKGdata(self):
        for elem in self._dataList:
            try:
                elem.clearCurrent(self._backgroundPointsName)
            except KeyError:
                pass

    def resetTRAPINTdata(self):
        self.useSignalProcessing(False)
        for elem in self._dataList:
            try:
                elem.clearCurrent(self._trapintName)
                # ugly fix: there is also the error to be concerned
                elem.clearCurrent(self._trapintName+"_stderr")
            except KeyError:
                pass

    def resetSIGdata(self):
        self.useSignalProcessing(False)
        for elem in self._dataList:
            try:
                elem.clearCurrent(self._signalName)
            except KeyError:
                pass

    def resetFITdata(self):
        self.useSignalProcessing(False)
        for elem in self._dataList:
            try:
                elem.clearCurrent(self._fittedSignalName)
                elem.clearCurrent(self._fitSignalPointsName)
            except KeyError:
                pass

    def _setupProcessParameters(self):
        self._processParameters["specread"] = specfilereader.specfilereader().getProcessDictionary()
        self._processParameters["fioread"] = fiofilereader.fiofilereader().getProcessDictionary()
        self._processParameters["observabledef"] = iintdefinition.iintdefinition().getProcessDictionary()
        self._processParameters["despike"] = filter1d.filter1d().getProcessDictionary()
        self._processParameters["bkgselect"] = subsequenceselection.subsequenceselection().getProcessDictionary()
        self._processParameters["bkgfit"] = curvefitting.curvefitting().getProcessDictionary()
        self._processParameters["bkgintegral"] = integratefitresult.integratefitresult().getProcessDictionary()
        self._processParameters["calcbkgpoints"] = gendatafromfunction.gendatafromfunction().getProcessDictionary()
        self._processParameters["bkgsubtract"] = backgroundsubtraction.backgroundsubtraction().getProcessDictionary()
        self._processParameters["signalcurvefit"] = curvefitting.curvefitting().getProcessDictionary()
        self._processParameters["testfit"] = curvefitting.curvefitting().getProcessDictionary()
        self._processParameters["calcfitpoints"] = gendatafromfunction.gendatafromfunction().getProcessDictionary()
        self._processParameters["calcsinglefitpoints"] = gendatafromfunction.gendatafromfunction().getProcessDictionary()
        self._processParameters["trapint"] = trapezoidintegration.trapezoidintegration().getProcessDictionary()
        self._processParameters["finalize"] = iintfinalization.iintfinalization().getProcessDictionary()
        self._processParameters["polana"] = iintpolarization.iintpolarization().getProcessDictionary()
        self._processParameters["inspection"] = iintcontrolplots.iintcontrolplots().getProcessDictionary()
        self._processParameters["scanprofileplot"] = iintscanprofileplot.iintscanprofileplot().getProcessDictionary()
        self._processParameters["scanplot"] = iintscanplot.iintscanplot().getProcessDictionary()

        self._fitmodels = curvefitting.curvefitting().getFitModels()

    def _setupDefaultNames(self):
        self._processParameters["specread"]["output"] = self._rawName
        self._processParameters["fioread"]["output"] = self._rawName
        # from out to in:
        self._processParameters["observabledef"]["input"] = self._rawName
        self._processParameters["observabledef"]["output"] = self._observableName
        self._processParameters["observabledef"]["detector_column"] = "exp_c01"
        self._processParameters["observabledef"]["monitor_column"] = "sumvfcs_counts"
        self._processParameters["observabledef"]["exposureTime_column"] = "exp_t01"
        self._processParameters["observabledef"]["id"] = self._id

        self._processParameters["scanprofileplot"]["outfilename"] = None
        self._processParameters["scanprofileplot"]["xaxis"] = None
        self._processParameters["scanprofileplot"]["yaxis"] = self._id
        self._processParameters["scanprofileplot"]["zaxis"] = self._observableName
        self._processParameters["scanprofileplot"]["rawdataname"] = self.getRawDataName()

        self._processParameters["despike"]["input"] = self._observableName
        self._processParameters["despike"]["method"] = "p09despiking"
        self._processParameters["despike"]["output"] = self._despObservableName
        # from out to in
        self._processParameters["bkgselect"]["input"] = [self._despObservableName, self._motorName]
        self._processParameters["bkgselect"]["output"] = ["bkgY", "bkgX"]
        self._processParameters["bkgselect"]["selectors"] = ["selectfromstart", "selectfromend"]
        self._processParameters["bkgselect"]["startpointnumber"] = 3
        self._processParameters["bkgselect"]["endpointnumber"] = 3
        # fit bkg
        self._processParameters["bkgfit"]["xdata"] = "bkgX"
        self._processParameters["bkgfit"]["ydata"] = "bkgY"
        self._processParameters["bkgfit"]["error"] = "None"
        self._processParameters["bkgfit"]["result"] = "bkgfitresult"
        self._processParameters["bkgfit"]["usepreviousresult"] = 0
        self._processParameters["bkgfit"]["model"] = {"lin_": {"modeltype": "linearModel"}}
        # bkg integral, standard case
        self._processParameters["bkgintegral"]["fitresult"] = "bkgfitresult"
        self._processParameters["bkgintegral"]["xdata"] = self._motorName
        self._processParameters["bkgintegral"]["output"] = self._backgroundIntegralName
        # calc bkg points
        self._processParameters["calcbkgpoints"]["fitresult"] = "bkgfitresult"
        self._processParameters["calcbkgpoints"]["xdata"] = self._motorName
        self._processParameters["calcbkgpoints"]["output"] = self._backgroundPointsName
        # subtract bkg
        self._processParameters["bkgsubtract"]["input"] = self._despObservableName
        self._processParameters["bkgsubtract"]["output"] = self._signalName
        self._processParameters["bkgsubtract"]["background"] = self._backgroundPointsName
        # signal fitting
        self._processParameters["signalcurvefit"]["xdata"] = self._motorName
        self._processParameters["signalcurvefit"]["ydata"] = self._signalName
        self._processParameters["signalcurvefit"]["error"] = "None"
        self._processParameters["signalcurvefit"]["usepreviousresult"] = 0
        self._processParameters["signalcurvefit"]["useguessing"] = 0
        self._processParameters["signalcurvefit"]["result"] = self._fittedSignalName
        self._processParameters["signalcurvefit"]["model"] = {"m0_": {"modeltype": "gaussianModel"}}
        # test fit
        self._processParameters["testfit"]["xdata"] = self._motorName
        self._processParameters["testfit"]["ydata"] = self._signalName
        self._processParameters["testfit"]["error"] = "None"
        self._processParameters["testfit"]["usepreviousresult"] = 0
        self._processParameters["testfit"]["useguessing"] = 0
        self._processParameters["testfit"]["result"] = self._testfitName
        self._processParameters["testfit"]["model"] = {"m0_": {"modeltype": "gaussianModel"}}
        # calc fitted signal points
        self._processParameters["calcfitpoints"]["fitresult"] = self._fittedSignalName
        self._processParameters["calcfitpoints"]["xdata"] = self._motorName
        self._processParameters["calcfitpoints"]["output"] = self._fitSignalPointsName
        # calc single fit points
        self._processParameters["calcsinglefitpoints"]["fitresult"] = self._testfitName
        self._processParameters["calcsinglefitpoints"]["xdata"] = self._motorName
        self._processParameters["calcsinglefitpoints"]["output"] = self._singleFitPointsName
        # trapezoidal integration
        self._processParameters["trapint"]["motor"] = self._motorName
        self._processParameters["trapint"]["observable"] = self._signalName
        self._processParameters["trapint"]["output"] = self._trapintName
        # finalization: saving files
        self._processParameters["finalize"]["specdataname"] = self._rawName
        self._processParameters["finalize"]["fitresult"] = self._fittedSignalName
        self._processParameters["finalize"]["trackedHeaders"] = []
        self._processParameters["finalize"]["trackedColumns"] = []
        # polarization analysis
        self._processParameters["polana"]["specdataname"] = self._rawName
        self._processParameters["polana"]["fitresult"] = self._fittedSignalName
        self._processParameters["polana"]["trapintname"] = self._trapintName
        # inspection plots
        self._processParameters["inspection"]["specdataname"] = self._rawName
        self._processParameters["inspection"]["fitresult"] = self._fittedSignalName
        self._processParameters["inspection"]["trapintname"] = self._trapintName
        self._processParameters["inspection"]["trackedColumns"] = []
        # finalization: saving files
        self._processParameters["scanplot"]["specdataname"] = self._rawName
        self._processParameters["scanplot"]["fitresult"] = self._fittedSignalName
        self._processParameters["scanplot"]["trapintname"] = self._trapintName

    def _cleanUpTrackedData(self):
        self._trackedHeaderData.clear()
        self._trackedColumnData.clear()

    def getRawDataName(self):
        return self._rawName

    def getMotorName(self):
        return self._motorName

    def setMotorName(self, name=None):
        self._motorName = name
        self._processParameters["observabledef"]["motor_column"] = self._motorName
        self._processParameters["scanprofileplot"]["xaxis"] = self._motorName
        self._processParameters["bkgselect"]["input"] = [self._despObservableName, self._motorName]
        self._processParameters["bkgintegral"]["xdata"] = self._motorName
        self._processParameters["calcbkgpoints"]["xdata"] = self._motorName
        self._processParameters["signalcurvefit"]["xdata"] = self._motorName
        self._processParameters["testfit"]["xdata"] = self._motorName
        self._processParameters["calcfitpoints"]["xdata"] = self._motorName
        self._processParameters["calcsinglefitpoints"]["xdata"] = self._motorName
        self._processParameters["trapint"]["motor"] = self._motorName
        self._processParameters["inspection"]["motor"] = self._motorName
        self._processParameters["finalize"]["motor"] = self._motorName
        self._processParameters["scanplot"]["motor"] = self._motorName

    def settingChoiceDesBkg(self):
        # four cases des-bkg: no-no yes-no no-yes and yes-yes
        if self._nodespike and self._nobkg:
            self._processParameters["trapint"]["observable"] = self._observableName
            self._processParameters["signalcurvefit"]["ydata"] = self._observableName
            self._processParameters["testfit"]["ydata"] = self._observableName
            self._processParameters["inspection"]["observable"] = self._observableName
            self._processParameters["finalize"]["observable"] = self._observableName
            self._processParameters["scanplot"]["observable"] = self._observableName
        if not self._nodespike and self._nobkg:
            self._processParameters["trapint"]["observable"] = self._despObservableName
            self._processParameters["signalcurvefit"]["ydata"] = self._despObservableName
            self._processParameters["testfit"]["ydata"] = self._despObservableName
            self._processParameters["inspection"]["observable"] = self._despObservableName
            self._processParameters["finalize"]["observable"] = self._despObservableName
            self._processParameters["scanplot"]["observable"] = self._despObservableName
        if self._nodespike and not self._nobkg:
            self._processParameters["bkgselect"]["input"] = [self._observableName, self._motorName]
            self._processParameters["bkgsubtract"]["input"] = self._observableName
            self._processParameters["trapint"]["observable"] = self._signalName
            self._processParameters["signalcurvefit"]["ydata"] = self._signalName
            self._processParameters["testfit"]["ydata"] = self._signalName
            self._processParameters["inspection"]["observable"] = self._signalName
            self._processParameters["finalize"]["observable"] = self._signalName
            self._processParameters["scanplot"]["observable"] = self._signalName
        if not self._nodespike and not self._nobkg:
            self._processParameters["bkgselect"]["input"] = [self._despObservableName, self._motorName]
            self._processParameters["bkgsubtract"]["input"] = self._despObservableName
            self._processParameters["trapint"]["observable"] = self._signalName
            self._processParameters["signalcurvefit"]["ydata"] = self._signalName
            self._processParameters["testfit"]["ydata"] = self._signalName
            self._processParameters["inspection"]["observable"] = self._signalName
            self._processParameters["finalize"]["observable"] = self._signalName
            self._processParameters["scanplot"]["observable"] = self._signalName

    def getObservableName(self):
        return self._observableName

    def getDespikedObservableName(self):
        return self._despObservableName

    def getBackgroundName(self):
        return self._backgroundPointsName

    def getSignalName(self):
        return self._signalName

    def getSingleFitName(self):
        return self._testfitName

    def getFittedSignalName(self):
        return self._fitSignalPointsName

    def getSingleFitPointsName(self):
        return self._singleFitPointsName

    def getTrapezoidIntegralName(self):
        return self._trapintName

    def getProcessTypeList(self):
        return self._procControl.getProcessTypeList()

    def createDataList(self, data, name):
        for datum in data:
            pd = processData.ProcessData()
            pd.addData(name, datum)
            # this is not safe for multiple data elements with MCA data
            # !!! FIXME !!!
            if datum.getMCAName() != '':
                pd.addData("MCAName", datum.getMCAName())
                pd.addData("MCA", datum.getMCA())
                self._mcaDict[datum.getScanNumber()] = datum.getMCA()
            self._dataList.append(pd)
        try:
            self.setMotorName(self._dataList[0].getData(self.getRawDataName()).getMotorName())
        except IndexError:
            pass
        except psioException.PSIOUnknownScanTypeException:
            self.setMotorName(None)
        # and now create the scan list!
        self._createScanList()

    def getMCA(self):
        return self._mcaDict

    def checkDataIntegrity(self):
        error = False
        motor = self._dataList[0].getData(self.getRawDataName()).getMotorName()
        for datum in self._dataList:
            if motor != datum.getData(self.getRawDataName()).getMotorName():
                error = True
                break
        return error

    def checkScanRanges(self):
        tmpdict = {}
        self._rangeDict = {}
        for datum in self._dataList:
            scandata = datum.getData(self.getRawDataName())
            ranges = scandata.getRanges()
            for rangeitem in ranges.items():
                try:
                    tmpdict[rangeitem[0]].append(rangeitem[1])
                except KeyError:
                    tmpdict[rangeitem[0]] = [rangeitem[1]]
        for scanitem in tmpdict.items():
            testlist = list(set(scanitem[1]))
            if( len(testlist) > 1 ):
                ranger = np.asarray(scanitem[1])
                newrange = ranger.min()
                self._rangeDict[scanitem[0]] = float(newrange)
            else:
                pass
        return self._rangeDict

    def getRawDataObject(self):
        return self.getDataList()[0].getData(self.getRawDataName())

    def getDataList(self):
        return self._dataList

    def createAndInitialize(self, pdict):
        proc = self._procBuilder.createProcessFromDictionary(pdict)
        proc.initialize()
        return proc

    def createAndBulkExecute(self, pDict):
        if pDict is None:
            return
        proc = self._procBuilder.createProcessFromDictionary(pDict)
        proc.initialize()
        try:
            proc.loopExecuteWithOverwrite(self._dataList, emitProgress=True)
        except adaptException.AdaptProcessingStoppedException:
            return "stopped"
        return proc

    def createAndSingleExecute(self, pDict, index):
        if pDict is None:
            return
        proc = self._procBuilder.createProcessFromDictionary(pDict)
        proc.initialize()
        try:
            proc.executeWithOverwrite(self._dataList[index])
        except adaptException.AdaptProcessingStoppedException:
            return "stopped"
        return proc

    def processAll(self, pDict):
        if pDict is None:
            return
        proc = self._procBuilder.createProcessFromDictionary(pDict)
        proc.initialize()
        proc.loopExecute(self._dataList, emitProgress=True)
        proc.finalize(data=None)

    def performBKGIntegration(self):
        # bkg integral, ranged case:
        try:
            if len(self._rangeDict) > 0:
                self._processParameters["bkgintegral"]["selectrange"] = self._rangeDict[self._motorName]
        except AttributeError:
            pass
        self.createAndBulkExecute(self._processParameters["bkgintegral"])

    def removeBKGparts(self):
        for datum in self._dataList:
            datum.clearCurrent(self._signalName)
            datum.clearCurrent(self._backgroundIntegralName)
            datum.clearCurrent(self._fittedSignalName)
            datum.clearCurrent(self._fitSignalPointsName)
            datum.clearCurrent(self._singleFitPointsName)
        # if there was some bkg information present/processed
        # now it's the time to remove all traces:
        try:
            while(1):
                self._processParameters["finalize"]["trackedHeaders"].remove(self._backgroundIntegralName)
        except ValueError:
            # all values removed
            pass

    def processScanProfiles(self, name):
        self._processParameters["scanprofileplot"]["outfilename"] = name
        self.processAll(self._processParameters["scanprofileplot"])

    def processMCAPlots(self, name):
        self._processParameters["mcaplot"]["outfilename"] = name
        self.processAll(self._processParameters["mcaplot"])

    def processScanControlPlots(self, name):
        self._processParameters["scanplot"]["outfilename"] = name
        self.processAll(self._processParameters["scanplot"])

    def processTrackedColumnsControlPlots(self, name):
        self._processParameters["inspection"]["outfilename"] = name
        self.processAll(self._processParameters["inspection"])

    def setReaderType(self, rtype=""):
        self._readerType = rtype

    def loadConfig(self, processConfig):
        self._procRunList.clear()
        execOrder = processConfig.getOrderOfExecution()
        if "fioread" in execOrder:
            self._readerType = "fio"
        elif "specread" in execOrder:
            self._readerType = "spec"
        pDefs = processConfig.getProcessDefinitions()
        for proc in execOrder:
            if proc in self._processNames:
                self._procRunList.append(proc)
                for k, v in pDefs[proc].items():
                    self._processParameters[proc][k] = v
            else:
                print("Wrong configuration file, unrecognized process name/type: " + str(proc))
        if "despike" in execOrder:
            self._nodespike = False
        if "bkgsubtract" in execOrder:
            self._nobkg = False
        # set motor name proper from the config !
        if self._processParameters["observabledef"]["motor_column"] is not None:
            self.setMotorName(self._processParameters["observabledef"]["motor_column"])
        # set tracked stuff, if present in config
        hl, cl = self._processParameters["observabledef"]["trackedHeaders"], self._processParameters["observabledef"]["trackedColumns"]
        if hl is None:
            hl = []
        if cl is None:
            cl = []
        self.setTrackedData(headerlist=hl, columnlist=cl)
        # cleaning up, improper handling of save value -- how to really fix?
        if self._processParameters["observabledef"]["attenuationFactor_column"] is None:
            del self._processParameters["observabledef"]["attenuationFactor_column"]
        return execOrder

    def saveConfig(self, filename):
        if self._readerType == "spec":
            execlist = ["specread", "observabledef"]
        elif self._readerType == "fio":
            execlist = ["fioread", "observabledef"]
        else:
            return
        processDict = {}
        processDict["specread"] = self.getSFRDict()
        processDict["fioread"] = self.getFFRDict()
        processDict["observabledef"] = self.getOBSDict()
        try:
            if processDict["observabledef"]["attenuationFactor_column"] is None:
                del processDict["observabledef"]["attenuationFactor_column"]
        except KeyError:
            # key is not present -- don't worry
            pass
        if self._trackedHeaderData is not []:
            processDict["observabledef"]["trackedHeaders"] = self._trackedHeaderData
        if self._trackedColumnData is not []:
            processDict["observabledef"]["trackedColumns"] = self._trackedColumnData
        if not self._nodespike:
            execlist.append("despike")
            processDict["despike"] = self.getDESDict()
        if not self._nobkg:
            execlist.append("bkgselect")
            execlist.append("bkgfit")
            execlist.append("calcbkgpoints")
            execlist.append("bkgsubtract")
            ds = self.getBKGDicts()
            processDict["bkgselect"] = ds[0]
            processDict["bkgfit"] = ds[1]
            processDict["calcbkgpoints"] = ds[2]
            processDict["bkgsubtract"] = ds[3]
            execlist.append("bkgintegral")
            processDict["bkgintegral"] = self.getBKGIntegralDict()
        if not self._nosignalprocessing:
            execlist.append("trapint")
            processDict["trapint"] = self.getTrapIntDict()
            execlist.append("signalcurvefit")
            processDict["signalcurvefit"] = self.getSIGDict()
        if not self._nofinalizing:
            execlist.append("finalize")
            processDict["finalize"] = self.getFinalizingDict()
        procconfig = processingConfiguration.ProcessingConfiguration()
        procconfig.addProcessDefinition(processDict)
        procconfig.setOrderOfExecution(execlist)
        from adapt import configurationHandler
        handler = configurationHandler.ConfigurationHandler()
        handler.writeConfig(filename, procconfig)

    def setOutputDirectory(self, name):
        self._outputDirectory = name

    def getOutputDirectory(self):
        if self._outputDirectory is None:
            import os.path
            self._outputDirectory = os.path.expanduser('~')
        return self._outputDirectory

    def setDefaultOutputDirectory(self, filename):
        import os.path
        defpath = os.path.dirname(filename)
        self.setOutputDirectory(defpath)

    def proposeSaveFileName(self, suffix=''):
        import os.path
        filenamestart = os.path.join(self._outputDirectory, self._outfileName)
        # needs distinction between fio and spec !
        # decompose the scanlist parameters
        if self._readerType == "spec":
            scanlist = str(self._processParameters["specread"]["scanlist"])
            stride = None
            retlist = []
            if scanlist.find(':') != -1:
                stride = int(scanlist.split(':')[-1])
                scanlist = scanlist.split(':')[0]
            scanlist = scanlist.split('[')[-1]
            scanlist = scanlist.split(']')[0]
            try:
                li = scanlist.split(',')
            except AttributeError:
                pass
            for elem in li:
                try:
                    retlist.append(int(elem))
                except ValueError:
                    try:
                        tmp = elem.split('-')
                        for i in tmp:
                            retlist.append(i)
                    except:
                        pass
            retlist.sort()
            startnumber = retlist[0]
            endnumber = retlist[-1]
            if stride is not None:
                stridesuffix = "-s" + str(stride)
            else:
                stridesuffix = ''
            return filenamestart + "_S" + str(startnumber) + "E" + str(endnumber) + stridesuffix + suffix, datetime.datetime.now().strftime("_%Y%m%d-%Hh%M")
        elif self._readerType == "fio":
            return filenamestart, datetime.datetime.now().strftime("_%Y%m%d-%Hh%M")

    def _setOutfileName(self, name):
        import os.path
        if name == "spec":
            try:
                self._outfileName = os.path.basename(self._processParameters["specread"]["filename"]).split('.')[0]
            except:
                return
        elif name == "fio":
            # get the complete file name without the directory
            bname = os.path.basename(self._processParameters["fioread"]["filenames"][0])
            bname2 = os.path.basename(self._processParameters["fioread"]["filenames"][-1])
            # chop off the suffix .fio
            rawname = os.path.splitext(bname)[0]
            rawname2 = os.path.splitext(bname2)[0]
            # determine the last part/number
            snippet = rawname.split("_")[-1]
            snippet2 = rawname2.split("_")[-1]
            start = int(snippet)
            end = int(snippet2)
            # and set the final name, remove the last underscore
            self._outfileName = rawname.strip(snippet)[:-1] + "_S" + str(start) + "E" + str(end)

    def getSFRDict(self):
        return self._processParameters["specread"]

    def getFFRDict(self):
        return self._processParameters["fioread"]

    def getOBSDict(self):
        return self._processParameters["observabledef"]

    def setOBSDict(self, obsdic):
        self._processParameters["observabledef"] = iintdefinition.iintdefinition().getProcessDictionary()
        for k, v in obsdic.items():
            self._processParameters["observabledef"][k] = v

    def getDESDict(self):
        if self._nodespike:
            return {}
        try:
            return self._processParameters["despike"]
        except KeyError:
            return {}

    def setDESDict(self, desdic):
        for k, v in desdic.items():
            self._processParameters["despike"][k] = v

    def getTrapIntDict(self):
        try:
            return self._processParameters["trapint"]
        except KeyError:
            return {}

    def setZValueInProfilePlot(self, zval):
        self._processParameters["scanprofileplot"]["zaxis"] = zval

    def setSpecFile(self, name, scanlist):
        self._processParameters["specread"]["filename"] = name
        self._processParameters["specread"]["scanlist"] = scanlist
        self._setOutfileName("spec")

    def setFioFile(self, names):
        self._processParameters["fioread"]["filenames"] = names
        self._setOutfileName("fio")

    def getScanlist(self):
        return self._scanlist

    def _createScanList(self):
        self._scanlist = []
        for datum in self._dataList:
            sn = datum.getData(self.getRawDataName()).getScanNumber()
            self._scanlist.append(sn)

    def _expandList(self, somelist):
        scanlist = str(somelist)
        retlist = []
        stride = None
        self._scanlist = []
        if scanlist.find(':') != -1:
            stride = int(scanlist.split(':')[-1])
            scanlist = scanlist.split(':')[0]
        scanlist = scanlist.split('[')[-1]
        scanlist = scanlist.split(']')[0]
        try:
            li = scanlist.split(',')
        except AttributeError:
            pass
        for elem in li:
            try:
                retlist.append(int(elem))
            except ValueError:
                try:
                    tmp = elem.split('-')
                    if stride:
                        for n in range(tmp[0], (tmp[1]+1), stride):
                            retlist.append(n)
                    else:
                        for n in range(int(tmp[0]), int(tmp[1])+1):
                            retlist.append(n)
                except:
                    pass
        retlist.sort()
        return retlist

    def setBkgModel(self, modelname):
        if modelname == "linearModel":
            self._processParameters["bkgfit"]["model"] = {"linbkg_": {"modeltype": modelname}}
        elif modelname == "constantModel":
            self._processParameters["bkgfit"]["model"] = {"constbkg_": {"modeltype": modelname}}
        elif modelname == "shiftedhyperbolaModel":
            self._processParameters["bkgfit"]["model"] = {"hyperbolicbkg_": {"modeltype": modelname}}
        else:
            print("Unknown model for background. Check.")

    def getBKGDicts(self):
        try:
            return (self._processParameters["bkgselect"],
                    self._processParameters["bkgfit"],
                    self._processParameters["calcbkgpoints"],
                    self._processParameters["bkgsubtract"])
        except KeyError:
            return ({}, {}, {}, {})

    def getBKGIntegralDict(self):
        try:
            if len(self._rangeDict) > 0:
                self._processParameters["bkgintegral"]["selectrange"] = self._rangeDict[self._motorName]
            return self._processParameters["bkgintegral"]
        except KeyError:
            return {}

    def getSIGDict(self):
        try:
            return self._processParameters["signalcurvefit"]
        except KeyError:
            return {}

    def getTestFitDict(self):
        try:
            return self._processParameters["testfit"]
        except KeyError:
            return {}

    def getPOLANADict(self):
        try:
            name, suff = self.proposeSaveFileName()
            self._processParameters["polana"]["outputname"] = str(name+suff)
            return self._processParameters["polana"]
        except KeyError:
            return {}

    def getInspectionDict(self):
        try:
            name, suff = self.proposeSaveFileName()
            self._processParameters["inspection"]["outputname"] = str(name+suff)
            return self._processParameters["inspection"]
        except KeyError:
            return {}

    def getSignalFitModel(self):
        return self._processParameters["signalcurvefit"]["model"]["m0_"]["modeltype"]

    def getFitModels(self):
        return curvefitting.curvefitting().getFitModels()

    def createFitFunctions(self, names):
        return [self._fitmodels[name]() for name in names]

    # i can't help it, this breaks about every design rule; but i can't think of a better way currently
    def getSumExchangeObject(self, tmpobjects, colour):
        self._ffexo = None
        for tmp in tmpobjects:
            try:
                self._ffexo.addData(tmp.data())
            except:
                self._ffexo = fakeFitExchangeObject(data=tmp.data(), colour=colour)
        return self._ffexo

    def getSignalFitDict(self):
        return self._processParameters["calcfitpoints"]

    def getSingleFitDict(self):
        return self._processParameters["calcsinglefitpoints"]

    def getFinalizingDict(self):
        # build the finalizing dict manually 
        # add the scannumber and trapint data to the tracked header data
        self._processParameters["finalize"]["trackedHeaders"] = ['scannumber']
        self._processParameters["finalize"]["trackedHeaders"] += self._trackedHeaderData
        self._processParameters["finalize"]["trackedHeaders"] +=  [self._trapintName, self._trapintName+"_stderr"]
        if not self._nobkg:
            self._processParameters["finalize"]["trackedHeaders"].append(self._backgroundIntegralName)
        self._processParameters["finalize"]["trackedColumns"] = self._trackedColumnData
        return self._processParameters["finalize"]

    def setTrackedData(self, headerlist=[], columnlist=[]):
        if headerlist is []:
            if columnlist is []:
                return
        self._cleanUpTrackedData()
        # hard lesson learned: shared lists are the same!
        self._trackedHeaderData = headerlist.copy()
        self._trackedColumnData = columnlist.copy()
        self._processParameters["inspection"]["trackedColumns"] = columnlist.copy()

    def getTrackedHeaderData(self):
        return self._trackedHeaderData

    def getTrackedColumnData(self):
        return self._trackedColumnData

    def resetTrackedData(self):
        self._trackedHeaderData.clear()
        self._trackedColumnData.clear()

    def useBKG(self, value):
        self._nobkg = not value
        self.settingChoiceDesBkg()

    def useDespike(self, value):
        self._nodespike = not value
        self.settingChoiceDesBkg()

    def useSignalProcessing(self, value):
        self._nosignalprocessing = not value

    def useFinalizing(self, value):
        self._nofinalizing = not value

    def getTrackInformation(self, name, header=False):
        '''Collect the tracked data given by name.
           Returns the name, value and error of the tracked parameter,
           plus a dictionary of the fitted parameters including their error.'''

        value, error = [], []
        infoholder = {}
        # fill the array element by element from the datalist
        for datum in self._dataList:
            fitresult = datum.getData(self._fittedSignalName)
            params = fitresult.params
            for param in params:
                # exclude the duplicate part for gauss/lorentz
                if "fwhm" in param:
                    continue
                elif "height" in param:
                    continue
                try:
                    infoholder[params[param].name].append((params[param].value, params[param].stderr))
                except KeyError:
                    infoholder[params[param].name] = []
                    infoholder[params[param].name].append((params[param].value, params[param].stderr))
            if not header:
                try:
                    array = datum.getData(self._rawName).getArray(name)
                    value.append(np.mean(array))
                    error.append(np.std(array))
                except:
                    print("Can't retrieve the information of " + str(name))
                    return  
            if header:
                try:
                    value.append(datum.getData(self._rawName).getCustomVar(name))
                    error.append(0.)
                except:
                    print("Can't retrieve the information of " + str(name))
                    return
        return trackedInformation(name, value, error, infoholder)

    def getRawTrackInformation(self, name):
        '''Collect the tracked data given by name.
           Returns the name and value of the tracked parameter.'''
        value = []
        for datum in self._dataList:
            try:
                array = datum.getData(self._rawName).getArray(name)
                value.append(np.mean(array))
            except KeyError:
                try:
                    value.append(datum.getData(self._rawName).getCustomVar(name))
                except:
                    print("Can't retrieve the information of " + str(name))
                    return
        return value

    def getSignalFitResults(self):
        resultlist = []
        try:
            for datum in self._dataList:
                scannumber = datum.getData(self.getRawDataName()).getScanNumber()
                resultlist.append(80 * "*" + '\n' + "Scan number : " + str(scannumber) + '\n')
                resultlist.append(datum.getData(self._fittedSignalName).fit_report())
        except:
            pass
        return resultlist

    def getDefaultTrackInformation(self):
        value, error = [], []
        infoholder = {}
        name = 'ScanNumber'
        for datum in self._dataList:
            fitresult = datum.getData(self._fittedSignalName)
            params = fitresult.params
            for param in params:
                # exclude the duplicate part for gauss/lorentz
                if "fwhm" in param:
                    continue
                elif "height" in param:
                    continue
                try:
                    infoholder[params[param].name].append((params[param].value, params[param].stderr))
                except KeyError:
                    infoholder[params[param].name] = []
                    infoholder[params[param].name].append((params[param].value, params[param].stderr))

            value.append(datum.getData(self._rawName).getScanNumber())
            error.append(0.)

        return trackedInformation(name, value, error, infoholder)

    def setResultFilename(self, filename):
        self._processParameters["finalize"]["outfilename"] = filename + ".iint"
        self._resultBaseFilename = filename

    def getResultBaseFilename(self):
        try:
            return self._resultBaseFilename
        except:
            return None

    def useGuessSignalFit(self, guess):
        if guess:
            self._processParameters["signalcurvefit"]["usepreviousresult"] = 0
            self._processParameters["signalcurvefit"]["useguessing"] = 1
        else:
            self._processParameters["signalcurvefit"]["usepreviousresult"] = 1
            self._processParameters["signalcurvefit"]["useguessing"] = 0

    def guessSignalFit(self):
        return self._processParameters["signalcurvefit"]["useguessing"]


class trackedInformation():
    '''Exchange data object for plotting tracked data vs. fitted parameters.'''

    def __init__(self, name, value, error, info):
        self.name = name
        self.value = value
        self.error = error
        self.names = sorted(info.keys())
        self.values = info

    def getName(self):
        return self.name

    def getTrackedValues(self):
        return self.value

    def getValues(self, name):
        tmpval = []
        for val in self.values[name]:
            tmpval.append(val[0])
        return np.array(tmpval)

    def getErrors(self, name):
        tmpval = []
        for val in self.values[name]:
            tmpval.append(val[1])
        return np.array(tmpval)

    def getFitParameterValue(self, name):
        return self.values[name]


class fakeFitExchangeObject():
    # until I come up with a better idea, this is the way to create the
    # "sum" display part from an object

    def __init__(self, data=None, colour=QtGui.QColor('black')):
        self._data = np.copy(data)
        self._colour = colour

    def data(self):
        return self._data

    def colour(self):
        return self._colour

    def addData(self, data):
        self._data += data

    def setData(self, data):
        self._data = data

    def setColour(self, colour):
        self._colour = colour

    def dump(self):
        print("[FakeFitExchangeObject] colour " + str(self._colour) + "\ndata:  " + str(self._data))
