#include "common.h"
#include "T.h"
#include "rapidxml/rapidxml.hpp"
#include "rapidxml/rapidxml_print.hpp"

#include <fstream>
#include <string.h>
#include <time.h>

using namespace std;
using namespace rapidxml;

void buildNetwork(char* filename, Network &n)
{
	int tasks_num=0, msgs_num=0, partitions_num=0, cores_num=0, windows_num=0;
	xml_document<> doc;
	xml_node<> * root_node;
	// Read the xml file into a vector
	ifstream file(filename);
	vector<char> buffer((istreambuf_iterator<char>(file)), istreambuf_iterator<char>());
	buffer.push_back('\0');
	// Parse the buffer using the xml file parsing library into doc

	doc.parse<0>(&buffer[0]);
	root_node = doc.first_node("system");

	map <int, Channel *> send_m;
	map <int, Channel *> receive_m;
	map <int, vector <Var*>* > is_data_ready_m;
	map <int, TaskData*> taskData_m;

	//разбор модулей
	int mod_id=0;
	for (xml_node<> * module_node = root_node->first_node("module"); module_node; module_node = module_node->next_sibling(), mod_id++) {
		if (strcmp(module_node->name(), "module"))
			continue;
		CoreSchedulerData* globalSchedulerData = new CoreSchedulerData;
		globalSchedulerData->majorFrame = atoi(module_node->first_attribute("major_frame")->value());
		if (n.simulationInterval < globalSchedulerData->majorFrame)
			n.simulationInterval = globalSchedulerData->majorFrame;

		//разбор окон
		for (xml_node<> *window_node = module_node->first_node("window"); window_node; window_node = window_node->next_sibling()) {
			if (strcmp(window_node->name(), "window"))
				continue;
			WindowData *w = new WindowData;
			w->start = atoi(window_node->first_attribute("start")->value());
			w->stop = atoi(window_node->first_attribute("stop")->value());
			w->partitionId = atoi(window_node->first_attribute("partition")->value());
			globalSchedulerData->windows.push_back(*w);
			windows_num++;
		}
		globalSchedulerData->numOfWindows = globalSchedulerData->windows.size();
		if (globalSchedulerData->numOfWindows == 0)
			continue;

		vector <Channel*> *wakeup_v = new vector <Channel*>;
		vector <Channel*> *sleep_v = new vector <Channel*>;


		//разбор разделов
		int id = 0;
		for (xml_node<> *partition_node = module_node->first_node("partition"); partition_node; partition_node = partition_node->next_sibling(), ++id) {
			if (strcmp(partition_node->name(), "partition"))
				continue;

			TaskSchedulerData* localSchedulerData = new TaskSchedulerData;

			vector <Var*> *is_ready_v = new vector <Var*>;
			vector <Var*> *abs_deadline_v = new vector <Var*>;
			vector <Var*> *prio_v = new vector <Var*>;
			vector <Var*> *id_v = new vector <Var*>;
			vector <Channel*> *exec_v = new vector <Channel*>;
			vector <Channel*> *preempt_v = new vector <Channel*>;

			Channel *finished = new DuplexChannel(&n, "finished");
			Channel *ready = new DuplexChannel(&n, "ready");

			//разбор задач
			for (xml_node<> *task_node = partition_node->first_node("task"); task_node; task_node = task_node->next_sibling()) {
				if (strcmp(task_node->name(), "task"))
					continue;
				TaskData *t = new TaskData;
				int t_id = atoi(task_node->first_attribute("id")->value());
				t->wcet = atoi(task_node->first_attribute("wcet")->value());
				int t_prio = atoi(task_node->first_attribute("prio")->value());
				t->offset = atoi(task_node->first_attribute("offset")->value());
				t->period = atoi(task_node->first_attribute("period")->value());
				t->deadline = atoi(task_node->first_attribute("deadline")->value());
				t->numOfInputLinks = 0;
				//localSchedulerData->tasks.push_back(*t);

				taskData_m[t_id] = t;

				Var *is_ready = new Var(&n, "is_ready"+to_string(t_id));
				is_ready_v->push_back(is_ready);

				Var *abs_deadline = new Var(&n, "abs_deadline"+to_string(t_id));
				abs_deadline_v->push_back(abs_deadline);

				Var *prio = new Var(&n, "prio"+to_string(t_id));
				*prio = t_prio;
				prio_v->push_back(prio);

				Var *id = new Var(&n, "id"+to_string(t_id));
				*id = t_id;
				id_v->push_back(id);

				Channel *preempt = new DuplexChannel(&n, "preempt"+to_string(t_id));
				preempt_v->push_back(preempt);

				Channel *exec = new DuplexChannel(&n, "exec"+to_string(t_id));
				exec_v->push_back(exec);

				Channel *receive = new BroadcastChannel(&n, "receive"+to_string(t_id));
				Channel *send = new BroadcastChannel(&n, "send"+to_string(t_id));
				receive_m[t_id] = receive;
				send_m[t_id] = send;

				vector <Var*> *is_data_ready = new vector <Var*>;
				is_data_ready_m[t_id] = is_data_ready;

				createT("T", "task"+to_string(t_id) + "_" + task_node->first_attribute("name")->value(),
					&n,
					1,
					true,
					t,
					abs_deadline,
					is_ready,
					prio,
					*is_data_ready,
					exec,
					preempt,
					ready,
					finished,
					send,
					receive
					);
				tasks_num++;
			}
			localSchedulerData->numOfTasks = is_ready_v->size();

			Channel *wakeup = new DuplexChannel(&n, "wakeup");
			wakeup_v->push_back(wakeup);
			Channel *sleep = new DuplexChannel(&n, "sleep");
			sleep_v->push_back(sleep);


			createTS(partition_node->first_attribute("scheduler")->value(), "localscheduler"+to_string(mod_id)+module_node->first_attribute("name")->value() + "_" + to_string(id),
				&n,
				3,
				false,
				localSchedulerData,
				*abs_deadline_v,
				*is_ready_v,
				*prio_v,
				*id_v,
				wakeup,
				sleep,
				ready,
				finished,
				*exec_v,
				*preempt_v
				);
			partitions_num++;
		}

		createCS("CS", (string)"globalscheduler_" + module_node->first_attribute("name")->value(),
			&n,
			4,
			false,
			globalSchedulerData,
			*wakeup_v,
			*sleep_v
			);
		cores_num++;
	}

	//разбор зависимостей по данным (должен быть после разбора задач, когда каналы send-receive уже созданы)
	for (xml_node<> * link_node = root_node->first_node("link"); link_node; link_node = link_node->next_sibling()) {
		if (strcmp(link_node->name(), "link"))
			continue;
		int src = atoi(link_node->first_attribute("src")->value());
		int dst = atoi(link_node->first_attribute("dst")->value());
		LinkData * linkData = new LinkData;
		Var *is_data_ready = new Var(&n, "is_data_ready"+to_string(dst));
		is_data_ready_m[dst]->push_back(is_data_ready);
		taskData_m[dst]->numOfInputLinks++;

		linkData->delay = atoi(link_node->first_attribute("delay")->value());
		createL("L", (string)"link"+link_node->first_attribute("src")->value()+link_node->first_attribute("dst")->value(),
			&n,
			2,
			false,
			linkData,
			is_data_ready,
			send_m[src],
			receive_m[dst]
			);
		msgs_num++;
	}
	cerr << "Num of tasks: " << tasks_num << endl;
	cerr << "Num of msgs: " << msgs_num << endl;
	cerr << "Num of partitions: " << partitions_num << endl;
	cerr << "Num of cores: " << cores_num << endl;
	cerr << "Num of windows: " << windows_num << endl;
}

void print_time(const struct timespec &ts1, const struct timespec &ts2)
{

	struct timespec ts;
	ts.tv_sec = ts2.tv_sec - ts1.tv_sec;
	if (ts2.tv_nsec >= ts1.tv_nsec)
		ts.tv_nsec = ts2.tv_nsec - ts1.tv_nsec;
	else {
		ts.tv_nsec = 1e9 + ts2.tv_nsec - ts1.tv_nsec;
		ts.tv_sec--;
	}
	cerr << ts.tv_sec << "s " << ts.tv_nsec / 1e6 << "ms" << endl;
}

int main(int argc, char* argv[])
{
	if (argc != 2){
		cerr << "Usage: " << argv[0] << " <input.xml>" << endl;
		exit(1);
	}

	Network n;
	struct timespec ts1, ts2, ts3, ts4;
	clock_gettime(CLOCK_REALTIME, &ts1);
	buildNetwork(argv[1], n);
	clock_gettime(CLOCK_REALTIME, &ts2);
	//cerr << "Build: ";
	//print_time(ts1, ts2);
	//exit(1);
	n.run();
	clock_gettime(CLOCK_REALTIME, &ts3);

	rapidxml::xml_document<> doc;
	xml_node<>* res = doc.allocate_node(node_element, "trace");
	for (int i=0; i < n.automata.size(); i++) {
		T::T *t = dynamic_cast <T::T *> (n.automata[i]);
		if (!t)
			continue;
		xml_node<>* task = doc.allocate_node(node_element, "task");
		string s = t->name;
		s.erase(s.find("_"));
		char* id = doc.allocate_string(s.substr(4).c_str());
		char* name = doc.allocate_string(t->name.substr(t->name.find("_")+1).c_str());
    		task->append_attribute(doc.allocate_attribute("id", id));
    		task->append_attribute(doc.allocate_attribute("name", name));
		res->append_node(task);
		int jobNum = 0;
		bool first = true;
		xml_node<>* job;
		for (int j=0; j < t->trace.size(); j++) {
			if (t->trace[j].chan->name().find("exec")==0) {
				if (t->trace[j].time / t->data->period + 1 > jobNum) { 
					jobNum = t->trace[j].time / t->data->period + 1;
					job = doc.allocate_node(node_element, "job");
					char* jobNumStr = doc.allocate_string(to_string(jobNum).c_str());
					job->append_attribute(doc.allocate_attribute("id", jobNumStr));
					first = false;
					task->append_node(job);
				}
				xml_node<>* ev = doc.allocate_node(node_element, "event");
				ev->append_attribute(doc.allocate_attribute("type", "exec"));
				char* timeStr = doc.allocate_string(to_string(t->trace[j].time).c_str());
				ev->append_attribute(doc.allocate_attribute("time", timeStr));
				job->append_node(ev);
			}
			if (t->trace[j].chan->name().find("finished")==0) {
				xml_node<>* ev = doc.allocate_node(node_element, "event");
				ev->append_attribute(doc.allocate_attribute("type", "finished"));
				char* timeStr = doc.allocate_string(to_string(t->trace[j].time).c_str());
				ev->append_attribute(doc.allocate_attribute("time", timeStr));
				job->append_node(ev);
				first = true;
			}
			if (t->trace[j].chan->name().find("preempt")==0) {
				xml_node<>* ev = doc.allocate_node(node_element, "event");
				ev->append_attribute(doc.allocate_attribute("type", "preempt"));
				char* timeStr = doc.allocate_string(to_string(t->trace[j].time).c_str());
				ev->append_attribute(doc.allocate_attribute("time", timeStr));
				job->append_node(ev);
			}
		}
	}
	doc.append_node(res);
	cout << doc;
	clock_gettime(CLOCK_REALTIME, &ts4);
	cerr << "Build: ";
	print_time(ts1, ts2);
	cerr << "Run: ";
	print_time(ts2, ts3);
	cerr << "Write trace: ";
	print_time(ts3, ts4);
	cerr << "All: ";
	print_time(ts1, ts4);
	return 0;
}
