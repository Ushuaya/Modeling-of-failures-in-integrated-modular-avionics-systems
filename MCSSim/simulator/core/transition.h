#ifndef SIMULATOR_TRANSITION_H
#define SIMULATOR_TRANSITION_H

#include "location.h"
#include "channel.h"
#include <iostream>

class Network;

class Transition {
public:
	Network *net;
	Location *next; //состояние, в которое ведет переход
	virtual void action() {} //действие
	virtual bool guard() {return true;} //условие
	virtual bool synchronize()
	{
		if (is_sender)
			return channel->send(this);
		else
			return channel->receive(this);
	}
	void stopSync()
	{
		if (!channel)
			return;
		if (is_sender)
			channel->stopSend(this);
		else
			channel->stopReceive(this);
	}
	
	Channel *channel;
	bool is_sender;
	bool canSync;
	virtual bool needSync() {return false;}
	Transition(Network *_net, Location *_next): net(_net), next(_next), channel(NULL), is_sender(false), canSync(false) {}
};


#endif //SIMULATOR_TRANSITION_H
