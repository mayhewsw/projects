

class FeatureMap:
    def __init__(self):
        self.feat_ind = {}
        self.ind_feat = {}
        self.currInd = 0

        self.label_ind = {}
        self.currLabInd = 0
        
    def add(self, feat):
        ''' To add a feature, you simply add the value.
        This will add binary features. '''
        if feat not in self.feat_ind:
            self.feat_ind[feat] = self.currInd
            self.ind_feat[self.currInd] = feat
            self.currInd += 1
        return self.feat_ind[feat]

    def getInd(self, feat):
        return self.feat_ind[feat]

    def getLabelInd(self, label):
        if label not in self.label_ind:
            self.label_ind[label] = self.currLabInd
            self.currLabInd += 1
        return self.label_ind[label]
    
    def __str__(self):
        return str(self.feat_ind)

    def __contains__(self, featname):
        return featname in self.feat_ind

    


if __name__ == "__main__":
    fm = FeatureMap()
    fm.add("th")
    fm.add("rr")
    fm.add("24")

    print fm
    
