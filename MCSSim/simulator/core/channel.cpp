#include "channel.h"
#include "transition.h"

using namespace std;

Channel::Channel(Network * __net, std::string __name, bool b) : net(__net), _name(__name), isBroadcast(b), processing(false) {
	__net->addChannel(this);
}

DuplexChannel::DuplexChannel(Network * __net, std::string __name): Channel(__net,__name, false), snd_req(false), rcv_req(false)
{
}

BroadcastChannel::BroadcastChannel(Network * __net, std::string __name): Channel(__net,__name, true), snd_request(NULL) 
{
}



bool BroadcastChannel::processSynchronisation()
{
	if (snd_request) {
		for (int i=0; i<rcv_requests.size(); i++)
			rcv_requests[i]->canSync = true;
		snd_request->canSync=true;
		snd_request=NULL;
		return true;
	}
	rcv_requests.clear();
	processing = false;
	return false;
}

bool BroadcastChannel::send(Transition *t)
{
	if (t->canSync) { //Второй проход
		t->canSync = false;
		net->syncNum++;
		return true;
	}
	if (processing)
		return false;
	snd_request = t;
	processing = true;
	return false;
}

bool BroadcastChannel::receive(Transition *t)
{
	if (t->canSync) { //Второй проход
		t->canSync = false;
		return true;
	}
	// первый проход
	rcv_requests.push_back(t);
	return false;
}

void BroadcastChannel::stopSend(Transition *t)
{
	snd_request = NULL;
	processing = false;
	t->canSync = false;
}

void BroadcastChannel::stopReceive(Transition *t)
{
	rcv_requests.clear();
	processing = false;
	t->canSync = false;

}
