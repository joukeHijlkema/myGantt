#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  =================================================
#   - Author jouke hijlkema <jouke.hijlkema@onera.fr>
#   - ven. févr. 11:27 2018
#   - Initial Version 1.0
#  =================================================
from Classes.Task import Task
from Classes.Project import Project
import re, sys

fid = open(sys.argv[1],"r")
Tasks=[]
for l in fid:
    items = l.split("\t")
    if items[0] == "Id":
        pass
    elif items[0] == "P":
        Proj = Project(items)
    else:
        Proj.addTask(Task(items,Proj.Start))

Proj.Parse()
# Proj.Print()
Proj.printGantt()
Proj.saveGantt(sys.argv[2],sys.argv[3])
