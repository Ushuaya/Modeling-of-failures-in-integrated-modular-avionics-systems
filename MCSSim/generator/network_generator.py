# -*- coding: utf-8 -*-
import xml.dom.minidom
import sys
import os
import re
from automaton_h import automaton_h
from automaton_cpp import automaton_cpp
from cmakelists import cmakelists
from common_h import common_h
from common_cpp import common_cpp

class State:
    def __init__(self, node, a):
        self.automaton = a
        self.id = node.getAttribute("id")
        self.timers = []
        self.inv = ""
        self.committed = "false"
        for node1 in node.childNodes:
            if isinstance(node1, xml.dom.minidom.Text) or isinstance(node1, xml.dom.minidom.Comment):
                continue
            if node1.tagName=="name":
                for node2 in node1.childNodes:
                    if isinstance(node2, xml.dom.minidom.Text):
                        self.name = node2.data
            if node1.tagName=="label":
                if node1.getAttribute("kind")=="invariant":
                    for node2 in node1.childNodes:
                        if isinstance(node2, xml.dom.minidom.Text):
                            self.inv = node2.data
            if node1.tagName=="committed" or node1.tagName=="urgent":
                self.committed = "true"


    def processInv(self):
        for s in self.inv.split("&&"):
            if "'" in s: #условие продвижения таймера
                s=s.replace(" ", "")
                timer = s[:s.index("'")]
                timer = "&(" + self.automaton.strToCpp(timer) + ")"
                pred = s[s.index("==")+2:]
                pred = self.automaton.strToCpp(pred)
                self.timers.append((timer,pred));

class Transition:
    def __init__(self, node, a, local="", edges=[]):
        self.channel = ""
        self.channel_prio = ""
        self.complex_guard = ""
        self.guard = ""
        self.action= ""
        self.automaton = a
        self.local = ""
        if local != "":
            self.local = "int " + local + ";"
        for node1 in node.childNodes:
            if isinstance(node1, xml.dom.minidom.Text) or isinstance(node1, xml.dom.minidom.Comment):
                continue
            if node1.tagName=="source":
                self.src=node1.getAttribute("ref")
            if node1.tagName=="target":
                self.dst=node1.getAttribute("ref")
            if node1.tagName=="label":
                if node1.getAttribute("kind")=="synchronisation":
                    for node2 in node1.childNodes:
                        if isinstance(node2, xml.dom.minidom.Text):
                            self.is_sender = node2.data[-1]=="!"
                            self.channel = node2.data[:-1]
                if node1.getAttribute("kind")=="guard":
                    for node2 in node1.childNodes:
                        if isinstance(node2, xml.dom.minidom.Text):
                            if (local != ""):
                                self.complex_guard = "for (%s = %s; %s <= %s; %s++) {\n" % (local, edges[0], local, edges[1], local) 
                                self.complex_guard += "\tif ( " + node2.data + " ) {\n";
                                self.complex_guard += "\t\treturn true;\n"
                                self.complex_guard += "\t}\n"
                                self.complex_guard += "\t}\n"
                                self.complex_guard += "\treturn false;\n"
                            else:
                                if "forall" not in node2.data:
                                    self.guard = node2.data
                                else:
                                    tmp = node2.data.strip()
                                    iterator = tmp[tmp.index("(")+1:tmp.index(":")]
                                    edges = tmp[tmp.index("[")+1:tmp.index("]")].split(",")
                                    tmp = tmp[tmp.index(")")+1:]
                                    self.complex_guard = "for (int %s = %s; %s <= %s; %s++) {\n" % (iterator, edges[0], iterator, edges[1], iterator) 
                                    self.complex_guard += "\tif (!(" + tmp + ")) {\n";
                                    self.complex_guard += "\t\treturn false;\n"
                                    self.complex_guard += "\t}\n"
                                    self.complex_guard += "\t}\n"
                                    self.complex_guard += "\treturn true;\n"




                if node1.getAttribute("kind")=="assignment":
                    for node2 in node1.childNodes:
                        if isinstance(node2, xml.dom.minidom.Text):
                            self.action = node2.data
                if node1.getAttribute("kind")=="testcode":
                    for node2 in node1.childNodes:
                        if isinstance(node2, xml.dom.minidom.Text):
                            self.channel_prio = node2.data


class Automaton:
    def __init__(self, node, net):
        self.net = net
        self.states = {}
        self.transitions = []
        self.declaration = ''
        for node1 in node.childNodes:
            if isinstance(node1, xml.dom.minidom.Text) or isinstance(node1, xml.dom.minidom.Comment):
                continue
            if node1.tagName=="name":
                for node2  in node1.childNodes:
                    if isinstance(node2, xml.dom.minidom.Text):
                        self.name = node2.data
            if node1.tagName=="parameter":
                for node2  in node1.childNodes:
                    if isinstance(node2, xml.dom.minidom.Text):
                        self.parseParameters(node2.data)
                        #FIXME
            if node1.tagName=="declaration":
                for node2 in node1.childNodes:
                    if isinstance(node2, xml.dom.minidom.Text):
                        self.declaration=node2.data

            if node1.tagName=="location":
                s = State(node1, self)
                self.states[s.id] = s
            if node1.tagName=="init":
                self.init = node1.getAttribute("ref")
            if node1.tagName=="transition":
                iterator = ""
                edges = []
                for n in node1.getElementsByTagName("label"):
                    if n.getAttribute("kind")=="select":
                        for n1 in n.childNodes:
                            if isinstance(n1, xml.dom.minidom.Text):
                                tmp = n1.data.strip()
                                iterator = tmp[0:tmp.index(":")]
                                edges = tmp[tmp.index("[")+1:tmp.rindex("]")].split(",")
                if iterator == "":
                    self.transitions.append(Transition(node1, self))
                else:
                    self.transitions.append(Transition(node1, self, iterator, edges))

    def processDeclaration(self):
        self.localVars = set()
        self.localClocks = set ()
        self.localArrayVars = set()
        self.localArrayClocks = {}
        self.functions = []
        new_decl = ""
        for string in self.declaration.split('\n'):
            tmp = string.strip()
            if tmp.startswith('for'):
                iterator = tmp[tmp.index("(")+1:tmp.index(":")]
                edges = tmp[tmp.index("[")+1:tmp.rindex("]")].split(",")
                tmp = "for (int %s = %s; %s <= %s; %s++) {" % (iterator, edges[0], iterator, edges[1], iterator)
                new_decl += self.strToCpp(tmp)
            elif tmp.startswith('int') and tmp.endswith("];"): #локальный массив переменных
                new_decl += tmp;
                tmp = tmp.replace("int", "").replace(" ", "");
                tmp = tmp[:tmp.index("[")]
                self.localArrayVars.add(tmp)
            elif tmp.startswith('int') and tmp.endswith(";"): #локальная переменная
                tmp = tmp.replace("int", "").replace(" ", "")[:-1] #откусываем ;
                self.localVars.add(tmp)
            elif tmp.startswith('bool') and tmp.endswith("];"): #локальный массив переменных
                new_decl += tmp;
                tmp = tmp.replace("bool", "").replace(" ", "");
                tmp = tmp[:tmp.index("[")]
                self.localArrayVars.add(tmp)
            elif tmp.startswith('bool') and tmp.endswith(";"): #локальная переменная
                tmp = tmp.replace("bool", "").replace(" ", "")[:-1] #откусываем ;
                self.localVars.add(tmp)
            elif tmp.startswith('clock') and tmp.endswith("];"): #локальный массив таймеров
                tmp = tmp.replace("clock", "").replace(" ", "");
                size = tmp[tmp.index("[")+1:tmp.rindex("]")]
                tmp = tmp[:tmp.index("[")]
                self.localArrayClocks[tmp]=size
            elif tmp.startswith('clock'): #локальный таймер
                tmp = tmp.replace("clock", "").replace(" ", "")[:-1] #откусываем ;
                self.localClocks.add(tmp)
            elif tmp.startswith('int'): #функция
                tmp = tmp.replace("int", "", 1).replace(" ", "") #убираем первый int и пробелы
                tmp = tmp[:tmp.index("(")] #выделяем имя функции
                self.functions.append(tmp)
                new_decl += string
            elif tmp.startswith('bool'): #функция
                tmp = tmp.replace("bool", "", 1).replace(" ", "") #убираем первый bool и пробелы
                tmp = tmp[:tmp.index("(")] #выделяем имя функции
                self.functions.append(tmp)
                new_decl += string
            elif tmp.startswith('void'): #функция
                tmp = tmp.replace("void", "", 1).replace(" ", "") #убираем первый void и пробелы
                tmp = tmp[:tmp.index("(")] #выделяем имя функции
                self.functions.append(tmp)
                new_decl += string
            elif tmp.startswith('meta'): #переменные внутри функции
                new_decl += string.replace("meta", "")
            else:
                new_decl += self.strToCpp(string)
            new_decl+='\n'
        self.declaration = new_decl

    def strToCpp(self, string):
        string = string.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        p = re.compile('([a-zA-Z][\w]*)')
        processed = set()
        for param in p.findall(string): #цикл по всем найденным параметрам
            if param in processed:
                continue
            p1 = re.compile(r'(^|[^a-zA-Z0-9_.])(' + param + r')(\b|\W)')
            if param in self.vars or param in self.timers or param in self.chans or param in self.typedParamsNames:
                string = p1.sub(r'\1(*(automaton->\2))\3', string)
            if param in self.arrayVars or param in self.arrayArrayVars or param in self.arrayTimers or param in self.arrayChans or param in self.arrayTypedParamsNames:
                string = p1.sub(r'\1*automaton->\2\3', string)
            if param in self.localVars or param in self.localClocks or param in self.functions:
                string = p1.sub(r'\1automaton->\2\3', string)
            if param in self.localArrayVars:
                string = p1.sub(r'\1automaton->\2\3', string)
            if param in self.localArrayClocks.keys():
                string = p1.sub(r'\1*automaton->\2\3', string)

            processed.add(param)
        return string

    def toCpp(self):
        self.processDeclaration()
        for s in self.states.values():
            s.processInv()
        for t in self.transitions:
            t.guard = self.strToCpp(t.guard)
            t.complex_guard = self.strToCpp(t.complex_guard)
            t.action = self.strToCpp(t.action)
            t.channel = self.strToCpp(t.channel)
      

    def getArrayName(self, string):
        try:
            name = string[0:string.index("[")]
        except:
            print "Error in array parameter"
        return name

    def getArrayLevel(self, string):
        return string.count("]")


    def parseParameters(self, params):
        params = params.replace(" ","")
        self.vars = []
        self.timers = []
        self.chans = []
        self.arrayVars = []
        self.arrayArrayVars = []
        self.arrayTimers = []
        self.arrayChans = []
        self.typedParams = []
        self.arrayTypedParams = []
        self.typedParamsNames = []
        self.arrayTypedParamsNames = []
        for e in params.split(","):
            if e.startswith("chan") or e.startswith("broadcast"):
                e = e.replace("broadcast", "")
                if e.endswith("]"): #array
                    e = e.replace("chan&","")
                    name = self.getArrayName(e)
                    self.arrayChans.append(name)
                else: #обычная переменная
                    self.chans.append(e.replace("chan&",""))

            elif e.startswith("int"):
                if e.endswith("]"): #array
                    e = e.replace("int&","")
                    name = self.getArrayName(e)
                    level =  self.getArrayLevel(e)
                    if level==1:
                        self.arrayVars.append(name)
                    else:
                        self.arrayArrayVars.append(name)

                else: #обычная переменная
                    self.vars.append(e.replace("int&",""))
            elif e.startswith("clock"):
                if e.endswith("]"): #array
                    e = e.replace("clock&","")
                    name = self.getArrayName(e)
                    self.arrayTimers.append(name)
                else: #обычный таймер
                    self.timers.append(e.replace("clock&",""))
            else:
                if e.endswith("]"): #array
                    name = self.getArrayName(e.split("&")[1])
                    self.arrayTypedParams.append((name, e.split("&")[0]))
                    self.arrayTypedParamsNames.append(name)
                else: #обычный параметр пользовательского типа
                    self.typedParams.append((e.split("&")[1], e.split("&")[0]));
                    self.typedParamsNames.append(e.split("&")[1])
                

class Network:
    def __init__(self, node):
        self.automata = []
        self.declaration = ""
        for node1 in node.childNodes:
            if isinstance(node1, xml.dom.minidom.Text) or isinstance(node1, xml.dom.minidom.Comment):
                continue
            if node1.tagName=="template":
                self.automata.append(Automaton(node1, self))
            if node1.tagName=="declaration":
                for node2  in node1.childNodes:
                    if isinstance(node2, xml.dom.minidom.Text):
                        self.declaration = node2.data

    def processCommonDeclaration(self):
        new_decl = ""
        for string in self.declaration.split('\n'):
            if '[' in string:
                string = string.strip()
                t = string.split(" ")[0]
                name =  string.split(" ")[1]
                name = name[:name.index("[")]
                new_decl += "std::vector <" + t + "> " + name + ";"
            else:
                new_decl += string
            new_decl += "\n"
        self.declaration = new_decl
#         print self.declaration


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + sys.argv[0] + " <models directory>"
        exit(1)

    commonH = common_h()
    commonH.nta = []
    commonH.declarations = []
    commonH.base = {}

    commonCPP = common_cpp()
    commonCPP.nta = []
    commonCPP.declarations = []
    commonCPP.base = {}


    cmake = cmakelists()
    cmake.nta = []
    for f in os.listdir(sys.argv[1]):
        if os.path.isdir(sys.argv[1] + "/" + f):
            baseType = f
            i = 0
            commonH.base[f] = []
            commonCPP.base[f] = []
            for f1 in os.listdir(sys.argv[1] + "/" + f):
                concreteType = f1
                file1 = open(sys.argv[1] + "/" + f + "/" + f1)
                dom = xml.dom.minidom.parse(file1)
                for node in dom.getElementsByTagName("nta"):
                    if isinstance(node, xml.dom.minidom.DocumentType):
                        continue
                    if isinstance(node, xml.dom.minidom.Text) or isinstance(node, xml.dom.minidom.Comment):
                        continue
                    if node.tagName=="nta":
                        n = Network(node)
                        n.processCommonDeclaration()
                        commonH.nta.append(n)
                        commonCPP.nta.append(n)
                        if i == 0:
                            commonH.declarations.append(n.declaration)
                            commonCPP.declarations.append(n.declaration)

                        for a in n.automata:
                            commonH.base[f].append(a);
                            commonCPP.base[f].append(a);
                            a.toCpp()
                            autH = automaton_h()
                            autH.automaton = a
                            outH = open("generated_components/"+a.name+".h", "w")
                            outH.write(str(autH))
                            outH.close()
                            autCpp = automaton_cpp()
                            autCpp.automaton = a
                            outCpp = open("generated_components/"+a.name+".cpp", "w")
                            outCpp.write(str(autCpp))
                            outCpp.close()
                            cmake.nta.append(a)
                i += 1

    outCommonH = open("generated_components/common.h", "w")
    outCommonH.write(str(commonH))
    outCommonH.close()

    outCommonCPP = open("generated_components/common.cpp", "w")
    outCommonCPP.write(str(commonCPP))
    outCommonCPP.close()

    outCmake =  open("generated_components/CMakeLists.txt", "w")
    outCmake.write(str(cmake))
    outCmake.close()
