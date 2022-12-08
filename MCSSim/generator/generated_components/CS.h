#ifndef __CS__H_
#define __CS__H_

#include "automaton.h"
#include "common.h"

namespace CS {

class CS:public Automaton {
	CS *automaton;
public:
	CoreSchedulerData* data;





	std::vector <Channel*> &wakeup;
	std::vector <Channel*> &sleep;




	Var current_window;
	Var last_window;
	Var current_partition;

	Timer time;


	CS(std::string _name, Network *n, int p, bool t, CoreSchedulerData* _data, std::vector <Channel*> &_wakeup, std::vector <Channel*> &_sleep);






void next()
{
    if (automaton->current_window == (*(automaton->data)).numOfWindows-1) {
        automaton->current_window=0;
        automaton->time=0;
    } else {
        automaton->current_window=automaton->current_window+1;
    }
    if (automaton->current_window == (*(automaton->data)).numOfWindows-1) {
        automaton->last_window=1;
    } else {
        automaton->last_window=0;
    }
}

void start()
{
    automaton->current_window=0;
    if (automaton->current_window == (*(automaton->data)).numOfWindows-1)
        automaton->last_window=1;
    else
        automaton->last_window=0;
}



};


class Init_GetPartition_0: public Transition {
	CS* automaton;
	

public:
	Init_GetPartition_0 (Network *_net, Location *_next, CS *_aut): Transition(_net, _next), automaton(_aut) {}




	virtual void action()
	{
		automaton->start();
	}


};

class Stop_Next_1: public Transition {
	CS* automaton;
	

public:
	Stop_Next_1 (Network *_net, Location *_next, CS *_aut): Transition(_net, _next), automaton(_aut) {}

	virtual bool guard()
	{
		return automaton->last_window==0;
	}





};

class WaitForNewFrame_Next_2: public Transition {
	CS* automaton;
	

public:
	WaitForNewFrame_Next_2 (Network *_net, Location *_next, CS *_aut): Transition(_net, _next), automaton(_aut) {}

	virtual bool guard()
	{
		return automaton->time == (*(automaton->data)).majorFrame;
	}





};

class Stop_WaitForNewFrame_3: public Transition {
	CS* automaton;
	

public:
	Stop_WaitForNewFrame_3 (Network *_net, Location *_next, CS *_aut): Transition(_net, _next), automaton(_aut) {}

	virtual bool guard()
	{
		return automaton->last_window==1;
	}





};

class Next_GetPartition_4: public Transition {
	CS* automaton;
	

public:
	Next_GetPartition_4 (Network *_net, Location *_next, CS *_aut): Transition(_net, _next), automaton(_aut) {}




	virtual void action()
	{
		automaton->next();
	}


};

class GetPartition_PreActive_5: public Transition {
	CS* automaton;
	

public:
	GetPartition_PreActive_5 (Network *_net, Location *_next, CS *_aut): Transition(_net, _next), automaton(_aut) {}




	virtual void action()
	{
		automaton->current_partition =
(*(automaton->data)).windows[automaton->current_window].partitionId;
	}


};

class Active_Stop_6: public Transition {
	CS* automaton;
	

public:
	Active_Stop_6 (Network *_net, Location *_next, CS *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = true;
	}

	virtual bool guard()
	{
		return automaton->time ==
(*(automaton->data)).windows[automaton->current_window].stop;
	}




	virtual bool synchronize()
	{
		channel = &(*automaton->sleep[automaton->current_partition]);
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};

class PreActive_Active_7: public Transition {
	CS* automaton;
	

public:
	PreActive_Active_7 (Network *_net, Location *_next, CS *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = true;
	}

	virtual bool guard()
	{
		return automaton->time ==
(*(automaton->data)).windows[automaton->current_window].start;
	}




	virtual bool synchronize()
	{
		channel = &(*automaton->wakeup[automaton->current_partition]);
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};


class PreActive: public Location {
	CS* automaton;
public:
	PreActive (Network *n, std::string _name, bool init, bool committed, CS *a): Location (n, _name, init, committed), automaton(a) {}
};

class WaitForNewFrame: public Location {
	CS* automaton;
public:
	WaitForNewFrame (Network *n, std::string _name, bool init, bool committed, CS *a): Location (n, _name, init, committed), automaton(a) {}
};

class Active: public Location {
	CS* automaton;
public:
	Active (Network *n, std::string _name, bool init, bool committed, CS *a): Location (n, _name, init, committed), automaton(a) {}
};

class Stop: public Location {
	CS* automaton;
public:
	Stop (Network *n, std::string _name, bool init, bool committed, CS *a): Location (n, _name, init, committed), automaton(a) {}
};

class Next: public Location {
	CS* automaton;
public:
	Next (Network *n, std::string _name, bool init, bool committed, CS *a): Location (n, _name, init, committed), automaton(a) {}
};

class Init: public Location {
	CS* automaton;
public:
	Init (Network *n, std::string _name, bool init, bool committed, CS *a): Location (n, _name, init, committed), automaton(a) {}
};

class GetPartition: public Location {
	CS* automaton;
public:
	GetPartition (Network *n, std::string _name, bool init, bool committed, CS *a): Location (n, _name, init, committed), automaton(a) {}
};


}

#endif
