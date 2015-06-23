from PySteppables import *
from PySteppablesExamples import MitosisSteppableBase
import CompuCell
import sys
from random import uniform
from random import seed
from random import expovariate 
import math
from math import sqrt

class CellMigration2DSteppable(SteppableBasePy):    
    def __init__(self,_simulator,_frequency=1):
        SteppableBasePy.__init__(self,_simulator,_frequency)

    def start(self):
	pass
    def step(self,mcs):        
        pass                       
    def finish(self):
        # Finish Function gets called after the last MCS
	pass

class PolarityEvolutionSteppable(SteppableBasePy):
    def __init__(self,_simulator,_frequency=1):
        SteppableBasePy.__init__(self,_simulator,_frequency)
        
        self.vectorPolarityField=self.createVectorFieldCellLevelPy("PolarityField")
    def start(self):
        
        IDCount = 1;
        
        for cell in self.cellListByType(1,2):
                cellDict=self.getDictionaryAttribute(cell)
                
                cellDict["ID"] = IDCount;
                IDCount = IDCount+1;
                
                cellDict["comX"] = [cell.xCOM]
                cellDict["comY"] = [cell.yCOM]
                
                for i in range(10,1,-1):
                    cellDict["comX"].append(cell.xCOM)
                    cellDict["comY"].append(cell.yCOM)
                
                seed()
                avgX = uniform(-1.0,1.0);
                seed()
                avgY = uniform(-1.0,1.0);
                
                #print "avgXY",avgX,avgY
                if avgX!=0 or avgY!=0:
                    norm = sqrt(avgX**2 + avgY**2)
                    cellDict["vecX"]  = avgX/norm
                    cellDict["vecY"]  = avgY/norm
                #print "norm,vecX,vecY",norm,cellDict["vecX"],cellDict["vecY"]
                    
                if cell.type == 1:
                    mu = 50
                if cell.type == 2:
                    mu = 50
                self.vectorPolarityField[cell] = [cellDict["vecX"],cellDict["vecY"],0]
                
                cell.lambdaVecX=mu*cellDict["vecX"] # force component along X axis
                cell.lambdaVecY=mu*cellDict["vecY"]# force component along Y axis
                cell.lambdaVecZ=0.0 # force component along Z axis
                
    def step(self,mcs):
        
        #self.vectorPolarityField.clear()
        
        tau = 10;
        for cell in self.cellListByType(1,2):
            cellDict=self.getDictionaryAttribute(cell)
            
            for i in range(0,tau-1):
                cellDict["comX"][i]  = cellDict["comX"][i+1]
                cellDict["comY"][i]  = cellDict["comY"][i+1]    
                
            cellDict["comX"][tau-1]  = cell.xCOM;
            cellDict["comY"][tau-1]  = cell.yCOM;

            #print "Centroid",cell.xCOM,cell.yCOM
            
            avgX = 0;
            avgY = 0;
            sumX = 0;
            sumY = 0;
            norm = 0;
            
            if(mcs<9):
                seed()
                avgX = uniform(-1.0,1.0);
                seed()
                avgY = uniform(-1.0,1.0);
                
                if avgX!=0 or avgY!=0:
                    norm = sqrt(avgX**2 + avgY**2)
                    cellDict["vecX"]  = avgX/norm
                    cellDict["vecY"]  = avgY/norm
                            
            else:    
                for i in range(0,tau-1,1):
                    diffX = cellDict["comX"][i+1] - cellDict["comX"][i]
                    diffY = cellDict["comY"][i+1] - cellDict["comY"][i]
            
                    sumX  = sumX + diffX
                    sumY  = sumY + diffY
                    
#                     fileName='Local'+str(cellDict["ID"])+'.csv'
#                     try: 
#                         fileHandle,fullFileName=self.openFileInSimulationOutputDirectory(fileName,"a")
#                     except IOError:
#                         print "Could not open file ", fileName," for writing. "
#                         return
                
#                     cellDict=self.getDictionaryAttribute(cell)
#                     print >>fileHandle,mcs,",",cellDict["comX"][i],",",cellDict["comY"][i],",",cellDict["comX"][i+1],",",cellDict["comY"][i+1],",",diffX,",",diffY,",",sumX,",",sumY,",",avgX,",",avgY
#                     fileHandle.close()

                avgX = -sumX/(tau-1);
                avgY = -sumY/(tau-1);
                
                norm = 0
                if avgX!=0 or avgY!=0:
                        norm = sqrt(avgX**2 + avgY**2)
                        cellDict["vecX"]  = avgX/norm
                        cellDict["vecY"]  = avgY/norm
                            
            fileName='Data'+str(cellDict["ID"])+'.csv'
            try:
                fileHandle,fullFileName=self.openFileInSimulationOutputDirectory(fileName,"a")
            except IOError:
                print "Could not open file ", fileName," for writing. "
                return
        
            cellDict=self.getDictionaryAttribute(cell)
            print >>fileHandle,mcs,",",cell.xCOM,",",cell.yCOM,",",sumX,",",sumY,",",avgX,",",avgY,",",cellDict['vecX'],",",cellDict['vecY']
            fileHandle.close()
        
            #print "norm, lambdaVecXY",norm ,cellDict["vecX"],cellDict["vecX"]
            
            if cell.type == 1:
                    mu = 50
            if cell.type == 2:
                    mu = 50
                    
            #self.vectorPolarityField[cell] = [cellDict["vecX"],cellDict["vecY"],0]

             ## ForTestingOfPredefinedTrajectories
#             if(mcs%800 <200):
#                 cellDict["vecX"] = 0
#                 cellDict["vecY"] = 1
#             elif(mcs%800 <400):
#                 cellDict["vecX"] = -1
#                 cellDict["vecY"] = 0
#             elif(mcs%800 <600):
#                 cellDict["vecX"] = 0
#                 cellDict["vecY"] = -1
#             else:
#                 cellDict["vecX"] = 1
#                 cellDict["vecY"] = 0
                
            ## End ForTestingOfPredefinedTrajectories
        
            cell.lambdaVecX=mu*cellDict["vecX"] # force component along X axis
            cell.lambdaVecY=mu*cellDict["vecY"] # force component along Y axis

class MMPSecretionSteppable(SteppableBasePy):
    def __init__(self,_simulator,_frequency=1):
        SteppableBasePy.__init__(self,_simulator,_frequency)
    def start(self):
        pass
    def step(self,mcs):
#         fieldMMP=self.getConcentrationField("MMP")
        totalMMPProduced = 0
        
#         for cell in self.cellListByType(1,2):
#             pixelList=self.getCellBoundaryPixelList(cell)
#             if(pixelList):
#                 #print "TotlPixel=",pixelList.numberOfPixels()
#                 for boundaryPixelTrackerData in pixelList:
#                     x = boundaryPixelTrackerData.pixel.x;
#                     y = boundaryPixelTrackerData.pixel.y;
#                     z = boundaryPixelTrackerData.pixel.z;
#                     totalfibers = 0
#                     for i in range(-1,2):
#                         for j in range(-1,2):
#                            cell2=self.cellField[x+i,y+j,z]
#                            if cell2 and (cell2.type==3):
#                                 MMPtoProduce = 0.180*8889; # secretionRate * NoofCollagenFibrilsIn1 pixel
#                                 fieldMMP[x+i,y+j,z]+=MMPtoProduce;
#                                 totalMMPProduced = totalMMPProduced + MMPtoProduce

        totalMMPPresent = 0
        fieldMMP=self.getConcentrationField("MMP")
        for x in xrange(self.dim.x):             
            for y in xrange(self.dim.y):                 
                for z in xrange(self.dim.z): 
                    totalMMPPresent += fieldMMP[x,y,z];
                    
        fileName='MMP.csv'
        try:
            fileHandle,fullFileName=self.openFileInSimulationOutputDirectory(fileName,"a")
        except IOError:
            print "Could not open file ", fileName," for writing. "
            return
            
        print >>fileHandle,mcs,",",totalMMPProduced,",", totalMMPPresent
        fileHandle.close()
        
class ECMDegradationSteppable(SteppableBasePy):
    def __init__(self,_simulator,_frequency=1):
        SteppableBasePy.__init__(self,_simulator,_frequency)
    def start(self):
        pass
    def step(self,mcs):
	totalFibersDeleted = 0
        fieldMMP=self.getConcentrationField("MMP")
        for x,y,z in self.everyPixel():
             cell1=self.cellField[x,y,z]
             if(cell1 and cell1.type==3 and fieldMMP[x,y,z]>=1):
                        fieldMMP[x,y,z]=fieldMMP[x,y,z] - 1
                        self.deleteCell(cell1)
			totalFibersDeleted += 1
	fileName='FiberDegraded'+'.csv'
        try:
            fileHandle,fullFileName=self.openFileInSimulationOutputDirectory(fileName,"a")
        except IOError:
            print "Could not open file ", fileName," for writing. "
            return
            
        print >>fileHandle,mcs,",",totalFibersDeleted
        fileHandle.close()

       
class IdFieldVisualizationSteppable(SteppableBasePy):
    def __init__(self,_simulator,_frequency=10):
        SteppableBasePy.__init__(self,_simulator,_frequency)
        self.scalarCLField=self.createScalarFieldCellLevelPy("IdField")
    def step(self,mcs):
        self.scalarCLField.clear()
        for cell in self.cellListByType(1,2):
            self.scalarCLField[cell]=cell.id*uniform(0,1)

