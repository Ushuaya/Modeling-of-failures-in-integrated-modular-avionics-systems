//
// Created by user on 22.02.16.
//

#ifndef SIMULATOR_CHANNEL_H
#define SIMULATOR_CHANNEL_H

#include <vector>
#include "network.h"

class Transition;

class Channel {
	std::string _name;
protected:
	Network *net;
public:
	bool isBroadcast;
	bool processing;

	Channel(Network * __net, std::string __name, bool);

	virtual bool processSynchronisation() {return false;}
	virtual bool send(Transition *) = 0;
	virtual bool receive(Transition *) = 0;
	virtual void stopSend(Transition *) = 0;
	virtual void stopReceive(Transition *) = 0;
	std::string& name() {return _name;}
};

class DuplexChannel: public Channel {
	bool rcv_req;
	bool snd_req;
public:
	DuplexChannel(Network * __net, std::string __name);
	virtual bool send(Transition *t)
	{
	//	std::cerr << _name << " send" << std::endl;
	if (!processing)
		snd_req = true;
	if (rcv_req) {
		processing=true;
		rcv_req=false;
		if (!snd_req)
			processing=false;
		net->syncNum++;
		return true;
	}
	return false;
	}

	virtual bool receive(Transition *t)
	{
		//std::cerr << _name << " receive" << std::endl;
	if (!processing)
		rcv_req = true;
	if (snd_req) {
		processing=true;
		snd_req=false;
		if (!rcv_req)
			processing=false;
		return true;
	}
	return false;
	}

	virtual void stopSend(Transition *t) {
		processing = false;
		snd_req = false;
	}

	virtual void stopReceive(Transition *t) {
		processing = false;
		rcv_req = false;
	}


};

class BroadcastChannel: public Channel {
public:
	Transition* snd_request;
	std::vector<Transition *> rcv_requests;
	BroadcastChannel(Network * __net, std::string __name);
	virtual bool processSynchronisation();
	virtual bool send(Transition *);
	virtual bool receive(Transition *);
	virtual void stopSend(Transition *);
	virtual void stopReceive(Transition *);

};

#endif //SIMULATOR_CHANNEL_H
