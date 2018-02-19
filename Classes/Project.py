#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  =================================================
#   - Author jouke hijlkema <jouke.hijlkema@onera.fr>
#   - ven. févr. 14:22 2018
#   - Initial Version 1.0
#  =================================================

from Classes.Task import Task
import arrow
import gantt
from collections import OrderedDict
import workdays

class Project:
    Tasks = OrderedDict()
    
    def __init__(self,items):
        "docstring"
        # for i in items:
            # print("'%s'"%i.strip())
        self.Name     = items[1].strip()
        self.Start    = self.getTime(items[6].strip(),arrow.utcnow())
        self.End      = self.getTime(items[7].strip(),self.Start)
        self.Duration = 0
        print("Project %s"%self.Name)

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
    ## Description : Add task
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 16-23-2018 14:23:24
    ## --------------------------------------------------------------
    def addTask (self,Task):
        self.Tasks[Task.Id]=Task
        if Task.Parent != "":
            Task.Parent = self.Tasks[Task.Parent]
            # print("%s set parent to %s"%(Task.Id,Task.Parent.Id))
        else:
            Task.Parent = None
        # Task.Print()

    ## --------------------------------------------------------------
    ## Description : parse the project
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 16-57-2018 14:57:24
    ## --------------------------------------------------------------
    def Parse (self):
        # print("======== Start Parsing ==========")
        # find connections
        tmax                    = self.Start
        tmin                    = self.Start
        for t in self.Tasks:
            tt                  = self.Tasks[t]
            if len(tt.Before)>0:
                tt.setBefore(self.Tasks[tt.Before])
            if len(tt.After)>0:
                # print(tt.After)
                for t in tt.After.split(","):
                    tt.setAfter(self.Tasks["%s"%t])
            if tt.Parent != None:
                tt.Parent.addChild(tt)
                
        # Update times
        for t in self.Tasks:
            tt         = self.Tasks[t]
            self.Start = min(self.Start,tt.Start)
            self.End   = max(self.End,tt.End)
        self.Duration  = workdays.networkdays(self.Start,self.End)
        self.gantt     = gantt.Project(name=self.Name)
        
        for t in self.Tasks:
            tt         = self.Tasks[t]
            self.gantt.add_task(tt.makeGanttItem())
            
            
    ## --------------------------------------------------------------
    ## Description : Print
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 16-33-2018 14:33:14
    ## --------------------------------------------------------------
    def Print (self):
        print("== Project %s =="%self.Name)
        print("| Start : %s"%self.Start)
        for t in self.Tasks:
            self.Tasks[t].Print()
        print("---------------")
        

    ## --------------------------------------------------------------
    ## Description : print the Gantt
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 16-50-2018 16:50:54
    ## --------------------------------------------------------------
    def printGantt (self):
        str = "╔ %s %s days "%(self.Name,self.Duration)
        # str+= "-"*(self.Duration-len(str))

        for i in range(len(str),self.Duration):
            if i%30==0:
                str+="╬"
            elif i%5==0:
                str+="╩"
            else:
                str+="═"
        
        print(str)
        for t in self.Tasks:
            tt = self.Tasks[t]
            tt.printGantt(self.Start)
        
    ## --------------------------------------------------------------
    ## Description : save the gantt as svg
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 16-05-2018 17:05:29
    ## --------------------------------------------------------------
    def saveGantt (self,path,scale):
        self.gantt.make_svg_for_tasks(filename=path, today=arrow.now(),scale=scale)
