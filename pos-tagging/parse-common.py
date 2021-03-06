 #!/usr/bin/python
 # -*- coding: utf-8 -*-
 
from treetagger import TreeTagger
import argparse
import re

def convertTags(filename):
  posConvert = open("../universal-tags/"+filename,"r")
  tagDict = {}
  for line in posConvert:
    oldTag, newTag = line.split("\t")
    tagDict[oldTag] = newTag.strip()
  return tagDict

def tagWrite(line, tagDict, tagger, langCode, output, errors):
  tags = tagger.tag(line)
  splitLine = line.split()
  output.write("\t".join(splitLine)+"\n")
  for wordTags in tags:
    for tag in wordTags[1:]:
      #print tag
      oldTag = tag.split()[0]
      prob = tag.split()[-1]
      try:
        universalTag = tagDict[oldTag]
      except KeyError:
        errors.write(oldTag+" not found in "+langCode+"tag dictionary.\n")
        universalTag = oldTag
        #universalTag = raw_input("Enter the universal tag for "+oldTag+"in "+langCode+": ")
        #tagDict[oldTag] = universalTag
      output.write(universalTag+ " " + prob + " ")
    output.write("\t")
  output.write("\n")

def tagLang(langs, corpus):
  if "fr" in langs:
    frTagDict = convertTags('fr-treetagger.map')
    frTagger = TreeTagger(encoding='utf-8',language='french')
  if "sl" in langs:
    slTagDict = convertTags('sl-treetagger.map')
    slTagger = TreeTagger(encoding='utf-8',language='slovenian')
  if "de" in langs:
    deTagDict = convertTags('de-tiger.map')
    deTagger = TreeTagger(encoding='utf-8',language='german')
  if "it" in langs:
    itTagDict = convertTags('it-treetagger.map')
    itTagger = TreeTagger(encoding='utf-8',language='italian')
  if "pl" in langs:
    plTagDict = convertTags('pl-treetagger.map')
    plTagger = TreeTagger(encoding='utf-8',language='polish')
  if "sk" in langs:
    skTagDict = convertTags('sk-treetagger.map')
    skTagger = TreeTagger(encoding='utf-8',language='slovak')
  if "es" in langs:
    esTagDict = convertTags('es-treetagger.map')
    esTagger = TreeTagger(encoding='utf-8',language='spanish')
  if "nl" in langs:
    nlTagDict = convertTags('nl-treetagger.map')
    nlTagger = TreeTagger(encoding='utf-8',language='dutch')
  engTagger = TreeTagger(encoding='utf-8',language='english')
  engTagDict = convertTags('en-ptb.map')
  corpus = open(corpus, 'r')
  output = open('tagged.all','w')
  errors = open('errors.txt','w')
  numLines = 0

  for line in corpus:
    #numLines += 1
    #print numLines
    if line.startswith("<fr>"):
      splitline = line.split(" ")
      notag = " ".join(splitline[1:])
      tagWrite(notag, frTagDict, frTagger,"fr", output, errors)
    elif line.startswith("<sl>"):
      splitline = line.split(" ")
      notag = " ".join(splitline[1:])
      tagWrite(notag, slTagDict, slTagger,"sl", output, errors)
    elif line.startswith("<de>"):
      splitline = line.split(" ")
      notag = " ".join(splitline[1:])
      tagWrite(notag, deTagDict, deTagger,"de", output, errors)
    elif line.startswith("<it>"):
      splitline = line.split(" ")
      notag = " ".join(splitline[1:])
      tagWrite(notag, itTagDict, itTagger,"it", output, errors)
    elif line.startswith("<pl>"):
      splitline = line.split(" ")
      notag = " ".join(splitline[1:])
      tagWrite(notag, plTagDict, plTagger,"pl", output, errors)
    elif line.startswith("<sk>"):
      splitline = line.split(" ")
      notag = " ".join(splitline[1:])
      tagWrite(notag, skTagDict, skTagger,"sk", output, errors)
    elif line.startswith("<es>"):
      splitline = line.split(" ")
      notag = " ".join(splitline[1:])
      tagWrite(notag, esTagDict, esTagger,"es", output, errors)
    elif line.startswith("<nl>"):
      splitline = line.split(" ")
      notag = " ".join(splitline[1:])
      tagWrite(notag, nlTagDict, nlTagger,"nl", output, errors)
    elif line.startswith("-1") or line[0].isdigit():
      splitline = line.split(",")
      output.write("\t".join(splitline))
    elif line.startswith("!@#$%^&*()"):
      output.write(line)
    else:
      tagWrite(line,engTagDict,engTagger,"en", output, errors)

def main():
  parser = argparse.ArgumentParser()
  parser.usage = "python treetagger-test.py -i common.txt"
  #parser.add_argument("-l", "--langs", dest="langs", action="store", nargs='+', help="Language codes for languages to tag")
  parser.add_argument("-i", "--infile", dest="corpus", action="store", help="File to tag")
  opts = parser.parse_args()
  langs = ["fr","sl","de","it","pl","sk","es","nl"]
  tagLang(langs, opts.corpus)
main()