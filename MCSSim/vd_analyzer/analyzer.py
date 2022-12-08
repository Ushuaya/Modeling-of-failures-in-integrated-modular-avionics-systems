# -*- coding: utf-8 -*-
import xml.dom.minidom
import sys



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: " + sys.argv[0] + "<conf.xml> <vd.xml>"
        exit(1)

    file_conf = open(sys.argv[1])
    dom_conf = xml.dom.minidom.parse(file_conf)

    tasks = {}

    for node in dom_conf.getElementsByTagName("task"):
        if isinstance(node, xml.dom.minidom.Text) or isinstance(node, xml.dom.minidom.Comment):
            continue

        task_id = node.getAttribute("id")
        tasks[task_id] = {}

        tasks[task_id]["period"] = node.getAttribute("period")
        tasks[task_id]["deadline"] = node.getAttribute("deadline")
        tasks[task_id]["wcet"] = node.getAttribute("wcet")

    dom_conf.unlink()
    file_conf.close()

    file_vd = open(sys.argv[2])
    dom_vd = xml.dom.minidom.parse(file_vd)

    for node in dom_vd.getElementsByTagName("task"):
        if isinstance(node, xml.dom.minidom.Text) or isinstance(node, xml.dom.minidom.Comment):
            continue

        task_id = node.getAttribute("id")
        #print node.getAttribute("name")
        for node1 in node.childNodes:
            if isinstance(node1, xml.dom.minidom.Text) or isinstance(node1, xml.dom.minidom.Comment):
                continue
            if node1.tagName == "job":
                job_num = int(node1.getAttribute("id"))
                exec_time = 0
                cur_time = 0;
                #print 1
                for node2 in node1.childNodes:
                    if isinstance(node2, xml.dom.minidom.Text) or isinstance(node2, xml.dom.minidom.Comment):
                        continue
                    if node2.tagName == 'event':
                        e_time = int(node2.getAttribute("time"))
                        e_type = node2.getAttribute("type")
                        if e_type == "exec":
                            cur_time = e_time;
                        if e_type == "preempt" or e_type == "finished":
                            exec_time += e_time - cur_time
                #print exec_time, int(tasks[task_id]["wcet"])
                if (exec_time != int(tasks[task_id]["wcet"])):
                    #print exec_time, int(tasks[task_id]["wcet"])
                    print False
                    exit(1)

    print True

                        

