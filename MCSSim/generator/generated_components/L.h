#ifndef __L__H_
#define __L__H_

#include "automaton.h"
#include "common.h"

namespace L {

class L:public Automaton {
	L *automaton;
public:
	LinkData* data;

	Var* is_data_ready;



	Channel* send;
	Channel* receive;






	Timer transfer_time;


	L(std::string _name, Network *n, int p, bool t, LinkData* _data, Var* _is_data_ready, Channel* _send, Channel* _receive);



};


class Delivery_Idle_0: public Transition {
	L* automaton;
	

public:
	Delivery_Idle_0 (Network *_net, Location *_next, L *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = true;
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

class Busy_Delivery_1: public Transition {
	L* automaton;
	

public:
	Busy_Delivery_1 (Network *_net, Location *_next, L *_aut): Transition(_net, _next), automaton(_aut) {}

	virtual bool guard()
	{
		return automaton->transfer_time==(*(automaton->data)).delay;
	}



	virtual void action()
	{
		(*(automaton->is_data_ready))=1;
	}


};

class Idle_Busy_2: public Transition {
	L* automaton;
	

public:
	Idle_Busy_2 (Network *_net, Location *_next, L *_aut): Transition(_net, _next), automaton(_aut)
	{
		is_sender = false;
	}

	virtual bool guard()
	{
		return !(*(automaton->is_data_ready));
	}



	virtual void action()
	{
		automaton->transfer_time=0;
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


class Idle: public Location {
	L* automaton;
public:
	Idle (Network *n, std::string _name, bool init, bool committed, L *a): Location (n, _name, init, committed), automaton(a) {}
	virtual bool checkTimer(Timer *__t)
	{
		if ( __t == &(automaton->transfer_time))
			return 0;
		return true;
	}
};

class Delivery: public Location {
	L* automaton;
public:
	Delivery (Network *n, std::string _name, bool init, bool committed, L *a): Location (n, _name, init, committed), automaton(a) {}
};

class Busy: public Location {
	L* automaton;
public:
	Busy (Network *n, std::string _name, bool init, bool committed, L *a): Location (n, _name, init, committed), automaton(a) {}
	virtual bool checkTimer(Timer *__t)
	{
		if ( __t == &(automaton->transfer_time))
			return 1;
		return true;
	}
};


}

#endif
