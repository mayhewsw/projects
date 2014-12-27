

class FeatureMap:
    def __init__(self):
        self.feat_ind = {}
        self.ind_feat = {}
        self.currInd = 1

        self.label_ind = {}
        self.currLabInd = 1
        
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

    def getLabelName(self, ind):
        for k,v in self.label_ind.iteritems():
            if v == ind:
                return k
        return "Class " + str(ind)

    def writeLexicon(self, fname):
        with open(fname, 'w') as f:
            f.write("@Languages\n")
            for k in self.label_ind:
                #f.write(k.encode('utf-8') + " ")
                f.write(k + " ")
                f.write(str(self.label_ind[k]) + "\n")

            f.write("\n")
            f.write("@Features\n")
            for k in self.feat_ind:
                #f.write(k.encode('utf-8') + " ")
                f.write(k + " ")
                f.write(str(self.feat_ind[k]) + "\n")

                
    def readLexicon(self, fname):
        self.feat_ind = {}
        self.ind_feat = {}
        self.label_ind = {}
        self.currInd = 1

        langmode = False
        featmode = False
        with open(fname, 'r') as f:

            for line in f:
                if "@Languages" in line:
                    langmode = True
                    continue
                if len(line.strip()) == 0:
                    langmode = False
                    continue
                if "@Features" in line:
                    featmode = True
                    continue

                if langmode:
                    print line.strip()
                    lang, ind = line.strip().split()
                    ind = int(ind)
                    self.label_ind[lang] = ind

                if featmode:
                    feat, ind = line.strip().split()
                    ind = int(ind)
                    self.feat_ind[feat] = ind
                    self.ind_feat[ind] = feat
                    
            self.currInd = len(self.feat_ind)
                
                
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
    
