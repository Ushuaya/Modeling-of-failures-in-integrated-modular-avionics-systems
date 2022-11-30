#ifndef __EDF__H_
#define __EDF__H_

#include "automaton.h"
#include "common.h"

namespace EDF {

class EDF:public Automaton {
	EDF *automaton;
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



	EDF(std::string _name, Network *n, int p, bool t, TaskSchedulerData* _data, std::vector <Var*> &_abs_deadline, std::vector <Var*> &_is_ready, std::vector <Var*> &_prio, std::vector <Var*> &_id, Channel* _wakeup, Channel* _sleep, Channel* _ready, Channel* _finished, std::vector <Channel*> &_exec, std::vector <Channel*> &_preempt);



int get_job()
{
     int res = -1;
for (int i  = 0; i  <= (*(automaton->data)).numOfTasks-1; i ++) {
        if (*automaton->is_ready[i]) {
            if (res == -1 || (*automaton->abs_deadline[i]<*automaton->abs_deadline[res]))
                res = i;
        }
    }

    if (res == -1)
        return res;

for (int i  = 0; i  <=  (*(automaton->data)).numOfTasks-1; i ++) {
        if (*automaton->is_ready[i]) {
            if ((*automaton->abs_deadline[i] == *automaton->abs_deadline[res]) && (*automaton->id[i] < *automaton->id[res]))
                res = i;
        }
    }
    return res;
}

};


class Preempting_Scheduling_0: public Transition {
	EDF* automaton;
	

public:
	Preempting_Scheduling_0 (Network *_net, Location *_next, EDF *_aut): Transition(_net, _next), automaton(_aut)
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

class SendPreempt_Sleeping_1: public Transition {
	EDF* automaton;
	

public:
	SendPreempt_Sleeping_1 (Network *_net, Location *_next, EDF *_aut): Transition(_net, _next), automaton(_aut)
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

class NewJob_Executing_2: public Transition {
	EDF* automaton;
	

public:
	NewJob_Executing_2 (Network *_net, Location *_next, EDF *_aut): Transition(_net, _next), automaton(_aut) {}

	virtual bool guard()
	{
		return automaton->get_job()==automaton->current;
	}





};

class NewJob_Preempting_3: public Transition {
	EDF* automaton;
	

public:
	NewJob_Preempting_3 (Network *_net, Location *_next, EDF *_aut): Transition(_net, _next), automaton(_aut) {}

	virtual bool guard()
	{
		return automaton->get_job()!=automaton->current;
	}





};

class Scheduling_Waiting_4: public Transition {
	EDF* automaton;
	

public:
	Scheduling_Waiting_4 (Network *_net, Location *_next, EDF *_aut): Transition(_net, _next), automaton(_aut) {}

	virtual bool guard()
	{
		return automaton->get_job()==-1;
	}





};

class Executing_Scheduling_5: public Transition {
	EDF* automaton;
	

public:
	Executing_Scheduling_5 (Network *_net, Location *_next, EDF *_aut): Transition(_net, _next), automaton(_aut)
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

class SendPreempt_Sleeping_6: public Transition {
	EDF* automaton;
	

public:
	SendPreempt_Sleeping_6 (Network *_net, Location *_next, EDF *_aut): Transition(_net, _next), automaton(_aut)
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

class Preempting_Scheduling_7: public Transition {
	EDF* automaton;
	

public:
	Preempting_Scheduling_7 (Network *_net, Location *_next, EDF *_aut): Transition(_net, _next), automaton(_aut)
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

class Waiting_Sleeping_8: public Transition {
	EDF* automaton;
	

public:
	Waiting_Sleeping_8 (Network *_net, Location *_next, EDF *_aut): Transition(_net, _next), automaton(_aut)
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

class Sleeping_Scheduling_9: public Transition {
	EDF* automaton;
	

public:
	Sleeping_Scheduling_9 (Network *_net, Location *_next, EDF *_aut): Transition(_net, _next), automaton(_aut)
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

class Scheduling_Sleeping_10: public Transition {
	EDF* automaton;
	

public:
	Scheduling_Sleeping_10 (Network *_net, Location *_next, EDF *_aut): Transition(_net, _next), automaton(_aut)
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

class Executing_SendPreempt_11: public Transition {
	EDF* automaton;
	

public:
	Executing_SendPreempt_11 (Network *_net, Location *_next, EDF *_aut): Transition(_net, _next), automaton(_aut)
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

class Waiting_Scheduling_12: public Transition {
	EDF* automaton;
	

public:
	Waiting_Scheduling_12 (Network *_net, Location *_next, EDF *_aut): Transition(_net, _next), automaton(_aut)
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

class Sleeping_Sleeping_13: public Transition {
	EDF* automaton;
	

public:
	Sleeping_Sleeping_13 (Network *_net, Location *_next, EDF *_aut): Transition(_net, _next), automaton(_aut)
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

class Scheduling_Scheduling_14: public Transition {
	EDF* automaton;
	

public:
	Scheduling_Scheduling_14 (Network *_net, Location *_next, EDF *_aut): Transition(_net, _next), automaton(_aut)
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

class Executing_NewJob_15: public Transition {
	EDF* automaton;
	

public:
	Executing_NewJob_15 (Network *_net, Location *_next, EDF *_aut): Transition(_net, _next), automaton(_aut)
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

class Scheduling_Executing_16: public Transition {
	EDF* automaton;
	

public:
	Scheduling_Executing_16 (Network *_net, Location *_next, EDF *_aut): Transition(_net, _next), automaton(_aut)
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


class Waiting: public Location {
	EDF* automaton;
public:
	Waiting (Network *n, std::string _name, bool init, bool committed, EDF *a): Location (n, _name, init, committed), automaton(a) {}
};

class Executing: public Location {
	EDF* automaton;
public:
	Executing (Network *n, std::string _name, bool init, bool committed, EDF *a): Location (n, _name, init, committed), automaton(a) {}
};

class Scheduling: public Location {
	EDF* automaton;
public:
	Scheduling (Network *n, std::string _name, bool init, bool committed, EDF *a): Location (n, _name, init, committed), automaton(a) {}
};

class SendPreempt: public Location {
	EDF* automaton;
public:
	SendPreempt (Network *n, std::string _name, bool init, bool committed, EDF *a): Location (n, _name, init, committed), automaton(a) {}
};

class Preempting: public Location {
	EDF* automaton;
public:
	Preempting (Network *n, std::string _name, bool init, bool committed, EDF *a): Location (n, _name, init, committed), automaton(a) {}
};

class NewJob: public Location {
	EDF* automaton;
public:
	NewJob (Network *n, std::string _name, bool init, bool committed, EDF *a): Location (n, _name, init, committed), automaton(a) {}
};

class Sleeping: public Location {
	EDF* automaton;
public:
	Sleeping (Network *n, std::string _name, bool init, bool committed, EDF *a): Location (n, _name, init, committed), automaton(a) {}
};


}

#endif
