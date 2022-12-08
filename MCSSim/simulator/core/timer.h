#ifndef SIMULATOR_TIMER_H
#define SIMULATOR_TIMER_H

#include <string>
#include <vector>
#include <set>

class Network;

class Timer {
	int value;
	int start; // абсолютное модельное время, в которое был обнулен таймер
	std::set <int> knownPoints;
	Network *net;

	int lastPoint;
public:
	Timer(Network *_net, std::string _name);
	
	bool operator == (int x);
	bool operator < (int x);
	Timer& operator = (int x);	
	void inc(int x);
	operator int() const {return value;}
	void reset();

	bool can_inc() {return true;}

	static void createArray(std::vector<Timer*>&, Network *_net, std::string __name, int size);
};


#endif //SIMULATOR_TIMER_H
