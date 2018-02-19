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

Head = fid.readline().split("\t")
Proj = Project(fid.readline().split("\t"))
for l in fid:
    items = l.split("\t")
    Proj.addTask(Task(items,Proj.Start))

Proj.Parse()
# Proj.Print()
Proj.printGantt()
Proj.saveGantt(sys.argv[2],sys.argv[3])
