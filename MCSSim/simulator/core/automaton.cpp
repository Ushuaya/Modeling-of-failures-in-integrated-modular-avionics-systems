#include "automaton.h"
#include <iostream>

using namespace std;

Automaton::Automaton(Network *n, std::string _name, int p, bool t): net(n), name(_name), _priority(p), needTrace(t)
{
	n->addAutomaton(this);
}

void Automaton::addLocation(Location* st)
	{
		locations.push_back(st);
		if (st->is_init)
			init = st;
	}

void Automaton::_start()
{
	cur = init;
}

bool Automaton::step()
{
	//cerr << name << endl;
	//cerr << cur->numOfTransitions << endl;
	//cerr << cur << " " << init << endl;
	for (int i=0; i < cur->numOfTransitions; i++) {
		Transition * t = cur->transitions[i];
		//cerr << name << " " << cur->name << " -> " << t->next->name << " " << (t->guard() && t->next->inv()) << endl;
		if (t->guard() && t->next->inv()) { // если выполнено условие
			if (t->needSync() ) {// если есть действия по синхронизации
				//cerr << "sync start" << endl;
				bool sync = t->synchronize();
				//cerr << "sync fin" << sync << endl;
				if (sync) {
					for (int j=0; j < cur->numOfTransitions; j++) {
						if (i != j)
							cur->transitions[j]->stopSync();
					}
					t->action(); //выполняем действия перехода
					//cerr << "time = " << net->timeForInternalUse << " " << name << ": " << cur->name << " -> " << t->next->name << endl;
					cur = t->next; //изменяем текущее состояние
					if (needTrace)
						trace.push_back(AEvent(net->syncNum, net->timeForInternalUse,t->channel));
					return true; //был совершен переход
				}
			}
			else { // синхронизации нет, условие выполнено
				for (int j=0; j < cur->numOfTransitions; j++) {
					if (i != j)
						cur->transitions[j]->stopSync();
				}

				t->action(); //выполняем действия перехода
				//cerr << "time = " << net->timeForInternalUse << " " << name << ": " << cur->name << " -> " << t->next->name << endl;
				cur = t->next; //изменяем текущее состояние
				return true; //был совершен переход
			}
		}
	}
	return false; //перехода не было
}

void Automaton::printTrace()
{
	for (int i=0; i<trace.size(); i++)
		cerr << name << " " << trace[i].time << " " << trace[i].chan->name() << endl;
}
