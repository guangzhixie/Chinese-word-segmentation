# util libs
import time
from itertools import izip

# model libs
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
from nltk.classify.scikitlearn import SklearnClassifier

# in-house libs
import string_util

class MaxEntModel(object):
    def __init__(self):
        self.su = string_util.StringUtil()
        
    def train(self, feature_path, tag_path, model_path):
        print 'Loading training data..'
        train_data = []
        with open(feature_path, 'r') as feature_file, open(tag_path, 'r') as tag_file:
            for feature_line, tag_line in izip(feature_file, tag_file):
                feature_json = feature_line.strip()
                tag = tag_line.strip()
                #print("{0}\t{1}".format(feature_json, tag))

                feature_dict = self.su.from_json(feature_json)
                train_data.append((feature_dict, tag))
        print 'Done'

        model = SklearnClassifier(LogisticRegression())
        print "Start to train the model..."
        start = time.time()

        classifier = model.train(train_data)

        print('Done. Total time taken {0} seconds'.format(time.time() - start))

        # save the model to a file
        joblib.dump(classifier, model_path, compress=0)