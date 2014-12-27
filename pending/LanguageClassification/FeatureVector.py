from FeatureMap import FeatureMap

class FeatureVector:
    _featuremap = FeatureMap()

    def __init__(self):
        self.feats = set()
        self.label = None

    def add(self, feat):
        if feat not in self._featuremap:
            ind = self._featuremap.add(feat)
        else:
            ind = self._featuremap.getInd(feat)

        if ind < 0:
            print str(ind) + " ERROR!!! ind shouldn't be 0 or -1"
            
        if ind not in self.feats:
            self.feats.add(ind)

    def printVector(self):
        print self.label, 
        for f in sorted(list(self.feats)):
            print str(f) + ":1 ",
        print

    def getFeatDict(self):
        d = {}
        for f in self.feats:
            d[f] = 1
        return d

    def getLabel(self):
        return self.label
    
    def setLabel(self, label):
        self.label = self._featuremap.getLabelInd(label)
        
    def __str__(self):
        return self.label + str(self.feats)
        

if __name__ == "__main__":
    feats1 = ["th", "ww", "ah", "re"]
    feats2 = ["aa", "ah", "wer", "arr"]
    feats3 = ["we", "shsh", "wer", "whwhw"]

    fv1 = FeatureVector()
    for f in feats1:
        fv1.add(f)
    fv1.setLabel("spanish")

    fv2 = FeatureVector()
    for f in feats2:
        fv2.add(f)
    fv2.setLabel("english")

    fv3 = FeatureVector()
    for f in feats3:
        fv3.add(f)
    fv3.setLabel("spanish")
    
    print FeatureVector._featuremap
 
    fv1.printVector()
    fv2.printVector()
    fv3.printVector()
    
