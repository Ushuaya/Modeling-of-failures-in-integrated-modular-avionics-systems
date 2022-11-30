#include "L.h"

using namespace std;

namespace L {

L::L(string _name, Network *n, int p, bool __t, LinkData* _data, Var* _is_data_ready
, Channel* _send, Channel* _receive
): Automaton(n, _name, p, __t), data(_data), is_data_ready(_is_data_ready), send(_send), receive(_receive), transfer_time(n, "L_transfer_time")


{
	Idle* idle = new Idle (n, "Idle", true, false, this);
	addLocation(idle);
	Delivery* delivery = new Delivery (n, "Delivery", false, true, this);
	addLocation(delivery);
	Busy* busy = new Busy (n, "Busy", false, false, this);
	addLocation(busy);

	Delivery_Idle_0 *delivery_idle_0 = new Delivery_Idle_0 (n, idle, this);
	delivery->addTransition(delivery_idle_0);
	Busy_Delivery_1 *busy_delivery_1 = new Busy_Delivery_1 (n, delivery, this);
	busy->addTransition(busy_delivery_1);
	Idle_Busy_2 *idle_busy_2 = new Idle_Busy_2 (n, busy, this);
	idle->addTransition(idle_busy_2);

	automaton = this;
	automaton->timers.push_back(&transfer_time);


}

}

