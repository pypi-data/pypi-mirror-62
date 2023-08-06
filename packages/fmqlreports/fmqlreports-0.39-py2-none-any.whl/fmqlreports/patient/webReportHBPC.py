#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, Counter
from datetime import datetime

from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent
from fmqlutils.typer.reduceTypeUtils import splitTypeDatas, checkDataPresent
from ..webReportUtils import SITE_DIR_TEMPL, loadSelectTypes, reduce200, mdFilesOfDomain

"""
HBPC ... follow Dental, Health Factors

Requires:
- SELECT TYPEs for File Types

https://www.va.gov/vdl/documents/Clinical/Home_Based_Pri_Care_(HBPC)/hbh1_tm.pdf

"""
def webReportHBPC(stationNo):

    allThere, details = checkDataPresent(stationNo, [
    ])
    if not allThere:
        raise Exception("Some required data is missing - {}".format(details))

    mu = """---
layout: default
title: {} HBPC
---

## HBPC Package

""".format(stationNo) 
    
    usedFiles = ["HBHC PATIENT", "HBHC PROVIDER", "HBHC VISIT"]
    mu += mdFilesOfDomain(
        stationNo, 
        "HBPC", 
        631, 
        640,
        usedFiles
    )
    
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    open(userSiteDir + "hbpc.md", "w").write(mu)
        
# ################################# DRIVER #######################
               
def main():

    assert(sys.version_info >= (2,7))
    
    if len(sys.argv) < 2:
        print "need to specify station # ex/ 442 - exiting"
        return
        
    stationNo = sys.argv[1]
    
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    if not os.path.isdir(userSiteDir):
        raise Exception("Expect User Site to already exist with its basic contents")
    
    webReportHBPC(stationNo)
    
if __name__ == "__main__":
    main()
