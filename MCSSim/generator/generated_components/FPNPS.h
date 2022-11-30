#ifndef __FPNPS__H_
#define __FPNPS__H_

#include "automaton.h"
#include "common.h"

namespace FPNPS {

class FPNPS:public Automaton {
	FPNPS *automaton;
public:
	TaskSchedulerData* data;


	std::vector <Var*> &abs_deadline;
	std::vector <Var*> &is_ready;
	std::vector <Var*> &prio;
	std::vector <Var*> &id;


	Channel* wakeup;
	Channel* sleep;
	Channel* ready;
	Channel* finished;

	std::vector <Channel*> &exec;
	std::vector <Channel*> &preempt;




	Var current;



	FPNPS(std::string _name, Network *n, int p, bool t, TaskSchedulerData* _data, std::vector <Var*> &_abs_deadline, std::vector <Var*> &_is_ready, std::vector <Var*> &_prio, std::vector <Var*> &_id, Channel* _wakeup, Channel* _sleep, Channel* _ready, Channel* _finished, std::vector <Channel*> &_exec, std::vector <Channel*> &_preempt);

//bool needRescheduling;


int get_job()
{
     int res = -1;
for (int i  = 0; i  <= (*(automaton->data)).numOfTasks-1; i ++) {
        if (*automaton->is_ready[i]) {
            if (res == -1 || (*automaton->prio[i]>*automaton->prio[res]))
                res = i;
        }
    }
    return res;
}

};


class SendPreempt_Sleeping_0: public Transition {
	FPNPS* automaton;
	

public:
	SendPreempt_Sleeping_0 (Network *_net, Location *_next, FPNPS *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = false;
	}





	virtual bool synchronize()
	{
		channel = &((*(automaton->finished)));
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};

class Executing_Executing_1: public Transition {
	FPNPS* automaton;
	

public:
	Executing_Executing_1 (Network *_net, Location *_next, FPNPS *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = false;
	}





	virtual bool synchronize()
	{
		channel = &((*(automaton->ready)));
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};

class Waiting_Scheduling_2: public Transition {
	FPNPS* automaton;
	

public:
	Waiting_Scheduling_2 (Network *_net, Location *_next, FPNPS *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = false;
	}





	virtual bool synchronize()
	{
		channel = &((*(automaton->ready)));
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};

class Sleeping_Sleeping_3: public Transition {
	FPNPS* automaton;
	

public:
	Sleeping_Sleeping_3 (Network *_net, Location *_next, FPNPS *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = false;
	}





	virtual bool synchronize()
	{
		channel = &((*(automaton->ready)));
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};

class Waiting_Sleeping_4: public Transition {
	FPNPS* automaton;
	

public:
	Waiting_Sleeping_4 (Network *_net, Location *_next, FPNPS *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = false;
	}





	virtual bool synchronize()
	{
		channel = &((*(automaton->sleep)));
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};

class Executing_Scheduling_5: public Transition {
	FPNPS* automaton;
	

public:
	Executing_Scheduling_5 (Network *_net, Location *_next, FPNPS *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = false;
	}





	virtual bool synchronize()
	{
		channel = &((*(automaton->finished)));
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};

class Sleeping_Scheduling_6: public Transition {
	FPNPS* automaton;
	

public:
	Sleeping_Scheduling_6 (Network *_net, Location *_next, FPNPS *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = false;
	}





	virtual bool synchronize()
	{
		channel = &((*(automaton->wakeup)));
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};

class Scheduling_Sleeping_7: public Transition {
	FPNPS* automaton;
	

public:
	Scheduling_Sleeping_7 (Network *_net, Location *_next, FPNPS *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = false;
	}





	virtual bool synchronize()
	{
		channel = &((*(automaton->sleep)));
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};

class Scheduling_Scheduling_8: public Transition {
	FPNPS* automaton;
	

public:
	Scheduling_Scheduling_8 (Network *_net, Location *_next, FPNPS *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = false;
	}





	virtual bool synchronize()
	{
		channel = &((*(automaton->ready)));
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};

class SendPreempt_Sleeping_9: public Transition {
	FPNPS* automaton;
	

public:
	SendPreempt_Sleeping_9 (Network *_net, Location *_next, FPNPS *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = true;
	}





	virtual bool synchronize()
	{
		channel = &(*automaton->preempt[automaton->current]);
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};

class Executing_SendPreempt_10: public Transition {
	FPNPS* automaton;
	

public:
	Executing_SendPreempt_10 (Network *_net, Location *_next, FPNPS *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = false;
	}





	virtual bool synchronize()
	{
		channel = &((*(automaton->sleep)));
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};

class Scheduling_Executing_11: public Transition {
	FPNPS* automaton;
	

public:
	Scheduling_Executing_11 (Network *_net, Location *_next, FPNPS *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = true;
	}

	virtual bool guard()
	{
		return automaton->get_job()!=-1;
	}



	virtual void action()
	{
		automaton->current=automaton->get_job();
	}

	virtual bool synchronize()
	{
		channel = &(*automaton->exec[automaton->get_job()]);
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};

class Scheduling_Waiting_12: public Transition {
	FPNPS* automaton;
	

public:
	Scheduling_Waiting_12 (Network *_net, Location *_next, FPNPS *_aut): Transition(_net, _next), automaton(_aut) {}

	virtual bool guard()
	{
		return automaton->get_job()==-1;
	}





};


class Waiting: public Location {
	FPNPS* automaton;
public:
	Waiting (Network *n, std::string _name, bool init, bool committed, FPNPS *a): Location (n, _name, init, committed), automaton(a) {}
};

class Executing: public Location {
	FPNPS* automaton;
public:
	Executing (Network *n, std::string _name, bool init, bool committed, FPNPS *a): Location (n, _name, init, committed), automaton(a) {}
};

class Scheduling: public Location {
	FPNPS* automaton;
public:
	Scheduling (Network *n, std::string _name, bool init, bool committed, FPNPS *a): Location (n, _name, init, committed), automaton(a) {}
};

class Sleeping: public Location {
	FPNPS* automaton;
public:
	Sleeping (Network *n, std::string _name, bool init, bool committed, FPNPS *a): Location (n, _name, init, committed), automaton(a) {}
};

class SendPreempt: public Location {
	FPNPS* automaton;
public:
	SendPreempt (Network *n, std::string _name, bool init, bool committed, FPNPS *a): Location (n, _name, init, committed), automaton(a) {}
};


}

#endif
