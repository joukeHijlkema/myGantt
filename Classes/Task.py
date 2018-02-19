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
import gantt

class Task:
    def __init__(self,items,start):
        "docstring"
        # for i in items:
            # print("'%s'"%i.strip())
        self.Kids        = []
        self.Id          = items[0].strip()
        self.Description = items[1].strip()
        self.Parent      = items[2].strip()
        self.Duration    = self.calcDuration(items[3].strip())
        self.Before      = items[4].strip()
        self.After       = items[5].strip()
        self.Start       = self.getTime(items[6].strip(),start)
        self.End         = self.getTime(items[7].strip(),arrow.get(workdays.workday(self.Start,self.Duration-1)))
        # self.Start       = items[6].strip()
        self.Type        = items[8].strip()
        # if len(self.Start) == 0:
        #     self.Start   = start
        # else:
        #     self.Start   = arrow.get(self.Start,"D/M/YYYY")
        self.End         = arrow.get(workdays.workday(self.Start,self.Duration-1))
        self.gItem       = None
        self.Depends     = []

    ## --------------------------------------------------------------
    ## Description : get the time from an emcas string
    ## NOTE : return bup if not working
    ## -
    ## Author : jouke hylkema
    ## date   : 19-53-2018 15:53:11
    ## --------------------------------------------------------------
    def getTime (self,str,bup):
        try:
            out = arrow.get(str[1:11],"YYYY-MM-DD")
            # print(out)
        except:
            out = bup
        return out
        

    ## --------------------------------------------------------------
    ## Description : set before
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 16-22-2018 16:22:28
    ## --------------------------------------------------------------
    def setBefore (self,t):
        self.End    = arrow.get(workdays.workday(t.Start,-1))
        self.Start  = arrow.get(workdays.workday(self.End, -(self.Duration)))
        self.Before = t
        
    ## --------------------------------------------------------------
    ## Description : set before
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 16-22-2018 16:22:28
    ## --------------------------------------------------------------
    def setAfter (self,t):
        # print("%s after %s (%s)"%(self.Id,t.Id,t.End))
        if self.Start<t.End:
            self.Start = arrow.get(workdays.workday(t.End,+1))
        self.End   = arrow.get(workdays.workday(self.Start,self.Duration-1))
        self.Depends.append(t)
        
    ## --------------------------------------------------------------
    ## Description : ad a child
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 16-53-2018 14:53:51
    ## --------------------------------------------------------------
    def addChild (self,Task):
        # print("%s : parent = %s"%(Task.Id, self.Id))
        self.Kids.append(Task)
        if Task.Start < self.Start:
            Task.shiftTime(self.Start)
        if self.End < Task.End:
            self.End = Task.End
        self.checkTimes()

    ## --------------------------------------------------------------
    ## Description : shift in time
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 16-10-2018 21:10:11
    ## --------------------------------------------------------------
    def shiftTime (self,Start):
        self.Start   = Start
        self.End     = arrow.get(workdays.workday(self.Start,self.Duration-1))
        
    ## --------------------------------------------------------------
    ## Description : Calculate the duration
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 16-36-2018 14:36:51
    ## --------------------------------------------------------------
    def calcDuration (self,d):
        m            = re.search('(^\d+)([dwmy])',d)
        coef         = 0
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
        if len(self.Kids) > 0:
            sign = "╠"
        else:
            sign = "╚"
        if self.Type =="KP":
            sign+="█"
        else:
            sign+="═"
        o        = workdays.networkdays(start,self.Start)-1
        txt      = "%s%s "%(sign,self.Description)
        s        = self.Duration-len(txt)
        if s > 0:
            txt+= "-"*s
        str = " "*o+txt
        print(str)
        
    ## --------------------------------------------------------------
    ## Description : gItem
    ## NOTE : return a gantt item
    ## -
    ## Author : jouke hylkema
    ## date   : 16-47-2018 21:47:53
    ## --------------------------------------------------------------
    def makeGanttItem (self):
        # print("gItem %s"%self.Id)
        dd = []
        for d in self.Depends:
            dd.append(d.gItem)
        # print(dd)
        if self.Parent !=None:
            color="#807ACE"
        else :
            color="#92A094"
        if self.Type=="KP":
            self.gItem = gantt.Milestone(name=self.Id,
                                         fullname=self.Description,
                                         start=self.Start,
                                         depends_of=dd)
        else:
            self.gItem = gantt.Task(name=self.Id,
                                    fullname=self.Description,
                                    start=self.Start,
                                    stop=self.End,
                                    depends_of=dd,
                                    color=color)
        return self.gItem
