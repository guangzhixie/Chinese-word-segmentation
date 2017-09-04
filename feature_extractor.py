import time
# in-house libs
import string_util

def load_dict(dict_path):
    ref_dict = dict()
    for line in open(dict_path, 'r').readlines():
        word = line.strip().decode('utf-8')
        ref_dict[word] = len(word)
        
    return ref_dict

class FeatureExtractor(object):
    def __init__(self):
        self.su = string_util.StringUtil()
        self.ref_dict = load_dict("data/dict/processed.utf8")
        
    def extract_dict_feature(self, sentence, curr_i, window_size=10):
        start_index = curr_i - (window_size - 1)
        if start_index < 0:
            start_index = 0

        end_index = curr_i + window_size
        if end_index > len(sentence):
            end_index = len(sentence)

        t0 = 's'
        L = 0

        for i in range(start_index, curr_i+1):
            for j in range(curr_i+1, end_index+1):
                if sentence[i:j] in self.ref_dict and j-i > L:
                    L = j - i

                    if j-i == 1:
                        t0 = 's'
                    if i == curr_i:
                        t0 = 'b'
                    elif j-1 == curr_i:
                        t0 = 'e'
                    else:
                        t0 = 'm'

        return (L, t0)
    
    def extract_feature_for_sentence(self, sentence, window_size=5):
        if window_size % 2 == 0 or not window_size > 1:
            raise ValueError('Window size must be odd number and larger than 1')

        sentence = self.su.remove_whitespace(sentence)
        total_len = len(sentence)
        context_size = window_size / 2

        feature_dict_list = []

        for i, c in enumerate(sentence):
            feature_dict = dict()

            c_features = dict()
            c_features["c0"] = c

            t_features = dict()
            t_features["t0"] = self.su.get_character_type(c)

            for context_i in range(1, context_size+1):
                c_features["c_"+str(context_i)] = sentence[i-context_i] if i-context_i >=0 \
                                                    else self.su.SENTENCE_START.decode("utf-8")
                c_features["c"+str(context_i)] = sentence[i+context_i] if i+context_i < total_len \
                                                    else self.su.SENTENCE_END.decode("utf-8")

                t_features["t_"+str(context_i)] = self.su.get_character_type(c_features["c_"+str(context_i)])
                t_features["t"+str(context_i)] = self.su.get_character_type(c_features["c"+str(context_i)])

            # feature a
            feature_dict.update(c_features)

            # feature b
            for context_i in reversed(range(1, context_size+1)):
                if context_i-1 == 0:
                    feature_dict["c_"+str(context_i)+"c0"] = \
                        c_features["c_"+str(context_i)] + c_features["c0"]

                    feature_dict["c0"+"c"+str(context_i)] = \
                        c_features["c0"] + c_features["c"+str(context_i)]    

                else:
                    feature_dict["c_"+str(context_i)+"c_"+str(context_i-1)] = \
                        c_features["c_"+str(context_i)] + c_features["c_"+str(context_i-1)]

                    feature_dict["c"+str(context_i-1)+"c"+str(context_i)] = \
                        c_features["c_"+str(context_i-1)] + c_features["c_"+str(context_i)]

            # feature c
            feature_dict["c_1c1"] = c_features["c_1"] + c_features["c1"]

            # feature d
            feature_dict["p"] = "1" if self.su.is_punctuation(c) else "0"

            # feature e
            type_feature = reduce(lambda x,y: x+y, t_features.itervalues())
            feature_dict["t"] = type_feature

            matched = self.extract_dict_feature(sentence, i)

            # feature f
            feature_dict["Lt0"] = str(matched[0]) + matched[1]

            # feature g
            feature_dict["c_1t0"] = c_features["c_1"] + matched[1]
            feature_dict["c0t0"] = c_features["c0"] + matched[1]
            feature_dict["c1t0"] = c_features["c1"] + matched[1]

            feature_dict_list.append(feature_dict)

        return feature_dict_list
    
    def extract_feature_for_file(self, input_path, output_path, window_size=5):
        print 'Extracting features (v2) for %s and output to %s...' % (input_path, output_path)
        start = time.time()

        with open(output_path, "w+") as output_file:
            for line in open(input_path, "r").readlines():
                line = line.strip().decode("utf-8")
                feature_dict_list = self.extract_feature_for_sentence(line, window_size)
                for feature_dict in feature_dict_list:
                    output_file.writelines(self.su.to_json(feature_dict) + self.su.NEWLINE)

        print 'Done. Total time taken %d seconds' % (time.time() - start)
        