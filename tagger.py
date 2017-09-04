import time
# in-house libs
import string_util


class Tagger(object):
    def __init__(self):
        self.su = string_util.StringUtil()
        
    def tag_for_sentence(sentence):
        words = sentence.decode('utf-8').strip().split()
        tags = []
        for word in words:
            if len(word) > 1:
                tags.append('b')
                for char in word[1:(len(word) - 1)]:
                    tags.append('m')
                tags.append('e')
            else: 
                tags.append('s')

        return tags
    
    def tag_for_file(self, input_path, output_path):
        print 'Tagging for %s and output to %s...' % (input_path, output_path)
        start = time.time()

        with open(output_path, "w+") as output_file:
            for line in open(input_path, "r").readlines():
                line = line.strip().decode("utf-8")
                tags = self.tag_for_sentence(line)
                for tag in tags:
                    output_file.writelines(tag + self.su.NEWLINE)

        print 'Done. Total time taken %d seconds' % (time.time() - start)