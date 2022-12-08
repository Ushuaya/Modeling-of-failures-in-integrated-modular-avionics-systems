#ifndef __T__H_
#define __T__H_

#include "automaton.h"
#include "common.h"

namespace T {

class T:public Automaton {
	T *automaton;
public:
	TaskData* data;

	Var* abs_deadline;
	Var* is_ready;
	Var* prio;

	std::vector <Var*> &is_data_ready;


	Channel* exec;
	Channel* preempt;
	Channel* ready;
	Channel* finished;
	Channel* send;
	Channel* receive;






	Timer exec_timer;
	Timer local_timer;


	T(std::string _name, Network *n, int p, bool t, TaskData* _data, Var* _abs_deadline, Var* _is_ready, Var* _prio, std::vector <Var*> &_is_data_ready, Channel* _exec, Channel* _preempt, Channel* _ready, Channel* _finished, Channel* _send, Channel* _receive);

// Place local declarations here.



bool allDataReady()
{
for (int i = 0; i <=  DUMMY_NUM-1; i++) {
        if (i>=(*(automaton->data)).numOfInputLinks)
            return true;
        if (!*automaton->is_data_ready[i])
            return false;

    }
    return true;
}

void getData()
{
for (int i = 0; i <=  DUMMY_NUM-1; i++) {
        if (i>=(*(automaton->data)).numOfInputLinks)
            return;
        *automaton->is_data_ready[i] = 0;
    }
}

void resetData()
{
for (int i = 0; i <=  DUMMY_NUM-1; i++) {
        if (i>=(*(automaton->data)).numOfInputLinks)
            return;
        *automaton->is_data_ready[i] = 0;
    }
}

};


class Start_Dormant_0: public Transition {
	T* automaton;
	

public:
	Start_Dormant_0 (Network *_net, Location *_next, T *_aut): Transition(_net, _next), automaton(_aut) {}

	virtual bool guard()
	{
		return (*(automaton->data)).deadline != 0;
	}



	virtual void action()
	{
		(*(automaton->abs_deadline)) = (*(automaton->data)).deadline;
	}


};

class WaitingForData_WaitingForData_1: public Transition {
	T* automaton;
	

public:
	WaitingForData_WaitingForData_1 (Network *_net, Location *_next, T *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = false;
	}

	virtual bool guard()
	{
		return automaton->local_timer==0;
	}



	virtual void action()
	{
		automaton->resetData();
	}

	virtual bool synchronize()
	{
		channel = &((*(automaton->receive)));
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};

class Dormant_Dormant_2: public Transition {
	T* automaton;
	

public:
	Dormant_Dormant_2 (Network *_net, Location *_next, T *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = false;
	}

	virtual bool guard()
	{
		return automaton->local_timer==0;
	}



	virtual void action()
	{
		automaton->resetData();
	}

	virtual bool synchronize()
	{
		channel = &((*(automaton->receive)));
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};

class WaitingForNewPeriod_Dormant_3: public Transition {
	T* automaton;
	

public:
	WaitingForNewPeriod_Dormant_3 (Network *_net, Location *_next, T *_aut): Transition(_net, _next), automaton(_aut) {}

	virtual bool guard()
	{
		return automaton->local_timer==(*(automaton->data)).period;
	}



	virtual void action()
	{
		automaton->local_timer=0, automaton->exec_timer=0,automaton->resetData(),
(*(automaton->abs_deadline))=(*(automaton->abs_deadline))+(*(automaton->data)).period;
	}


};

class Exec_Finished_4: public Transition {
	T* automaton;
	

public:
	Exec_Finished_4 (Network *_net, Location *_next, T *_aut): Transition(_net, _next), automaton(_aut) {}

	virtual bool guard()
	{
		return automaton->local_timer==(*(automaton->data)).deadline && automaton->exec_timer < (*(automaton->data)).wcet;
	}





};

class Send_Finished_5: public Transition {
	T* automaton;
	

public:
	Send_Finished_5 (Network *_net, Location *_next, T *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = true;
	}





	virtual bool synchronize()
	{
		channel = &((*(automaton->send)));
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};

class Exec_Send_6: public Transition {
	T* automaton;
	

public:
	Exec_Send_6 (Network *_net, Location *_next, T *_aut): Transition(_net, _next), automaton(_aut) {}

	virtual bool guard()
	{
		return automaton->exec_timer==(*(automaton->data)).wcet;
	}





};

class WaitingForData_WaitingForNewPeriod_7: public Transition {
	T* automaton;
	

public:
	WaitingForData_WaitingForNewPeriod_7 (Network *_net, Location *_next, T *_aut): Transition(_net, _next), automaton(_aut) {}

	virtual bool guard()
	{
		return automaton->local_timer==(*(automaton->data)).deadline;
	}



	virtual void action()
	{
		(*(automaton->is_ready))=0;
	}


};

class Ready_WaitingForNewPeriod_8: public Transition {
	T* automaton;
	

public:
	Ready_WaitingForNewPeriod_8 (Network *_net, Location *_next, T *_aut): Transition(_net, _next), automaton(_aut) {}

	virtual bool guard()
	{
		return automaton->local_timer==
(*(automaton->data)).deadline;
	}



	virtual void action()
	{
		(*(automaton->is_ready))=0;
	}


};

class WaitingForData_SendReadySig_9: public Transition {
	T* automaton;
	

public:
	WaitingForData_SendReadySig_9 (Network *_net, Location *_next, T *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = false;
	}

	virtual bool guard()
	{
		return automaton->allDataReady()&&
automaton->local_timer<(*(automaton->data)).deadline
&&automaton->local_timer>0;
	}



	virtual void action()
	{
		(*(automaton->is_ready))=1;
	}

	virtual bool synchronize()
	{
		channel = &((*(automaton->receive)));
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};

class WaitingForData_WaitingForData_10: public Transition {
	T* automaton;
	

public:
	WaitingForData_WaitingForData_10 (Network *_net, Location *_next, T *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = false;
	}

	virtual bool guard()
	{
		return !automaton->allDataReady()&&
automaton->local_timer>0;
	}




	virtual bool synchronize()
	{
		channel = &((*(automaton->receive)));
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};

class Dormant_WaitingForData_11: public Transition {
	T* automaton;
	

public:
	Dormant_WaitingForData_11 (Network *_net, Location *_next, T *_aut): Transition(_net, _next), automaton(_aut) {}

	virtual bool guard()
	{
		return automaton->local_timer==(*(automaton->data)).offset
&&!automaton->allDataReady();
	}





};

class Finished_WaitingForNewPeriod_12: public Transition {
	T* automaton;
	

public:
	Finished_WaitingForNewPeriod_12 (Network *_net, Location *_next, T *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = true;
	}




	virtual void action()
	{
		(*(automaton->is_ready))=0;
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

class Exec_Ready_13: public Transition {
	T* automaton;
	

public:
	Exec_Ready_13 (Network *_net, Location *_next, T *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = false;
	}





	virtual bool synchronize()
	{
		channel = &((*(automaton->preempt)));
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};

class Ready_Exec_14: public Transition {
	T* automaton;
	

public:
	Ready_Exec_14 (Network *_net, Location *_next, T *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = false;
	}

	virtual bool guard()
	{
		return automaton->local_timer<(*(automaton->data)).deadline;
	}




	virtual bool synchronize()
	{
		channel = &((*(automaton->exec)));
		return Transition::synchronize();
	}

	virtual bool needSync()
	{
		return true;
	}

};

class SendReadySig_Ready_15: public Transition {
	T* automaton;
	

public:
	SendReadySig_Ready_15 (Network *_net, Location *_next, T *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = true;
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

class Dormant_SendReadySig_16: public Transition {
	T* automaton;
	

public:
	Dormant_SendReadySig_16 (Network *_net, Location *_next, T *_aut): Transition(_net, _next), automaton(_aut) {}

	virtual bool guard()
	{
		return automaton->local_timer==(*(automaton->data)).offset
&&automaton->allDataReady();
	}



	virtual void action()
	{
		(*(automaton->is_ready))=1;
	}


};


class Dormant: public Location {
	T* automaton;
public:
	Dormant (Network *n, std::string _name, bool init, bool committed, T *a): Location (n, _name, init, committed), automaton(a) {}
	virtual bool checkTimer(Timer *__t)
	{
		if ( __t == &(automaton->exec_timer))
			return 0;
		return true;
	}
};

class Ready: public Location {
	T* automaton;
public:
	Ready (Network *n, std::string _name, bool init, bool committed, T *a): Location (n, _name, init, committed), automaton(a) {}
	virtual bool checkTimer(Timer *__t)
	{
		if ( __t == &(automaton->exec_timer))
			return 0;
		return true;
	}
};

class SendReadySig: public Location {
	T* automaton;
public:
	SendReadySig (Network *n, std::string _name, bool init, bool committed, T *a): Location (n, _name, init, committed), automaton(a) {}
};

class Finished: public Location {
	T* automaton;
public:
	Finished (Network *n, std::string _name, bool init, bool committed, T *a): Location (n, _name, init, committed), automaton(a) {}
};

class Exec: public Location {
	T* automaton;
public:
	Exec (Network *n, std::string _name, bool init, bool committed, T *a): Location (n, _name, init, committed), automaton(a) {}
};

class WaitingForData: public Location {
	T* automaton;
public:
	WaitingForData (Network *n, std::string _name, bool init, bool committed, T *a): Location (n, _name, init, committed), automaton(a) {}
	virtual bool checkTimer(Timer *__t)
	{
		if ( __t == &(automaton->exec_timer))
			return 0;
		return true;
	}
};

class WaitingForNewPeriod: public Location {
	T* automaton;
public:
	WaitingForNewPeriod (Network *n, std::string _name, bool init, bool committed, T *a): Location (n, _name, init, committed), automaton(a) {}
	virtual bool checkTimer(Timer *__t)
	{
		if ( __t == &(automaton->exec_timer))
			return 0;
		return true;
	}
};

class Start: public Location {
	T* automaton;
public:
	Start (Network *n, std::string _name, bool init, bool committed, T *a): Location (n, _name, init, committed), automaton(a) {}
};

class Send: public Location {
	T* automaton;
public:
	Send (Network *n, std::string _name, bool init, bool committed, T *a): Location (n, _name, init, committed), automaton(a) {}
};


}

#endif
