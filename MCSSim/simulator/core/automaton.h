#ifndef SIMULATOR_AUTOMATON_H
#define SIMULATOR_AUTOMATON_H

#include "transition.h"
#include <vector>

class Network;

struct AEvent {
	unsigned int num;
	int time;
	std::string channelName;
	Channel* chan;
	AEvent(unsigned int n, int t, Channel* c): num(n), time(t), chan(c) {}
};

class Automaton {
public:
	std::vector <AEvent> trace; 
	Network *net;
	std::string name;
	std::vector<Location *> locations; //множество состояний
	std::vector<Timer *> timers; //множество состояний
	Location * init; // начальное состояние
	Location * cur; //текущее состояние
	std::vector<Location *> fin;
	int _priority;
	bool needTrace;
	Automaton(Network*, std::string, int, bool);
	void addLocation(Location* st);
	virtual void _start();
	bool step();
	void printTrace();
};


#endif //SIMULATOR_AUTOMATON_H
