#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  =================================================
#   - Author jouke hijlkema <jouke.hijlkema@onera.fr>
#   - ven. févr. 14:09 2018
#   - Initial Version 1.0
#  =================================================

import re
import arrow
import workdays

class Task:
    def __init__(self,items,start):
        "docstring"
        # for i in items:
        #     print("'%s'"%i.strip())
        self.Kids        = []
        self.Id          = items[0].strip()
        self.Description = items[1].strip()
        self.Parent      = items[2].strip()
        self.Duration    = self.calcDuration(items[3].strip())
        self.Before      = items[4].strip()
        self.After       = items[5].strip()
        self.Start       = items[6].strip()
        if len(self.Start) ==0:
            self.Start=start
        self.End = arrow.get(workdays.workday(self.Start,self.Duration-1))
            

    ## --------------------------------------------------------------
    ## Description : set before
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 16-22-2018 16:22:28
    ## --------------------------------------------------------------
    def setBefore (self,t):
        self.End   = arrow.get(workdays.workday(t.Start,-1))
        self.Start = arrow.get(workdays.workday(self.End, -(self.Duration)))
        
    ## --------------------------------------------------------------
    ## Description : set before
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 16-22-2018 16:22:28
    ## --------------------------------------------------------------
    def setAfter (self,t):
        self.Start = arrow.get(workdays.workday(t.End,+1))
        self.End   = arrow.get(workdays.workday(self.Start,self.Duration-1))

    ## --------------------------------------------------------------
    ## Description : ad a child
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 16-53-2018 14:53:51
    ## --------------------------------------------------------------
    def addChild (self,Task):
        self.Kids.append(Task)

    ## --------------------------------------------------------------
    ## Description : Calculate the duration
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 16-36-2018 14:36:51
    ## --------------------------------------------------------------
    def calcDuration (self,d):
        m = re.search('(^\d+)([dwmy])',d)
        coef = 0
        if m:
            if m.group(2) == "d":
                coef = 1
            elif m.group(2) == "w":
                coef = 5
            elif m.group(2) == "m":
                coef = 22
            elif m.group(2) == "y":
                coef = 260
            return coef*int(m.group(1))
        return 1

    ## --------------------------------------------------------------
    ## Description : check the times
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 16-16-2018 17:16:14
    ## --------------------------------------------------------------
    def checkTimes (self):
        self.Duration = workdays.networkdays(self.Start,self.End)
        
    ## --------------------------------------------------------------
    ## Description : print
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 16-30-2018 14:30:35
    ## --------------------------------------------------------------
    def Print (self):
        print("== Task %s =="%self.Id)
        print("| Description : '%s'"%self.Description)
        print("| Duration    : '%s'"%self.Duration)
        print("| Before      : '%s'"%self.Before)
        print("| After       : '%s'"%self.After)
        print("| Start       : '%s'"%self.Start)
        print("| End         : '%s'"%self.End)
        for k in self.Kids:
            print("|-- %s"%k.Id)
        print("---------------")


    ## --------------------------------------------------------------
    ## Description : print gantt element
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 16-44-2018 16:44:58
    ## --------------------------------------------------------------
    def printGantt (self,start):
        s = workdays.networkdays(start,self.Start)-1
        # print(s)
        str = ""
        str+= " "*s
        str+= "|%s"%self.Description
        s = self.Duration-len(self.Description)
        # print("duration %s, len %s -> %s"%( self.Duration,len(self.Description),s))
        if s > 0:
            str+= "-"*s
        print(str)
        
