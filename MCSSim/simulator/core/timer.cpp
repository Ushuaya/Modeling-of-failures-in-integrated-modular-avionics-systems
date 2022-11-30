#include "timer.h"
#include "network.h"
#include <iostream>

using namespace std;

Timer::Timer(Network *__net, std::string __name):  value(0), start(0), net(__net), lastPoint(0)
{
	__net->addTimer(this);
}

bool Timer::operator == (int x)
{
	int newPoint = net->timeForInternalUse + x - value;
	if (lastPoint!=newPoint /*&& knownPoints.find(newPoint) == knownPoints.end()*/) {
		lastPoint = newPoint;
		net->addPoint(newPoint);
		//knownPoints.insert(newPoint);
	}
	return (value == x);
}

bool Timer::operator < (int x)
{
	int newPoint = net->timeForInternalUse + x - value;
	if (lastPoint!=newPoint /*&& knownPoints.find(newPoint) == knownPoints.end()*/) {
		lastPoint = newPoint;
		net->addPoint(newPoint);
		//knownPoints.insert(newPoint);
	}
	return (value < x);
}

Timer& Timer::operator = (int x)
{
	//knownPoints.clear();
	if (value==x)
		return *this;
	value = x;
	start = net->timeForInternalUse - x;
	return *this;
}

void Timer::inc(int x)
{
	value += x;
}

void Timer::reset() {
	//knownPoints.clear();
	value = 0;
	start = net->timeForInternalUse;
}

void Timer::createArray(vector <Timer*>& v, Network *__net, std::string __name, int size)
{
	for (int i=0; i < size; i++) {
		string name = __name + "[" + to_string(i) + "]";
		v.push_back(new Timer(__net, name));
	}
}
