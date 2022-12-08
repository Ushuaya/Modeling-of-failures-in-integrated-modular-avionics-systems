#!/usr/bin/env python




##################################################
## DEPENDENCIES
import sys
import os
import os.path
try:
    import builtins as builtin
except ImportError:
    import __builtin__ as builtin
from os.path import getmtime, exists
import time
import types
from Cheetah.Version import MinCompatibleVersion as RequiredCheetahVersion
from Cheetah.Version import MinCompatibleVersionTuple as RequiredCheetahVersionTuple
from Cheetah.Template import Template
from Cheetah.DummyTransaction import *
from Cheetah.NameMapper import NotFound, valueForName, valueFromSearchList, valueFromFrameOrSearchList
from Cheetah.CacheRegion import CacheRegion
import Cheetah.Filters as Filters
import Cheetah.ErrorCatchers as ErrorCatchers
from Cheetah.compat import unicode

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '3.1.0'
__CHEETAH_versionTuple__ = (3, 1, 0, 'final', 1)
__CHEETAH_genTime__ = 1586513964.967573
__CHEETAH_genTimestamp__ = 'Fri Apr 10 13:19:24 2020'
__CHEETAH_src__ = 'automaton_h.tmpl'
__CHEETAH_srcLastModified__ = 'Fri Apr 10 11:57:32 2020'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class automaton_h(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(automaton_h, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def respond(self, trans=None):



        ## CHEETAH: main method generated for this template
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write(u'''#ifndef __''')
        _v = VFN(VFFSL(SL,"automaton.name",True),"upper",False)() # u'${automaton.name.upper()}' on line 1, col 12
        if _v is not None: write(_filter(_v, rawExpr=u'${automaton.name.upper()}')) # from line 1, col 12.
        write(u'''__H_
#define __''')
        _v = VFN(VFFSL(SL,"automaton.name",True),"upper",False)() # u'${automaton.name.upper()}' on line 2, col 12
        if _v is not None: write(_filter(_v, rawExpr=u'${automaton.name.upper()}')) # from line 2, col 12.
        write(u'''__H_

#include "automaton.h"
#include "common.h"

namespace ''')
        _v = VFFSL(SL,"automaton.name",True) # u'$automaton.name' on line 7, col 11
        if _v is not None: write(_filter(_v, rawExpr=u'$automaton.name')) # from line 7, col 11.
        write(u''' {

class ''')
        _v = VFFSL(SL,"automaton.name",True) # u'$automaton.name' on line 9, col 7
        if _v is not None: write(_filter(_v, rawExpr=u'$automaton.name')) # from line 9, col 7.
        write(u''':public Automaton {
\t''')
        _v = VFFSL(SL,"automaton.name",True) # u'$automaton.name' on line 10, col 2
        if _v is not None: write(_filter(_v, rawExpr=u'$automaton.name')) # from line 10, col 2.
        write(u''' *automaton;
public:
''')
        for p in VFFSL(SL,"automaton.typedParams",True): # generated from line 12, col 1
            write(u'''\t''')
            _v = VFFSL(SL,"p",True)[1] # u'${p[1]}' on line 13, col 2
            if _v is not None: write(_filter(_v, rawExpr=u'${p[1]}')) # from line 13, col 2.
            write(u'''* ''')
            _v = VFFSL(SL,"p",True)[0] # u'${p[0]}' on line 13, col 11
            if _v is not None: write(_filter(_v, rawExpr=u'${p[0]}')) # from line 13, col 11.
            write(u''';
''')
        for p in VFFSL(SL,"automaton.arrayTypedParams",True): # generated from line 15, col 1
            write(u'''\tstd::vector <''')
            _v = VFFSL(SL,"p",True)[1] # u'${p[1]}' on line 16, col 15
            if _v is not None: write(_filter(_v, rawExpr=u'${p[1]}')) # from line 16, col 15.
            write(u'''*> &''')
            _v = VFFSL(SL,"p",True)[0] # u'${p[0]}' on line 16, col 26
            if _v is not None: write(_filter(_v, rawExpr=u'${p[0]}')) # from line 16, col 26.
            write(u''';
''')
        write(u'''
''')
        for p in VFFSL(SL,"automaton.vars",True): # generated from line 19, col 1
            write(u'''\tVar* ''')
            _v = VFFSL(SL,"p",True) # u'$p' on line 20, col 7
            if _v is not None: write(_filter(_v, rawExpr=u'$p')) # from line 20, col 7.
            write(u''';
''')
        write(u'''
''')
        for p in VFFSL(SL,"automaton.arrayVars",True): # generated from line 23, col 1
            write(u'''\tstd::vector <Var*> &''')
            _v = VFFSL(SL,"p",True) # u'$p' on line 24, col 22
            if _v is not None: write(_filter(_v, rawExpr=u'$p')) # from line 24, col 22.
            write(u''';
''')
        write(u'''
''')
        for p in VFFSL(SL,"automaton.arrayArrayVars",True): # generated from line 27, col 1
            write(u'''\tstd::vector <std::vector <Var*> > &''')
            _v = VFFSL(SL,"p",True) # u'$p' on line 28, col 37
            if _v is not None: write(_filter(_v, rawExpr=u'$p')) # from line 28, col 37.
            write(u''';
''')
        write(u'''
''')
        for p in VFFSL(SL,"automaton.chans",True): # generated from line 31, col 1
            write(u'''\tChannel* ''')
            _v = VFFSL(SL,"p",True) # u'$p' on line 32, col 11
            if _v is not None: write(_filter(_v, rawExpr=u'$p')) # from line 32, col 11.
            write(u''';
''')
        write(u'''
''')
        for p in VFFSL(SL,"automaton.arrayChans",True): # generated from line 35, col 1
            write(u'''\tstd::vector <Channel*> &''')
            _v = VFFSL(SL,"p",True) # u'$p' on line 36, col 26
            if _v is not None: write(_filter(_v, rawExpr=u'$p')) # from line 36, col 26.
            write(u''';
''')
        write(u'''

''')
        for p in VFFSL(SL,"automaton.timers",True): # generated from line 40, col 1
            write(u'''\tTimer* ''')
            _v = VFFSL(SL,"p",True) # u'$p' on line 41, col 9
            if _v is not None: write(_filter(_v, rawExpr=u'$p')) # from line 41, col 9.
            write(u''';
''')
        write(u'''
''')
        for p in VFFSL(SL,"automaton.arrayTimers",True): # generated from line 44, col 1
            write(u'''\tstd::vector <Timer*> &''')
            _v = VFFSL(SL,"p",True) # u'$p' on line 45, col 24
            if _v is not None: write(_filter(_v, rawExpr=u'$p')) # from line 45, col 24.
            write(u''';
''')
        write(u'''
''')
        for p in VFFSL(SL,"automaton.localVars",True): # generated from line 48, col 1
            write(u'''\tVar ''')
            _v = VFFSL(SL,"p",True) # u'$p' on line 49, col 6
            if _v is not None: write(_filter(_v, rawExpr=u'$p')) # from line 49, col 6.
            write(u''';
''')
        write(u'''
''')
        for p in VFFSL(SL,"automaton.localClocks",True): # generated from line 52, col 1
            write(u'''\tTimer ''')
            _v = VFFSL(SL,"p",True) # u'$p' on line 53, col 8
            if _v is not None: write(_filter(_v, rawExpr=u'$p')) # from line 53, col 8.
            write(u''';
''')
        write(u'''
''')
        for p in VFN(VFFSL(SL,"automaton.localArrayClocks",True),"keys",False)(): # generated from line 56, col 1
            write(u'''\tstd::vector <Timer*> ''')
            _v = VFFSL(SL,"p",True) # u'$p' on line 57, col 23
            if _v is not None: write(_filter(_v, rawExpr=u'$p')) # from line 57, col 23.
            write(u''';
''')
        write(u'''
\t''')
        _v = VFFSL(SL,"automaton.name",True) # u'${automaton.name}' on line 60, col 2
        if _v is not None: write(_filter(_v, rawExpr=u'${automaton.name}')) # from line 60, col 2.
        write(u'''(std::string _name, Network *n, int p, bool t''')
        for p in VFFSL(SL,"automaton.typedParams",True): # generated from line 61, col 1
            write(u''', ''')
            _v = VFFSL(SL,"p",True)[1] # u'${p[1]}' on line 62, col 3
            if _v is not None: write(_filter(_v, rawExpr=u'${p[1]}')) # from line 62, col 3.
            write(u'''* _''')
            _v = VFFSL(SL,"p",True)[0] # u'${p[0]}' on line 62, col 13
            if _v is not None: write(_filter(_v, rawExpr=u'${p[0]}')) # from line 62, col 13.
        for p in VFFSL(SL,"automaton.arrayTypedParams",True): # generated from line 64, col 1
            write(u''', std::vector <''')
            _v = VFFSL(SL,"p",True)[1] # u'${p[1]}' on line 65, col 16
            if _v is not None: write(_filter(_v, rawExpr=u'${p[1]}')) # from line 65, col 16.
            write(u'''*> & _''')
            _v = VFFSL(SL,"p",True)[0] # u'${p[0]}' on line 65, col 29
            if _v is not None: write(_filter(_v, rawExpr=u'${p[0]}')) # from line 65, col 29.
        for p in VFFSL(SL,"automaton.vars",True): # generated from line 67, col 1
            write(u''', Var* _''')
            _v = VFFSL(SL,"p",True) # u'$p' on line 68, col 9
            if _v is not None: write(_filter(_v, rawExpr=u'$p')) # from line 68, col 9.
        for p in VFFSL(SL,"automaton.arrayVars",True): # generated from line 70, col 1
            write(u''', std::vector <Var*> &_''')
            _v = VFFSL(SL,"p",True) # u'$p' on line 71, col 24
            if _v is not None: write(_filter(_v, rawExpr=u'$p')) # from line 71, col 24.
        for p in VFFSL(SL,"automaton.arrayArrayVars",True): # generated from line 73, col 1
            write(u''', std::vector < std::vector <Var*> > &_''')
            _v = VFFSL(SL,"p",True) # u'$p' on line 74, col 40
            if _v is not None: write(_filter(_v, rawExpr=u'$p')) # from line 74, col 40.
        for p in VFFSL(SL,"automaton.chans",True): # generated from line 76, col 1
            write(u''', Channel* _''')
            _v = VFFSL(SL,"p",True) # u'$p' on line 77, col 13
            if _v is not None: write(_filter(_v, rawExpr=u'$p')) # from line 77, col 13.
        for p in VFFSL(SL,"automaton.arrayChans",True): # generated from line 79, col 1
            write(u''', std::vector <Channel*> &_''')
            _v = VFFSL(SL,"p",True) # u'$p' on line 80, col 28
            if _v is not None: write(_filter(_v, rawExpr=u'$p')) # from line 80, col 28.
        for p in VFFSL(SL,"automaton.timers",True): # generated from line 82, col 1
            write(u''', Timer* _''')
            _v = VFFSL(SL,"p",True) # u'$p' on line 83, col 11
            if _v is not None: write(_filter(_v, rawExpr=u'$p')) # from line 83, col 11.
        for p in VFFSL(SL,"automaton.arrayTimers",True): # generated from line 85, col 1
            write(u''', std::vector <Timer*> &_''')
            _v = VFFSL(SL,"p",True) # u'$p' on line 86, col 26
            if _v is not None: write(_filter(_v, rawExpr=u'$p')) # from line 86, col 26.
        write(u''');

''')
        _v = VFFSL(SL,"automaton.declaration",True) # u'$automaton.declaration' on line 90, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$automaton.declaration')) # from line 90, col 1.
        write(u'''
};

''')
        VFN(VFFSL(SL,"automaton.transitions",True),"sort",False)(key=lambda x: x.channel_prio)
        write(u'''
''')
        tnum = 0
        for t in VFFSL(SL,"automaton.transitions",True): # generated from line 96, col 1
            write(u'''class ''')
            _v = VFN(VFN(VFFSL(SL,"automaton",True),"states",True)[VFFSL(SL,"t.src",True)],"name",True) # u'${automaton.states[$t.src].name}' on line 97, col 7
            if _v is not None: write(_filter(_v, rawExpr=u'${automaton.states[$t.src].name}')) # from line 97, col 7.
            write(u'''_''')
            _v = VFN(VFN(VFFSL(SL,"automaton",True),"states",True)[VFFSL(SL,"t.dst",True)],"name",True) # u'${automaton.states[$t.dst].name}' on line 97, col 40
            if _v is not None: write(_filter(_v, rawExpr=u'${automaton.states[$t.dst].name}')) # from line 97, col 40.
            write(u'''_''')
            _v = VFFSL(SL,"tnum",True) # u'$tnum' on line 97, col 73
            if _v is not None: write(_filter(_v, rawExpr=u'$tnum')) # from line 97, col 73.
            write(u''': public Transition {
\t''')
            _v = VFFSL(SL,"automaton.name",True) # u'${automaton.name}' on line 98, col 2
            if _v is not None: write(_filter(_v, rawExpr=u'${automaton.name}')) # from line 98, col 2.
            write(u'''* automaton;
\t''')
            _v = VFFSL(SL,"t.local",True) # u'$t.local' on line 99, col 2
            if _v is not None: write(_filter(_v, rawExpr=u'$t.local')) # from line 99, col 2.
            write(u'''

public:
''')
            if VFFSL(SL,"t.channel",True)=="": # generated from line 102, col 1
                write(u'''\t''')
                _v = VFN(VFN(VFFSL(SL,"automaton",True),"states",True)[VFFSL(SL,"t.src",True)],"name",True) # u'${automaton.states[$t.src].name}' on line 103, col 2
                if _v is not None: write(_filter(_v, rawExpr=u'${automaton.states[$t.src].name}')) # from line 103, col 2.
                write(u'''_''')
                _v = VFN(VFN(VFFSL(SL,"automaton",True),"states",True)[VFFSL(SL,"t.dst",True)],"name",True) # u'${automaton.states[$t.dst].name}' on line 103, col 35
                if _v is not None: write(_filter(_v, rawExpr=u'${automaton.states[$t.dst].name}')) # from line 103, col 35.
                write(u'''_''')
                _v = VFFSL(SL,"tnum",True) # u'$tnum' on line 103, col 68
                if _v is not None: write(_filter(_v, rawExpr=u'$tnum')) # from line 103, col 68.
                write(u''' (Network *_net, Location *_next, ''')
                _v = VFFSL(SL,"automaton.name",True) # u'${automaton.name}' on line 103, col 107
                if _v is not None: write(_filter(_v, rawExpr=u'${automaton.name}')) # from line 103, col 107.
                write(u''' *_aut): Transition(_net, _next), automaton(_aut) {}
''')
            else: # generated from line 104, col 1
                write(u'''\t''')
                _v = VFN(VFN(VFFSL(SL,"automaton",True),"states",True)[VFFSL(SL,"t.src",True)],"name",True) # u'${automaton.states[$t.src].name}' on line 105, col 2
                if _v is not None: write(_filter(_v, rawExpr=u'${automaton.states[$t.src].name}')) # from line 105, col 2.
                write(u'''_''')
                _v = VFN(VFN(VFFSL(SL,"automaton",True),"states",True)[VFFSL(SL,"t.dst",True)],"name",True) # u'${automaton.states[$t.dst].name}' on line 105, col 35
                if _v is not None: write(_filter(_v, rawExpr=u'${automaton.states[$t.dst].name}')) # from line 105, col 35.
                write(u'''_''')
                _v = VFFSL(SL,"tnum",True) # u'$tnum' on line 105, col 68
                if _v is not None: write(_filter(_v, rawExpr=u'$tnum')) # from line 105, col 68.
                write(u''' (Network *_net, Location *_next, ''')
                _v = VFFSL(SL,"automaton.name",True) # u'${automaton.name}' on line 105, col 107
                if _v is not None: write(_filter(_v, rawExpr=u'${automaton.name}')) # from line 105, col 107.
                write(u''' *_aut): Transition(_net, _next), automaton(_aut)
\t{
\t\tis_sender = ''')
                _v = VFN(VFFSL(SL,"str",False)(t.is_sender),"lower",False)() # u'${str(t.is_sender).lower()}' on line 107, col 15
                if _v is not None: write(_filter(_v, rawExpr=u'${str(t.is_sender).lower()}')) # from line 107, col 15.
                write(u''';
\t}
''')
            write(u'''
''')
            if VFFSL(SL,"t.guard",True)!="": # generated from line 111, col 1
                write(u'''\tvirtual bool guard()
\t{
\t\treturn ''')
                _v = VFFSL(SL,"t.guard",True) # u'$t.guard' on line 114, col 10
                if _v is not None: write(_filter(_v, rawExpr=u'$t.guard')) # from line 114, col 10.
                write(u''';
\t}
''')
            write(u'''
''')
            if VFFSL(SL,"t.complex_guard",True)!="": # generated from line 118, col 1
                write(u'''\tvirtual bool guard()
\t{
\t\t''')
                _v = VFFSL(SL,"t.complex_guard",True) # u'$t.complex_guard' on line 121, col 3
                if _v is not None: write(_filter(_v, rawExpr=u'$t.complex_guard')) # from line 121, col 3.
                write(u'''
\t}
''')
            write(u'''

''')
            if VFFSL(SL,"t.action",True)!="": # generated from line 126, col 1
                write(u'''\tvirtual void action()
\t{
\t\t''')
                _v = VFFSL(SL,"t.action",True) # u'$t.action' on line 129, col 3
                if _v is not None: write(_filter(_v, rawExpr=u'$t.action')) # from line 129, col 3.
                write(u''';
\t}
''')
            write(u'''
''')
            if VFFSL(SL,"t.channel",True)!="": # generated from line 133, col 1
                write(u'''\tvirtual bool synchronize()
\t{
\t\tchannel = &(''')
                _v = VFFSL(SL,"t.channel",True) # u'$t.channel' on line 136, col 15
                if _v is not None: write(_filter(_v, rawExpr=u'$t.channel')) # from line 136, col 15.
                write(u''');
\t\treturn Transition::synchronize();
\t}

\tvirtual bool needSync()
\t{
\t\treturn true;
\t}
''')
            write(u'''
};
''')
            tnum = VFFSL(SL,"tnum",True) + 1
            write(u'''
''')
        write(u'''
''')
        for s in VFN(VFFSL(SL,"automaton.states",True),"values",False)(): # generated from line 151, col 1
            write(u'''class ''')
            _v = VFFSL(SL,"s.name",True) # u'$s.name' on line 152, col 7
            if _v is not None: write(_filter(_v, rawExpr=u'$s.name')) # from line 152, col 7.
            write(u''': public Location {
\t''')
            _v = VFFSL(SL,"automaton.name",True) # u'${automaton.name}' on line 153, col 2
            if _v is not None: write(_filter(_v, rawExpr=u'${automaton.name}')) # from line 153, col 2.
            write(u'''* automaton;
public:
\t''')
            _v = VFFSL(SL,"s.name",True) # u'$s.name' on line 155, col 2
            if _v is not None: write(_filter(_v, rawExpr=u'$s.name')) # from line 155, col 2.
            write(u''' (Network *n, std::string _name, bool init, bool committed, ''')
            _v = VFFSL(SL,"automaton.name",True) # u'${automaton.name}' on line 155, col 69
            if _v is not None: write(_filter(_v, rawExpr=u'${automaton.name}')) # from line 155, col 69.
            write(u''' *a): Location (n, _name, init, committed), automaton(a) {}
''')
            if VFFSL(SL,"len",False)(VFFSL(SL,"s.timers",True)) != 0: # generated from line 156, col 1
                write(u'''\tvirtual bool checkTimer(Timer *__t)
\t{
''')
                for t in VFFSL(SL,"s.timers",True): # generated from line 159, col 1
                    write(u'''\t\tif ( __t == ''')
                    _v = VFFSL(SL,"t",True)[0] # u'${t[0]}' on line 160, col 15
                    if _v is not None: write(_filter(_v, rawExpr=u'${t[0]}')) # from line 160, col 15.
                    write(u''')
\t\t\treturn ''')
                    _v = VFFSL(SL,"t",True)[1] # u'${t[1]}' on line 161, col 11
                    if _v is not None: write(_filter(_v, rawExpr=u'${t[1]}')) # from line 161, col 11.
                    write(u''';
''')
                write(u'''\t\treturn true;
\t}
''')
            write(u'''};

''')
        write(u'''
}

#endif
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        
    ##################################################
    ## CHEETAH GENERATED ATTRIBUTES


    _CHEETAH__instanceInitialized = False

    _CHEETAH_version = __CHEETAH_version__

    _CHEETAH_versionTuple = __CHEETAH_versionTuple__

    _CHEETAH_genTime = __CHEETAH_genTime__

    _CHEETAH_genTimestamp = __CHEETAH_genTimestamp__

    _CHEETAH_src = __CHEETAH_src__

    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__

    _mainCheetahMethod_for_automaton_h = 'respond'

## END CLASS DEFINITION

if not hasattr(automaton_h, '_initCheetahAttributes'):
    templateAPIClass = getattr(automaton_h,
                               '_CHEETAH_templateClass',
                               Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(automaton_h)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=automaton_h()).run()


