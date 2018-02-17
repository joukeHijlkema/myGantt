# myGantt

This is an attempt tu use the very nice python-gantt library in combination with emacs org-mode.

## Dependencies
You'll need python-gantt and arrow for the python executable
`sudo -H pip3 install python-gantt arrow`
On the emacs side you'd like to install org-mode

## Usage

in your emacs org file you need a block like
```lisp
* A fancy project
#+name: planning
|-------+------------------------------------+--------+----------+--------+-------+----------+------|
|    Id | Description                        | Parent | Duration | Before | After | Start    | Type |
|-------+------------------------------------+--------+----------+--------+-------+----------+------|
|     P | Fancy project name                 |        |          |        |       | 1/1/2018 |      |
|    L1 | Make a great gantt interface       |        |          |        |       |          |      |
|   1.1 | Write the python code              | L1     | 2w       |        |       |          |      |
|   1.2 | Write the lisp code                | L1     | 2w       |        |   1.1 |          |      |
|   1.3 | Tests                              | L1     | 1w       |        |   1.2 |          |      |
|    L2 | Write a readme                     |        |          |        |    L1 |          |      |
|   2.1 | Write the intro                    | L2     | 4w       |        |       |          |      |
|   2.2 | Do the details                     | L2     | 1w       |        |   2.1 |          |      |
|   2.3 | Keypoint to decide what to do next | L2     |          |        |   2.2 |          | KP   |
|    L3 | Take a break                       |        |          |        |    L2 |          |      |
|   3.1 | Sleep                              | L3     | 2d       |        |       |          |      |
|   3.2 | Read books                         | L3     | 2w       |        |   3.1 |          |      |
| 3.3.1 | Go on a trip                       | L3     | 1m       |        |   3.2 |          |      |
| 3.3.2 | Or do something else               | L3     | 1m       |        |   3.2 |          |      |
|   3.4 | Decide what to do next             | L3     |          |        | 3.3.2 |          | KP   |
#+begin_src sh :var tasks=planning tmpFile="/tmp/myGantt.txt" svgFile="./Images/Test.svg" scale="w" :results value code
   echo "$tasks" > /tmp/myGantt.txt; ~/Projects/myGantt/myGantt.py "$tmpFile" "$svgFile" "$scale"
#+end_src
```
Then if you execute the dynamic block (C-c C-c while somewhere between #+begin_src and #+end_src) then you'll get :
```lisp
#+RESULTS:
#+BEGIN_SRC sh
╔ Fancy project name 85 days ═╬════╩════╩════╩════╩════╩════╬════╩════╩════╩════╩════
╠Make a great gantt interface 
╚Write the python code 
          ╚Write the lisp code 
                    ╚Tests 
                         ╠Write a readme ----------
                         ╚Write the intro ---
                                             ╚Do the details 
                                                  ╚Keypoint to decide what to do next 
                                                   ╠Take a break --------------------
                                                   ╚Sleep 
                                                     ╚Read books 
                                                               ╚Go on a trip --------
                                                               ╚Or do something else 
                                                                                     ╚Decide what to do next 
#+END_SRC
```
and a nice svg file [gantt.svg](file://Tests/Images/Test.svg)

