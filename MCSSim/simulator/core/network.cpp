#include "network.h"
#include "automaton.h"
#include <iostream>

using namespace std;

void Network::addAutomaton(Automaton *a)
{
	automata_map.insert(pair <int, Automaton*> (a->_priority, a));
}

void Network::addPoint(int p)
{
	if (p != lastPoint && p > timeForInternalUse && p <= simulationInterval){
	//if (p > timeForInternalUse && p <= 200){
		lastPoint = p;
		points.insert(p);
	}
}

int Network::getPoint()
{
	if (points.empty()) {
		return -1;
	}
	int p = *points.begin();
	points.erase(p);
	return p;
}

void Network::addChannel(Channel *ch)
{
	channels.push_back(ch);
	if (ch->isBroadcast) {
		channels_sync.push_back(ch);
		numOfChannelsSync++;
	}
}

void Network::addVar(Var *v)
{
	vars.push_back(v);
}

void Network::addTimer(Timer *t)
{
	timers.push_back(t);
}


bool Network::step() { //возвращает true, если текущее состояние не конечное
	//cerr << "Step" << endl;
	bool was_transition = false;
	bool committed = false;
	for (int i=0; i < numOfAutomata; i++) {
		Automaton *a = automata[i];
		if ( a->step() ) {
			was_transition = true;
		}
		if (a->cur->isCommitted()) {
			committed = true;
			//cerr << automata[i]->cur->name << " in automaton " <<  automata[i]->name << endl;
		}
	}

	for (int i=0; i<numOfChannelsSync; ++i)
	{
		bool f = channels_sync[i]->processSynchronisation();
		was_transition = was_transition || f;
	}
	
	//if (was_transition) cerr << "was Step" << endl;
	//else cerr << "no Step" << endl;
	if (!was_transition) {// ни одного перехода не было
		if (committed) {
			cerr << "Trying to move time in committed location " << /*automata[i]->cur->name << " in automaton " <<  automata[i]->name <<*/ " at time " << timeForInternalUse << endl;
			return false;
		}

		int t = getPoint();
		//cerr << "Time: " << t << endl;
		if (t==-1) {
			std::cout << "Error!" << std::endl;
			cout.flush();
			return false;
		}
		for (int i=0; i < numOfAutomata; i++) {
			Automaton *a = automata[i];
			for (int j=0; j<a->timers.size();j++)
				if (a->cur->checkTimer(a->timers[j]))
					a->timers[j]->inc(t-timeForInternalUse);
		}
		/*for (int i=0; i<timers.size(); i++) {
			bool can_inc = true;
			for (int j=0; j < automata.size(); j++) {
				if (!automata[j]->cur->checkTimer(timers[i])) {
					can_inc = false;
					break;
				}
			}
			if (can_inc)
				timers[i]->inc(t-timeForInternalUse);
		}*/
		timeForInternalUse = t;
		steps++;

		if (timeForInternalUse >= simulationInterval) {
		//if (timeForInternalUse >= 200) {
			cout.flush();
			cerr << "steps = " << steps << endl;
			return false;
		}
	}
	return true;
}

void Network::run()
{
	syncNum = 0;
	for (multimap<int, Automaton*>::iterator it = automata_map.begin(); it!=automata_map.end(); ++it) {
		automata.push_back(it->second);
	}
	numOfAutomata = automata.size();
	for (int i=0; i < automata.size(); i++)
		automata[i]->_start();
	int stepNum = 0;
	do{
	} while (step());
}

void Network::buildTD()
{
	for (auto it = automata.begin(); it != automata.end(); ++it) {
		for (auto it1 = (*it)->trace.begin(); it1 !=  (*it)->trace.end(); ++it1) {
			if (trace.find(it1->num) != trace.end())
				trace[it1->num]->automata.push_back(*it);
			else {
				trace[it1->num] = new NetEvent;
				trace[it1->num]->automata.push_back(*it);
				trace[it1->num]->chan = it1->chan;
				trace[it1->num]->time = it1->time;
			}

		}
	}
}
