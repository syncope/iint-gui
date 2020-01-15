# Copyright (C) 2017-19  Christoph Rosemann
#  DESY, Notkestr. 85, D-22607 Hamburg
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


from PyQt4 import QtCore, QtGui, uic
import pyqtgraph as pg

from . import iintGUIProcessingControl
try:
    from adapt.processes import specfilereader
    from adapt.processes import fiofilereader
    from adapt import adaptException
except ImportError:
    print("[iintGUI]:: adapt is not available; please install or nothing will work.")
    pass
from . import getUIFile
from . import iintDataPlot
from . import iintOverlayPlot
from . import iintOverlaySelection
from . import fileInfo
from . import outputDir
from . import iintObservableDefinition
from . import iintBackgroundHandling
from . import iintSignalFitting
from . import iintFitConfiguration
from . import iintTrackedDataChoice
from . import trackedDataMap
from . import iintTrackedDataMapDisplay
from . import iintZValueSelection
from . import quitDialog
from . import loggerBox
from . import resetDialog
from . import showFileContents
from . import showAboutIintGUI
from . import showIintGUIHelp
from . import iintMultiTrackedDataView
from . import iintInspectAnalyze
from . import selectResultOutput
from . import collapsibleBox

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class iintGUI(QtGui.QMainWindow):

    def __init__(self, parent=None, configFile=None, testMode=False):
        super(iintGUI, self).__init__(parent)
        uic.loadUi(getUIFile.getUIFile("iintMain.ui"), self)

        self._testMode = testMode

        self.actionNew.triggered.connect(self._askReset)
        self.action_Open_SPEC_file.triggered.connect(self.showSFRGUI)
        self.actionOpen_FIO_files.triggered.connect(self.showFFRGUI)
        self.actionOpen_file.triggered.connect(self.chooseAndLoadConfig)
        self.actionSave_file.triggered.connect(self._saveConfig)
        self.actionExit.triggered.connect(self._closeApp)
        self.action_Config_File.triggered.connect(self._showConfig)
        self.actionFIO_File_s.triggered.connect(self._showFIOFiles)
        self.action_Spec_File.triggered.connect(self._showSpecFile)
        self.action_Fit_Results.triggered.connect(self._showFitResults)
        self.action_Results_File.triggered.connect(self._showResultsFile)
        self.action_Help.triggered.connect(self._showHelp)
        self.action_About.triggered.connect(self._showIintGuiInfo)

        # the steering helper object
        self._control = iintGUIProcessingControl.IintGUIProcessingControl()

        # the quit dialog
        self._quit = quitDialog.QuitDialog()
        self._quit.quitandsave.clicked.connect(self._saveConfig)
        self._quit.quitandsave.clicked.connect(exit)
        self._quit.justquit.clicked.connect(exit)

        # the core independent variable in iint:
        self._motorname = ""
        self._rawdataobject = None
        self.imageTabs = QtGui.QTabWidget()
        self.imageTabs.setTabsClosable(True)
        self.imageTabs.removeTab(1)
        self.imageTabs.removeTab(0)
        self.imageTabs.hide()
        self.imageTabs.tabCloseRequested.connect(self._checkTabClosing)
        self._dataTabIndex = None
        self._simpleImageView = iintDataPlot.iintDataPlot(parent=self)
        self._simpleImageView.blacklist.connect(self._retrackDataDisplay)
        self._simpleImageView.hidden.connect(self._unresize)
        self._overlayView = iintOverlayPlot.iintOverlayPlot(parent=self)
        self._blacklist = []

        self._resetQuestion = resetDialog.ResetDialog()
        self._resetQuestion.resetOK.connect(self._resetAll)
        self._fileInfo = fileInfo.FileInfo()
        self._outDir = outputDir.OutputDir("Unset")
        self._outDir.warning.connect(self.warning)
        self._outDir.warning.connect(print)
        self._sfrGUI = specfilereader.specfilereaderGUI()
        self._ffrGUI = fiofilereader.fiofilereaderGUI()
        self._obsDef = iintObservableDefinition.iintObservableDefinition()
        templayout = QtGui.QVBoxLayout()
        templayout.addWidget(self._obsDef)
        self._obsDefBox = collapsibleBox.CollapsibleBox("Signal definition")
        self._obsDefBox.setContentLayout(templayout)

        self._obsDef.doDespike.connect(self._control.useDespike)
        self._obsDef.showScanProfile.clicked.connect(self._openzvalchoice)
        self._obsDef.motorName.connect(self.setMotorName)

        self._obsDef.trackData.clicked.connect(self._dataToTrack)
        self._obsDef.overlayBtn.clicked.connect(self.doOverlay)

        self._overlayView.scanSelectBtn.clicked.connect(self.doOverlay)

        self._bkgHandling = iintBackgroundHandling.iintBackgroundHandling(self._control.getBKGDicts())
        self._bkgHandling.bkgmodel.connect(self._control.setBkgModel)

        self._fitList = []
        self._fitWidgets = []

        self._signalFitting = iintSignalFitting.iintSignalFitting(self._control.getFitModels())
        self._signalFitting.models.connect(self.openFitConfigurationDialog)
        self._signalFitting.autogauss.connect(self._control.useGuessSignalFit)
        self._signalFitting.fitButton.clicked.connect(self._prepareSignalFitting)

        self._inspectAnalyze = iintInspectAnalyze.iintInspectAnalyze()
        self._inspectAnalyze.trackedColumnsPlot.clicked.connect(self._runTrackedControlPlots)
        self._inspectAnalyze.showScanFits.clicked.connect(self._runScanControlPlots)
        self._inspectAnalyze.polAnalysis.clicked.connect(self._runPolarizationAnalysis)
        self._inspectAnalyze.saveResults.clicked.connect(self._saveResultsFiles)

        self._saveResultsDialog = selectResultOutput.SelectResultOutput()
        self._saveResultsDialog.accept.connect(self._control.setResultFilename)
        self._saveResultsDialog.accept.connect(self.runOutputSaving)

        self._loggingBox = loggerBox.LoggerBox()

        self.verticalLayout = QtGui.QVBoxLayout()
        self.scrollAreaContents.setLayout(self.verticalLayout)
        self.scrollArea2.setWidget(self.imageTabs)

        self.verticalLayout.addWidget(self._fileInfo)
        self.verticalLayout.addWidget(self._outDir)
        self.verticalLayout.addWidget(self._obsDefBox)
        self.verticalLayout.addWidget(self._bkgHandling)
        self.verticalLayout.addWidget(self._signalFitting)
        self.verticalLayout.addWidget(self._inspectAnalyze)
        self.verticalLayout.addWidget(self._loggingBox)

        self._sfrGUI.valuesSet.connect(self._resetForFR)
        self._ffrGUI.valuesSet.connect(self._resetForFR)
        self._sfrGUI.valuesSet.connect(self.runFileReader)
        self._ffrGUI.valuesSet.connect(self.runFileReader)
        self._obsDef.observableDicts.connect(self.runObservable)
        self._bkgHandling.bkgDicts.connect(self.runBkgProcessing)
        self._bkgHandling.noBKG.connect(self._noBackgroundToggle)
        self._simpleImageView.printButton.clicked.connect(self._printDisplayedData)

        self._initialGeometry = self.geometry()
        self._widgetList = []
        self._trackedDataDict = {}
        self._resultTabIndices = []
        self._resultFileName = None
        self._outDir.newdirectory.connect(self._control.setOutputDirectory)

        if configFile is not None:
            try:
                self.loadConfig(configFile)
            except(FileNotFoundError):
                self.warning("Failed to read the initial config file, file could not be found.")
            except(adaptException.AdaptFileReadException):
                self.warning("Failed to read the initial config file.\n" +
                             "Check for a spelling error, an inconstency within or it doesn't exist.")

    def _unresize(self):
        # this is the place any resizing code could/should go
        # i can't seem to get it to work, though
        pass

    def _resetInternals(self):
        self._motorname = ""
        del self._widgetList[:]
        self._trackedDataDict.clear()
        self._rawdataobject = None
        del self._blacklist[:]
        del self._fitList[:]
        self._resultFileName = None

    def _resetAll(self):
        self._resetInternals()
        self._simpleImageView.reset()
        self._overlayView.reset()
        self._fileInfo.reset()
        self._obsDef.reset()
        self._bkgHandling.reset()
        self._bkgHandling.setParameterDicts(self._control.getBKGDicts())
        self._signalFitting.reset()
        self._signalFitting.deactivateFitting()
        self._control.resetAll()
        self._sfrGUI.reset()
        self._ffrGUI.reset()
        self.resetTabs()
        try:
            self._trackedDataChoice.reset()
            self._trackedDataChoice.close()
            self._trackedDataChoice = None
        except AttributeError:
            pass
        try:
            self._overlaySelection.reset()
            self._overlaySelection.close()
        except AttributeError:
            pass
        self._inspectAnalyze.reset()
        self.message("Cleared all data and processing configuration.")

    def _resetForFR(self):
        self._resetInternals()
        self._simpleImageView.reset()
        self._overlayView.reset()
        self._obsDef.reset()
        self._bkgHandling.reset()
        self._bkgHandling.setParameterDicts(self._control.getBKGDicts())
        self._signalFitting.reset()
        self._signalFitting.deactivateFitting()
        self._control.resetAll()
        self.resetTabs()
        self._inspectAnalyze.reset()
        try:
            self._trackedDataChoice.reset()
            self._trackedDataChoice.close()
            self._trackedDataChoice = 0
        except AttributeError:
            pass
        try:
            self._overlaySelection.reset()
            self._overlaySelection.close()
        except AttributeError:
            pass
        self.message("Cleared all data and processing configuration.")

    def resetTabs(self, keepSpectra=False):
        if keepSpectra:
            ivtab = self.imageTabs.indexOf(self._simpleImageView)
            while self.imageTabs.count() > 1:
                for tab in range(self.imageTabs.count()):
                    if tab != ivtab:
                        self.imageTabs.removeTab(tab)
                        continue
        else:
            while self.imageTabs.count() >= 1:
                for tab in range(self.imageTabs.count()):
                    self.imageTabs.removeTab(tab)
            self.imageTabs.hide()
        self._dataTabIndex = None

    def resetResultTabs(self, keepSpectra=False):
        self._resultTabIndices = list(set(self._resultTabIndices))
        self._resultTabIndices.sort(reverse=True)
        if keepSpectra:
            for index in self._resultTabIndices:
                self.imageTabs.removeTab(index)
        else:
            while self.imageTabs.count() >= 1:
                for tab in range(self.imageTabs.count()):
                    self.imageTabs.removeTab(tab)
            self.imageTabs.hide()
        self._resultTabIndices.clear()

    def _checkTabClosing(self, index):
        if self._dataTabIndex is not None:
            if index is not self._dataTabIndex:
                self.message("Closing tab " + str(self.imageTabs.tabText(index)))
                self.imageTabs.removeTab(index)
            else:
                self.message("Won't close the scan display tab.")

    def closeEvent(self, event):
        event.ignore()
        self._closeApp()

    def _showConfig(self):
        try:
            if self._file != "":
                self._widgetList.append(showFileContents.ShowFileContents(open(self._file).read()))
            else:
                return
        except AttributeError:
            self.message("Can't show config file, since none is present (yet).\nSave the config file first (see File Menu).\n")

    def _showSpecFile(self):
        try:
            self._widgetList.append(showFileContents.ShowFileContents(open(self._sfrGUI.getParameterDict()["filename"]).read()))
        except TypeError:
            self.message("Can't show spec file, since none has been selected yet.\nOpen a spec file first (see File Menu).\n")
        return

    def _showFIOFiles(self):
        try:
            text = ''
            for fiofile in self._ffrGUI.getParameterDict()["filenames"]:
                text += "Filename: " + str(fiofile)
                text += open(fiofile).read()
                text += 80*"*" + "\n" + 80*"*" + "\n" + 80*"*" + "\n\n\n"
            self._widgetList.append(showFileContents.ShowFileContents(text))
        except TypeError:
            self.message("Can't show fio file(s), since none has been selected yet.\nFirst open fio file(s) (see File Menu).\n")
        return

    def _showResultsFile(self):
        try:
            self._widgetList.append(showFileContents.ShowFileContents(open(self._resultFileName).read()))
        except TypeError:
            self.message("Can't show results file, there is none yet.\nFirst save a result file (see Analysis section).\n")

    def _showFitResults(self):
        self._widgetList.append(showFileContents.ShowFileContents(''.join(self._control.getSignalFitResults())))

    def _showIintGuiInfo(self):
        self._widgetList.append(showAboutIintGUI.ShowAboutIintGUI())

    def _showHelp(self):
        self._widgetList.append(showIintGUIHelp.ShowIintGUIHelp())

    # LOG WINDOW DISPLAY::Messages
    def message(self, text):
        self._loggingBox.addText(text)

    # LOG WINDOW DISPLAY::Warnings!
    def warning(self, text):
        self._loggingBox.addRedText(text)

    def _closeApp(self):
        for i in self._widgetList:
            i.close()
        del self._widgetList[:]
        self._quit.show()

    def _saveConfig(self, num=None):
        try:
            savename, timesuffix = self._control.proposeSaveFileName('')
        except TypeError:
            self.warning("Nothing to save (yet?).")
            return
        except AttributeError:
            self.warning("There is nothing to save (yet?).")
            return
        self._control.saveConfig(savename + ".icfg")
        self._control.saveConfig(savename + timesuffix + ".icfg")
        self._file = savename + timesuffix + ".icfg"
        self.message("Saved config file " + str(savename) + ".\n")
        return

    def _askReset(self):
        if self._control.getSFRDict()["filename"] is None:
            self._resetAll()
        else:
            self._resetQuestion.show()

    def showSFRGUI(self):
        self._sfrGUI.show()

    def showFFRGUI(self):
        self._ffrGUI.show()

    def chooseAndLoadConfig(self):
        try:
            prev = self._file
        except:
            prev = None
        if self._testMode:
            pass
        else:
            self._file = QtGui.QFileDialog.getOpenFileName(self, 'Choose iint config file', '.', "iint cfg files (*.icfg)")
        if self._file != "":
            if prev is not None:
                self._resetAll()
            from adapt import configurationHandler
            handler = configurationHandler.ConfigurationHandler()
            self._procconf = handler.loadConfig(self._file)
            self._initializeFromConfig()

    def loadConfig(self, cfgfile):
        if cfgfile is not None:
            try:
                prev = self._file
            except:
                self._file = cfgfile
                prev = None
            if self._file != "":
                if prev is not None:
                    self._resetAll()
                from adapt import configurationHandler
                handler = configurationHandler.ConfigurationHandler()
                self._procconf = handler.loadConfig(self._file)
                self._initializeFromConfig()

    def _initializeFromConfig(self):
        # clear the memory!
        self._resetAll()
        # reset logic is screwed up
        # first load the config into the actual description
        runlist = self._control.loadConfig(self._procconf)
        # the next step is to set the gui up to reflect all the new values
        if "specread" in runlist:
            # check the type !
            self._sfrGUI.setParameterDict(self._control.getSFRDict())
            self.runFileReader("spec")
        elif "fioread" in runlist:
            self._ffrGUI.setParameterDict(self._control.getFFRDict())
            self.runFileReader("fio")
        else:
            return
        if "observabledef" in runlist:
            self._obsDef.setParameterDicts(self._control.getOBSDict(), self._control.getDESDict())
            self._obsDef.activateShowScanProfile()
        else:
            return
        if "bkgsubtract" in runlist:
            self._bkgHandling.setParameterDicts(self._control.getBKGDicts(), active=True)
            self.runBkgProcessing(self._control.getBKGDicts()[0], self._control.getBKGDicts()[1], self._control.getBKGDicts()[2], self._control.getBKGDicts()[3], reset=False)
        else:
            return
        if "signalcurvefit" in runlist:
            self._signalFitting.setParameterDict(self._control.getSIGDict())
            self.runSignalProcessing(self._control.getSIGDict()['model'], reset=False)
        else:
            return

    def _updateDisplay(self):
        self.plotit()
        self._bkgHandling.activate()
        self._signalFitting.activateConfiguration()
        self._inspectAnalyze.activate()

    def runFileReader(self, reader=None):
        if reader == "spec" or reader is None:
            self._control.setReaderType("spec")
            filereaderdict = self._sfrGUI.getParameterDict()
            self._fileInfo.setNames(filereaderdict["filename"], filereaderdict["scanlist"])
            self._control.setSpecFile(filereaderdict["filename"], filereaderdict["scanlist"])
            self.message("Reading spec file: " + str(filereaderdict["filename"]))
            try:
                sfr = self._control.createAndInitialize(filereaderdict)
            except(adaptException.AdaptFileReadException):
                self.warning("Failed to read the spec file.  Please check the file in question.")
                return
            self._control.createDataList(sfr.getData(), self._control.getRawDataName())
            self._control.setDefaultOutputDirectory(filereaderdict["filename"])
        elif reader == "fio":
            self._control.setReaderType("fio")
            filereaderdict = self._ffrGUI.getParameterDict()
            try:
                self._control.setFioFile(filereaderdict["filenames"])
            except:
                self.warning("FIO file(s) cannot be read in, there is something malformed.")
                return
            self.message("Reading fio file(s): " + str(filereaderdict["filenames"]))
            try:
                ffr = self._control.createAndBulkExecute(filereaderdict)
            except(adaptException.AdaptFileReadException):
                self.warning("Failed to read the FIO file(s). Please check the file in question.")
                return
            self._control.createDataList(ffr.getData(), self._control.getRawDataName())
            self._control.setDefaultOutputDirectory(filereaderdict["filenames"][0])
            self._fileInfo.setNames(filereaderdict["filenames"][0] + ", ...", str(self._control.getScanlist()))
        self._outDir.setOutputDirectory(self._control.getOutputDirectory())
        check = self._control.checkDataIntegrity()
        if check:
            self.warning("There are different motor names in the selection!\n Can't continue, please correct!")
            return
        # do the range checking for background equalization
        ranges = self._control.checkScanRanges()
        if len(ranges) > 0:
            text = '''Take notice: the individual scan commands within the chosen scan series differ in range.
                      Explicitly:'''  + str(ranges) + \
                    '''\nPlease confirm, that the background integral is calculated only within the shared range along the chosen motor.'''
            self.warning(text)
            from . import backgroundIntegralDialog
            d = backgroundIntegralDialog.BackgroundIntegralDialog(text)
            bla = d.exec_()

        # pass info to the observable definition part
        self._obsDef.passInfo(self._control.getRawDataObject(), self._control.getMotorName())
        self.message("... done.\n")

    def setMotorName(self, name):
        self._control.setMotorName(name)

    def runObservable(self, obsDict, despDict, reset=True):
        if obsDict != self._control.getOBSDict():
            self._control.setOBSDict(obsDict)
        if reset:
            self._simpleImageView.reset()
            self._overlayView.reset()
            self.resetTabs(keepSpectra=True)
            self._control.resetOBSdata()
            self._inspectAnalyze.reset()
            self._control.resetBKGdata()
            self._bkgHandling.setParameterDicts(self._control.getBKGDicts())
            self._control.resetSIGdata()
            self._control.resetFITdata()

        self.message("Computing the intensity...")
        self._control.createAndBulkExecute(obsDict)
        self.message(" and plotting ...")
        self.plotit()
        # just check if this works, still unclear of the trigger...
        self._control.settingChoiceDesBkg()

        # check whether despiking is activated, otherwise unset names
        if despDict != {}:
            if despDict != self._control.getDESDict():
                self._control.setDESDict(despDict)
            self._control.useDespike(True)
            self._control.createAndBulkExecute(despDict)
            if(self._simpleImageView is not None):
                self._simpleImageView.update("des")
        self._bkgHandling.activate()
        self._signalFitting.activateConfiguration()
        self.message(" done.\n")

    def doOverlay(self):
        try:
            self._overlaySelection.passData(self._control.getScanlist())
            if self._testMode:
                pass
            else:
                self._overlaySelection.show()
        except AttributeError:
            self._overlaySelection = iintOverlaySelection.iintOverlaySelection(datalist=self._control.getScanlist())
            self._overlaySelection.passData(self._control.getScanlist())
            if self._testMode:
                pass
            else:
                self._overlaySelection.show()
        self._overlaySelection.overlayscanlist.connect(self._showOverlay)

    def _showOverlay(self, selection):
        try:
            self._overlayView.passData(selection,
                                       self._control.getDataList(),
                                       self._control.getMotorName(),
                                       self._control.getObservableName(),
                                       self._control.getDespikedObservableName(),
                                       self._control.getBackgroundName(),
                                       self._control.getSignalName(),
                                       self._control.getFittedSignalName(),
                                       )
            self.imageTabs.setCurrentIndex(self.imageTabs.addTab(self._overlayView, "Overlay"))
            self.imageTabs.show()
            self._overlayView.plot()
            self._overlayView.show()
        except KeyError:
            self.warning("Nothing to plot yet, first define the signal.")
            pass

    def _openzvalchoice(self):
        rawScanData = self._control.getDataList()[0].getData(self._control.getRawDataName())
        self._tmpdialog = iintZValueSelection.iintZValueSelection(rawScanData.getLabels(), self._control.getObservableName())
        self._tmpdialog.zvalue.connect(self._runScanProfiles)

    def _runScanProfiles(self, zval):
        self._control.setZValueInProfilePlot(zval)
        name, timesuffix = self._control.proposeSaveFileName()
        filename = name + "-" + str(zval) + "_scanProfiles.pdf"
        self.message("Creating the scan profile plot ...")
        self._control.processScanProfiles(filename)
        self.message(" ... done.\n")
        from subprocess import Popen
        Popen(["evince", filename])
        self._tmpdialog = None

    def _runMCA(self):
        name, timesuffix = self._control.proposeSaveFileName()
        filename = name + "_mca.pdf"
        self.message("Creating the MCA plots ...")
        self._control.processMCAPlots(filename)
        self.message(" ... done.\n")
        from subprocess import Popen
        Popen(["evince", filename])

    def runBkgProcessing(self, selDict, fitDict, calcDict, subtractDict, reset=True):
        if reset:
            self.resetResultTabs(keepSpectra=True)
            self._inspectAnalyze.reset()
            self._control.resetSIGdata()
            self._control.resetFITdata()
            self._control.resetBKGdata()
            self._bkgHandling.setParameterDicts(self._control.getBKGDicts())
            self._signalFitting.deactivateFitting()
        self.message("Fitting background ...")

        if selDict == {}:
            self._control.useBKG(False)
            self.message("... nothing to be done.\n")
            return
        self._control.useBKG(True)
        try:
            self._control.createAndBulkExecute(selDict)
        except ValueError:
            self.warning("Can't use the selection of the background points, please recheck.")
            return
        try:
            self._control.createAndBulkExecute(fitDict)
        except ValueError:
            self.warning("Can't fit the background; e.g. maybe there are nan values.")
            return
        try:
            self._control.performBKGIntegration()
        except:
            self.warning("Background integration failed.")
        self._control.createAndBulkExecute(calcDict)
        self._control.createAndBulkExecute(subtractDict)
        if(self._simpleImageView is not None):
            self._simpleImageView.update("bkg")
        self.message(" ... done.\n")
        self._signalFitting.activateFitting()

    def _noBackgroundToggle(self, nobkg):
        self._control.resetBKGdata()
        self.resetResultTabs(keepSpectra=True)
        if nobkg is 1:
            self._control.useBKG(False)
        elif nobkg is 0:
            self._control.useBKG(True)
        if nobkg is 1:
            if(self._simpleImageView is not None):
                self._simpleImageView.update("nobkg")
            self._signalFitting.activateFitting()
            self._inspectAnalyze.deactivate()
            self._control.removeBKGparts()
        else:
            self._signalFitting.deactivateFitting()
            self._inspectAnalyze.deactivate()
            try:
                self._simpleImageView.update("unplotfit")
            except:
                self.warning("Please inform the developer; this is a new issue.")

    def plotit(self):
        # pyqt helper stuff
        self._simpleImageView.passData(self._control.getDataList(),
                                       self._control.getMotorName(),
                                       self._control.getObservableName(),
                                       self._control.getDespikedObservableName(),
                                       self._control.getBackgroundName(),
                                       self._control.getSignalName(),
                                       self._control.getFittedSignalName(),
                                       )
        self._simpleImageView.plot()
        self._dataTabIndex = self.imageTabs.addTab(self._simpleImageView, "Scan display")
        self.imageTabs.setCurrentIndex(self._dataTabIndex)
        self.imageTabs.show()
        self._simpleImageView.show()
        self._simpleImageView.plot()

    def openFitConfigurationDialog(self, names):
        del self._fitList[:]
        del self._fitWidgets[:]
        # first build the fit list !
        self._fitList = self._control.createFitFunctions(names)
        try:
            self._configWidget.reset()
        except AttributeError:
            self._configWidget = iintFitConfiguration.iintFitConfiguration()
        data = self._simpleImageView.getCurrentSignal()

        # first check if the sum widget needs to be shown
        if len(self._fitList) > 1:
            self._configWidget.showSumPart()

        for i in self._fitList:
            # from the fits get the widget, keep it for reference and add it
            tw = i.getWidget(data[0], data[1], name=str(self._fitList.index(i)))
            self._fitWidgets.append(tw)
            self._configWidget.addWidget(tw)
            tw.updateFit.connect(self._updateCurrentImage)
            tw.update()
        # if the model is made up from more than one part
        # create the sum model
        # MISSING: connect the signals from the config widget
        self._configWidget.testButton.clicked.connect(self.runSingleTestFit)
        self._configWidget.doneButton.clicked.connect(self._simpleImageView.removeGuess)
        self._configWidget.doneButton.clicked.connect(self._signalFitting.allowFitButton)
        self._configWidget.cancelButton.clicked.connect(self._cleanUpFit)
        self._configWidget.sumColourChanged.connect(self._updateCurrentImage)

    def _cleanUpFit(self):
        del self._fitList[:]
        del self._fitWidgets[:]
        self._simpleImageView.removeGuess()

    def _updateCurrentImage(self):
        # called by signal from fit config window
        # do: collect all info and piece it together
        tmpFits = []
        for wi in self._fitWidgets:
            tmpFits.append(wi.getCurrentFitData())
        # now get the fake exchange object if needed:
        if len(tmpFits) > 1:
            tmpObject = self._control.getSumExchangeObject(tmpFits, self._configWidget.getSumColour())
            tmpFits.append(tmpObject)
        try:
            # can fail if the model is constant; then the stupid signature is different. ignore!
            self._simpleImageView.plotFit(tmpFits)
        except:
            pass

    def _prepareSignalFitting(self):
        fitDict = {}
        # the config parts are inside the widget part, not the actual fit
        for fit in self._fitWidgets:
            fitDict.update(fit.getCurrentParameterDict())
        self.runSignalProcessing(fitDict, reset=True)

    def runSignalProcessing(self, fitDict, reset=True):
        # run two steps here:
        # first the trapezoid summation
        self.message("Signal processing: first trapezoidal integration ...")
        self._control.resetTRAPINTdata()
        self._control.createAndBulkExecute(self._control.getTrapIntDict())
        self.message(" ... done.")
        # second run the actual fitting; separate function call
        self.runSignalFitting(fitDict, reset)

    def runSignalFitting(self, fitDict, reset):
        # now run the signal fitting
        if reset:
            self._inspectAnalyze.reset()
        rundict = self._control.getSIGDict()
        self.message("Fitting the signal, this can take a while ...")
        # this is a bad idea; this is specific code and needs to be put into the control part!!
        if self._control.guessSignalFit():
            rundict['model'] = {"m0_": {'modeltype': "gaussianModel",
                                        'm0_center': {'value': 1.},
                                        'm0_amplitude': {'value': 2.},
                                        'm0_height': {'value': 22.},
                                        'm0_fwhm': {'value': 21.},
                                        'm0_sigma': {'value': 3.}}}
        else:
            rundict['model'] = fitDict
        if self._control.createAndBulkExecute(rundict) == "stopped":
            self._inspectAnalyze.reset()
            self._simpleImageView.update("unplotfit")
            return
        if self._control.createAndBulkExecute(self._control.getSignalFitDict()) == "stopped":
            self._inspectAnalyze.reset()
            self._simpleImageView.update("unplotfit")
            return
        if(self._simpleImageView is not None):
            self._simpleImageView.update("plotfit")

        # first show the tracked stuff, since it removes all other tabs
        self._doPostFitActions()

        # critical here, something doesn't work any longer; take it out
        # tdv.pickedTrackedDataPoint.connect(self._setFocusToSpectrum)
        self.message(" ... done.\n")
        self._inspectAnalyze.activate()
        self._control.useSignalProcessing(True)

    def runSingleTestFit(self):
        # single use function -- not the best way, but how to do it differently?
        fitDict = {}
        # the config parts are inside the widget part, not the actual fit
        for fit in self._fitWidgets:
            fitDict.update(fit.getCurrentParameterDict())
        rundict = self._control.getTestFitDict()
        self.message("Single test fit executing ....")
        # get the fit parameters for running
        rundict['model'] = fitDict
        index = self._simpleImageView.getCurrentIndex()
        self._control.createAndSingleExecute(rundict, index)
        # now fit is done, create points for drawing
        self._control.createAndSingleExecute(self._control.getSingleFitDict(), index)
        self.message("... test fit finished, now displaying.")
        self._simpleImageView.plotSingleFit(index, name=self._control.getSingleFitPointsName())

    def _printDisplayedData(self):
        dataDict = self._simpleImageView.getPrintData()
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_pdf import PdfPages
        name, timesuffix = self._control.proposeSaveFileName()
        filename = name + "_" + str(timesuffix) + "_SingleScan-#" + str(dataDict['scannumber']) + ".pdf"
        _outfile = PdfPages(filename)
        fig_size = plt.rcParams["figure.figsize"]
        # print "Current size:", fig_size
        fig_size[0] = 16
        fig_size[1] = 12
        plt.rcParams["figure.figsize"] = fig_size
        # the plotting commands
        try:
            plt.plot(dataDict['motor'], dataDict['raw'], 'k+', label="raw intensities")
        except KeyError:
            pass
        try:
            plt.plot(dataDict['motor'], dataDict['despike'], 'gx', label="despiked intensities")
        except KeyError:
            pass
        try:
            plt.plot(dataDict['motor'], dataDict['bkg'], 'rd', label="estimated bkg")
        except KeyError:
            pass
        try:
            plt.plot(dataDict['motor'], dataDict['signal'], 'bo', label="signal intensities")
        except KeyError:
            pass
        try:
            plt.plot(dataDict['motor'], dataDict['fit'], 'b-', label="fitted intensities")
        except KeyError:
            pass
        plt.xlabel(self._simpleImageView.getAxisNames()[0])
        plt.ylabel(self._simpleImageView.getAxisNames()[1])
        plt.legend()
        # index/argument correct?
        figure = plt.figure(1)
        figure.suptitle('Scan number ' + str(dataDict['scannumber']), fontsize=14, fontweight='bold')

        _outfile.savefig()
        _outfile.close()
        plt.close("all")
        self.message("Created scan file.\n")
        from subprocess import Popen
        Popen(["evince", filename])

    def _runScanControlPlots(self):
        name, timesuffix = self._control.proposeSaveFileName()
        filename = name + "_" + str(timesuffix) + "_scanControlPlots.pdf"
        self.message("Creating the scan control plots of the fits ...")
        self._control.processScanControlPlots(filename)
        self.message(" ... done.\n")
        from subprocess import Popen
        Popen(["evince", filename])

    def _runTrackedControlPlots(self):
        try:
            modelname = self._control.getSignalFitModel()
            if modelname != "gaussianModel" and modelname != "lorentzianModel":
                self.warning("Can't create the wanted plots, the fit model has to be either gaussian or lorentzian.")
                return
        except:
            pass
        name, timesuffix = self._control.proposeSaveFileName()
        filename = name + "_" + str(timesuffix) + "_trackedColumnsPlots.pdf"
        self.message("Creating the control plots of the tracked columns ...")
        self._control.processTrackedColumnsControlPlots(filename)
        self.message(" ... done.\n")
        from subprocess import Popen
        Popen(["evince", filename])

    def _runPolarizationAnalysis(self):
        self.message("Running the polarization analysis ...")
        polanadict = self._control.getPOLANADict()
        filename = polanadict["outputname"] + "_polarizationAnalysis.pdf"
        try:
            self._control.processAll(polanadict)
        except adaptException.AdaptProcessException:
            self.warning("Polarization analysis cannot be performed on this dataset. Maybe the dimensions are incorrect?")
            return
        self.message(" ... done.\n")
        from subprocess import Popen
        Popen(["evince", filename])

    def _setFocusToSpectrum(self, title, name, xpos, ypos):
        # very special function; lots of assumptions
        import math
        xvallist = self._trackedDataDict[title].getTrackedValues()
        yvallist = [i[0] for i in self._trackedDataDict[title].getFitParameterValue(name)]
        xindices = []
        yindices = []
        # since numpy does not provide a approximate 'where', iterate manually
        for xval in xvallist:
            if math.fabs(xval - xpos) < 0.00001:
                xindices.append(xvallist.index(xval))
        for yval in yvallist:
            if math.fabs(yval - ypos) < 0.00001:
                yindices.append(yvallist.index(yval))
        if len(xindices) == 1 and len(yindices) == 1:
            if xindices[0] == yindices[0]:
                self._simpleImageView.setCurrentIndex(xindices[0])
                self.imageTabs.setCurrentIndex(self.imageTabs.indexOf(self._simpleImageView))

    def _dataToTrack(self):
        self._currentTrackedHeaderData = set(self._control.getTrackedHeaderData())
        self._currentTrackedColumnData = set(self._control.getTrackedColumnData())
        try:
            self._trackedDataChoice.show()
        except AttributeError:
            rawScanData = self._control.getDataList()[0].getData(self._control.getRawDataName())
            self._trackedDataChoice = iintTrackedDataChoice.iintTrackedDataChoice(rawScanData, self._control.getTrackedHeaderData(), self._control.getTrackedColumnData())

            self._trackedDataChoice.trackedData.connect(self._control.setTrackedData)
            self._trackedDataChoice.trackedData.connect(self._checkTrackMapActivation)
            self._trackedDataChoice.trackedData.connect(self._checkChangesInTrackedData)

            self._trackedDataMap = trackedDataMap.TrackedDataMap()
            self._trackedDataMap.trackeddatatomap.connect(self._addMappedData)

            self._obsDef.maptracks.clicked.connect(self._trackedDataMap.show)

    def _checkTrackMapActivation(self, hlist, clist):
        if len(hlist + clist) > 0:
            self._obsDef.activateMapTrack()
            self._trackedDataMap.passNames(self._control.getTrackedHeaderData(), self._control.getTrackedColumnData())
        else:
            self._obsDef.deactivateMapTrack()

    def _checkChangesInTrackedData(self, hlist, clist):
        if( self._currentTrackedHeaderData != set(hlist) or self._currentTrackedColumnData != set(clist)):
            try:
                self._doPostFitActions()
            except(KeyError):
                pass

    def _doPostFitActions(self):
        # prepare the tabs and dict of tracked data for re-display
        self._trackedDataDict.clear()
        # remove older "Fit vs. xxx" tabs
        for index in range(self.imageTabs.__len__(), 0, -1):
            if (self.imageTabs.tabText(index)).startswith("Fit vs."):
                self.imageTabs.removeTab(index)

        # first iterate over header data
        for name in self._control.getTrackedHeaderData():
            trackinfo = self._control.getTrackInformation(name, header=True)
            tdv = iintMultiTrackedDataView.iintMultiTrackedDataView(trackinfo, self._blacklist)
            self._trackedDataDict[trackinfo.getName()] = trackinfo
            tmpindex = self.imageTabs.addTab(tdv, "Fit vs. " + str(trackinfo.getName()))
            self._resultTabIndices.append(tmpindex)
            self.imageTabs.setCurrentIndex(tmpindex)
            tdv.pickedTrackedDataPoint.connect(self._setFocusToSpectrum)

        # then iterate over columns, this is not elegant
        for name in self._control.getTrackedColumnData():
            trackinfo = self._control.getTrackInformation(name, header=False)
            tdv = iintMultiTrackedDataView.iintMultiTrackedDataView(trackinfo, self._blacklist)
            self._trackedDataDict[trackinfo.getName()] = trackinfo
            tmpindex = self.imageTabs.addTab(tdv, "Fit vs. " + str(trackinfo.getName()))
            self._resultTabIndices.append(tmpindex)
            self.imageTabs.setCurrentIndex(tmpindex)
            tdv.pickedTrackedDataPoint.connect(self._setFocusToSpectrum)

        trackinfo = self._control.getDefaultTrackInformation()
        tdv = iintMultiTrackedDataView.iintMultiTrackedDataView(trackinfo)
        self._trackedDataDict[trackinfo.getName()] = trackinfo
        tmpindex = self.imageTabs.addTab(tdv, ("Fit vs. " + trackinfo.getName()))
        self._resultTabIndices.append(tmpindex)
        self.imageTabs.setCurrentIndex(tmpindex)

    def _addMappedData(self, one, two):
        mtdmd = iintTrackedDataMapDisplay.iintTrackedDataMapDisplay(
                            one, self._control.getRawTrackInformation(one),
                            two, self._control.getRawTrackInformation(two))

        mtdmd.maperror.connect(self.warning)
        mtdmd.plot()
        self.message("Displaying " + str(one) + " versus " + str(two) + ".")
        self.imageTabs.setCurrentIndex(self.imageTabs.addTab(mtdmd, one + " vs. " + two))
        self.imageTabs.show()

    def _saveResultsFile(self):
        name, timesuffix = self._control.proposeSaveFileName()
        self._saveResultsDialog.setName(name+timesuffix)
        self._saveResultsDialog.show()

    def _saveResultsFiles(self):
        name, timesuffix = self._control.proposeSaveFileName()
        self._saveResultsDialog.setName(name+timesuffix)
        self._saveResultsDialog.show()

    def runOutputSaving(self):
        self._control.useFinalizing(True)
        finalDict = self._control.getFinalizingDict()
        self.message("Saving results files, might take a while ...")
        self._control.processAll(finalDict)
        self._resultFileName = finalDict["outfilename"]
        self.message("saving file: " + str(self._resultFileName))
        filename = self._control.getResultBaseFilename()
        self.message("... processing the scan profile plots: " + str(filename + "_scanProfiles.pdf"))
        self._control.processScanProfiles(filename + "_scanProfiles.pdf")
        self.message("... processing the plots of the tracked data: " + str(filename + "_trackedColumnsPlots.pdf"))
        self._control.processTrackedColumnsControlPlots(filename + "_trackedColumnsPlots.pdf")
        self.message("...and finally the control plots of the scans: " + str(filename + "_scanControlPlots.pdf"))
        self._control.processScanControlPlots(filename + "_scanControlPlots.pdf")
        self.message(" ... done.\n")

    def _retrackDataDisplay(self, blacklist):
        self._blacklist = blacklist
        # if the blacklist has been changed, re-display the tracked data
        ivtab = self.imageTabs.indexOf(self._simpleImageView)

        while self.imageTabs.count() > 1:
            for tab in range(self.imageTabs.count()):
                if tab != ivtab:
                    self.imageTabs.removeTab(tab)
                    continue

        for k, v in self._trackedDataDict.items():
            tdv = iintMultiTrackedDataView.iintMultiTrackedDataView(v, blacklist)
            tdv.pickedTrackedDataPoint.connect(self._setFocusToSpectrum)
            tmpindex = self.imageTabs.addTab(tdv, k)
            self._resultTabIndices.append(tmpindex)
            self.imageTabs.setCurrentIndex(tmpindex)

    def _showInspectionPlots(self):
        tempDict = self._control.getInspectionDict()
        filename = tempDict["outputname"] + '_controlPlots.pdf'
        self.message("Generating temporary control plots ...")
        self._control.processAll(tempDict)
        self.message(" ... done.\n")
        from subprocess import Popen
        Popen(["evince", filename])
