#ifndef SIMULATOR_NETWORK_H
#define SIMULATOR_NETWORK_H

#include "timer.h"
#include "var.h"
#include <vector>
#include <set>
#include <map>
#include <unistd.h>

class Channel;
class ArrayChannel;
class Automaton;

struct NetEvent {
	Channel *chan;
	int time;
	std::vector<Automaton *> automata;
};

class Network {
public:
	unsigned int syncNum;
	std::vector<Automaton *> automata;
	int numOfAutomata;
	std::multimap<int, Automaton *> automata_map;
	std::set<int> points;
	int lastPoint;
	int timeForInternalUse;
	int simulationInterval;
	std::map<int, NetEvent *> trace;


	std::vector<Channel *> channels;
	int numOfChannelsSync;
	std::vector<Channel *> channels_sync;
	void addChannel(Channel *);

	std::vector<Var *> vars;
	void addVar(Var *);

	std::vector<Timer *> timers;
	void addTimer(Timer*);

	int steps;

	Network(): syncNum(0), numOfAutomata(0), lastPoint(-1), timeForInternalUse(0), simulationInterval(0), numOfChannelsSync(0), steps(0) {}

	void addAutomaton(Automaton *a);

	void addPoint(int p);

	int getPoint();

	bool step(); //возвращает true, если текущее состояние не конечное

	void run();

	void buildTD();

	void setSimulationInterval(int t) {simulationInterval = t;} 
};


#endif //SIMULATOR_NETWORK_H
