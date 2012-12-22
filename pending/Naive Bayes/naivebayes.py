#Author: Krishnamurthy Koduvayur Viswanathan

from __future__ import division
import collections
import math

class Model: 
        def __init__(self, arffFile):
                self.trainingFile = arffFile
                #all feature names and their possible values (including the class label)
                self.features = {}
                #this is to maintain the order of features as in the arff
                self.ftNmList = []
                #contains tuples of the form (label, feature_name, feature_value)
                self.ftCnts = collections.defaultdict(lambda: 1)
                #contains all the values and the label as the last entry
                self.ftVcts = []
                #these will be smoothed later
                self.labelCounts = collections.defaultdict(lambda: 0)   

        def TrainClassifier(self):
                for fv in self.ftVcts:
                        self.labelCounts[fv[-1]] += 1 #update count of the label
                        for counter in range(0, len(fv)-1):
                                self.ftCnts[(fv[-1], self.ftNmList[counter], fv[counter])] += 1

                #increase label counts (smoothing). remember that
                # the last feature is actually the label
                for label in self.labelCounts:  
                        for feature in self.ftNmList[:len(self.ftNmList)-1]:
                                self.labelCounts[label] += len(self.features[feature])

        def Classify(self, ftVec):      #ftVec is a simple list like the ones that we use to train
                probabilityPerLabel = {}
                for label in self.labelCounts:
                        logProb = 0
                        for ftVal in ftVec:
                                t = (label, self.ftNmList[ftVec.index(ftVal)], ftVal)
                                logProb += math.log(self.ftCnts[t]/self.labelCounts[label])
                        f = (self.labelCounts[label]/sum(self.labelCounts.values()))
                        probabilityPerLabel[label] = f * math.exp(logProb)
                print probabilityPerLabel
                return max(probabilityPerLabel, key = lambda classLabel: probabilityPerLabel[classLabel])
                                
        def GetValues(self):
                file = open(self.trainingFile, 'r')
                for line in file:
                        if line[0] != '@':  #start of actual data
                                self.ftVcts.append(line.strip().lower().split(','))
                        else:   #feature definitions
                                c1 = line.strip().lower().find('@data') == -1
                                c2 = (not line.lower().startswith('@relation'))
                                if  c1 and c2:
                                        self.ftNmList.append(line.strip().split()[1])
                                        ind1 = line.find('{')+1
                                        ind2 =  line.find('}')
                                        fInd = self.ftNmList[len(self.ftNmList) - 1]
                                        self.features[fInd] = line[ind1:ind2].strip().split(',')
                file.close()

        def TestClassifier(self, arffFile):
                file = open(arffFile, 'r')
                for line in file:
                        if line[0] != '@':
                                vector = line.strip().lower().split(',')
                                s = "classifier: " + self.Classify(vector)
                                s += " given " + vector[len(vector) - 1]
                                print s

def main():
        model = Model("tennis.arff")
        model.GetValues()
        model.TrainClassifier()
        model.TestClassifier("tennis.arff")

if __name__ == "__main__":
        main()
