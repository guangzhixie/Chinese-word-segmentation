from sklearn.externals import joblib
import numpy as np
import time
import codecs

# in-house libs
import string_util
import feature_extractor


class Segmentor:
    def __init__(self, classifier):
        self.su = string_util.StringUtil()
        self.featureExtractor = feature_extractor.FeatureExtractor()
        self.classifier = classifier
    
    """
    Get best tag sequence that does not contains any invalid pairs.
    """
    def get_best_tag_seq(self, feature_list):
    
        # Map of (index, tag) -> log probability
        delta = dict()
        # Backpointers, map of (index, tag) -> previous tag
        bp = dict()

        for i, feature_dict in enumerate(feature_list):
            prob_distribution = self.classifier.prob_classify(feature_dict)

            if i == 0:
                for t in self.su.TAG_SET:
                    if not t == 'm' and not t == 'e':
                        delta[(i, t)] = prob_distribution.logprob(t)

            else:
                for t in self.su.TAG_SET:
                    max_term = max([(prob_distribution.logprob(t) + delta[(i - 1, t_1)], t_1)
                                        if not t_1 + t in self.su.INVALID_TAG_SEQ and (i - 1, t_1) in delta else (-np.inf, t_1)
                                            for t_1 in self.su.TAG_SET])

                    delta[(i, t)] = max_term[0]
                    bp[(i, t)] = max_term[1]

        n = len(feature_list)
        end_score, end_tag = max([(delta[(n-1, t)], t) if (n-1, t) in delta else (-np.inf, t) for t in self.su.TAG_SET])

        # Follow backpointers to obtain sequence with the highest score.
        tags = [end_tag]
        for i in reversed(range(0, n-1)):
            tags.append(bp[(i + 1, tags[-1])])
        return list(reversed(tags))
    
    
    def get_tags_for_sentence(self, sentence):
        feature_list = self.featureExtractor.extract_feature_for_sentence(sentence)
        return self.get_best_tag_seq(feature_list)
    
    
    """
    Combine consecutive segments containing only English letters or digits into one segment.
    """
    def post_processing(self, sentence):
        segments = sentence.split()
        temp = []

        # Post processing for digits & English letters
        i = 0
        while i < len(segments):
            word = segments[i]
            if self.su.is_digit_or_letter(word):
                while i+1 < len(segments):
                    if self.su.is_digit_or_letter(segments[i+1]):
                        word = word + segments[i+1]
                        i += 1
                    else:
                        break
            
            temp.append(word)
            i += 1

        # Post processing for decimal points
        results = []
        i = 0
        while i < len(temp):
            word = temp[i]
            if word == "." and i > 0 and i+1 < len(temp) and self.su.is_digit_or_letter(results[-1]) \
                    and self.su.is_digit_or_letter(temp[i+1]):
                results[-1] = results[-1] + word + temp[i+1]
                i += 1
            else:
                results.append(word)
            i += 1
            
        return self.su.SPACE.join(results)
    
    
    """
    Do segmentation for a part of sentence that does not contain white space
    """
    def do_segmentation_for_partial_sentence(self, sentence):
        tags = self.get_tags_for_sentence(sentence)

        output = []
        total_len = len(tags)

        for i, t in enumerate(tags):
            output.append(sentence[i])
            if i < total_len -1:
                if t == 's' or t == 'e':
                    output.append(self.su.SPACE)

        return self.post_processing(self.su.EMPTY.join(output))
    
    
    
    """
    Main function to do segmentation
    """
    def do_segmentation_for_sentence(self, sentence):
        sentence = sentence.strip().decode("utf-8")
        segments = sentence.split()

        return self.su.SPACE.join([self.do_segmentation_for_partial_sentence(s) for s in segments])
    
    
    """
    Read sentences from a file and output segmentation results to another file
    """
    def do_segmentation_for_file(self, source_path, output_path):
        start = time.time()
        with codecs.getwriter("utf-8")(open(output_path, "w+")) as output_file:
            for line in open(source_path, "r").readlines():
                output_file.write("%s\n" % self.do_segmentation_for_sentence(line.strip()))
    
        print 'Done. Total time taken %d seconds' % (time.time() - start)
