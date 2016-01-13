#!/usr/bin/python
#-*- coding: utf-8 -*-
'''
Created on 20131012
@author:    zyy_max

@brief: get tokens from input file by jieba
'''
import jieba
import os, sys, re
import chardet
import time
class JiebaTokenizer:
    def __init__(self, stop_words_path, mode):
        self.stopword_dict = {}
        #load stopword_dict
        with open(stop_words_path) as ins:
            for line in ins.readlines():
                self.stopword_dict[line.strip().decode('utf8')] = 1
        self.mode = mode
    def _run(self, intext):
        intext = u' '.join(intext.split())
        if self.mode == 's':
            token_list = jieba.cut_for_search(intext)
        else:
            token_list = jieba.cut(intext)
        #print list(token_list)
        #self.tokens_list = list(token_list)
        #print self.tokens_list
        return [token for token in token_list if token.strip() != '' and not token in self.stopword_dict]
        #return list(token_list)
    def tokens(self, intext):
        #if self.token_list == []:
        return self._run(intext)

def token_single_file(inputfile, outputfile):
    result_lines = []
    outs = open(outputfile, 'w')
    begin = time.time()
    with open(inputfile) as ins:
        for lineid, line in enumerate(ins):
            oriid, _, line = line.partition('\t')
            coding = 'utf-8'
            try:
                line = line.strip().decode(coding)
            except:
                print chardet.detect(line)
                coding = chardet.detect(line)['encoding']
                try:
                    line = line.strip().decode(coding)
                except:
                    continue
            if len(line) < 20:
                continue
            tokens = jt.tokens(line)
            outs.write(oriid+'\t'+' '.join(tokens).encode('utf8')+'\n')
            print '%s finished==>avg:%ss\r' %(lineid+1, (time.time()-begin)/(lineid+1)),
    print 'Wrote to ', outputfile

if __name__=="__main__":
    if len(sys.argv) < 6 or not sys.argv[4] in ['c','s']:
        print "Usage:\ttokens.py -s/-m <inputfile/inputfolder> <outputfile/outputfolder> <mode(c/s)> <stopword.list>"
        exit(-1)
    jt = JiebaTokenizer(sys.argv[5], sys.argv[4])
    #extract tokens and filter by stopword_dict
    if(sys.argv[1] == '-s'):
        token_single_file(sys.argv[2], sys.argv[3])
    elif(sys.argv[1] == '-m'):
        for inputfile in os.listdir(sys.argv[2]):
            token_single_file(os.path.join(sys.argv[2],inputfile), os.path.join(sys.argv[3],inputfile.replace('.ori','.token')))
    
