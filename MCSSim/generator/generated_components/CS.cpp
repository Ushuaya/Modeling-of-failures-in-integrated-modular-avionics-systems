#include "CS.h"

using namespace std;

namespace CS {

CS::CS(string _name, Network *n, int p, bool __t, CoreSchedulerData* _data
, vector <Channel*> &_wakeup, vector <Channel*> &_sleep
): Automaton(n, _name, p, __t), data(_data), wakeup(_wakeup), sleep(_sleep), current_window(n, "CS_current_window"), last_window(n, "CS_last_window"), current_partition(n, "CS_current_partition"), time(n, "CS_time")


{
	PreActive* preactive = new PreActive (n, "PreActive", false, false, this);
	addLocation(preactive);
	WaitForNewFrame* waitfornewframe = new WaitForNewFrame (n, "WaitForNewFrame", false, false, this);
	addLocation(waitfornewframe);
	Active* active = new Active (n, "Active", false, false, this);
	addLocation(active);
	Stop* stop = new Stop (n, "Stop", false, true, this);
	addLocation(stop);
	Next* next = new Next (n, "Next", false, true, this);
	addLocation(next);
	Init* init = new Init (n, "Init", true, true, this);
	addLocation(init);
	GetPartition* getpartition = new GetPartition (n, "GetPartition", false, true, this);
	addLocation(getpartition);

	Init_GetPartition_0 *init_getpartition_0 = new Init_GetPartition_0 (n, getpartition, this);
	init->addTransition(init_getpartition_0);
	Stop_Next_1 *stop_next_1 = new Stop_Next_1 (n, next, this);
	stop->addTransition(stop_next_1);
	WaitForNewFrame_Next_2 *waitfornewframe_next_2 = new WaitForNewFrame_Next_2 (n, next, this);
	waitfornewframe->addTransition(waitfornewframe_next_2);
	Stop_WaitForNewFrame_3 *stop_waitfornewframe_3 = new Stop_WaitForNewFrame_3 (n, waitfornewframe, this);
	stop->addTransition(stop_waitfornewframe_3);
	Next_GetPartition_4 *next_getpartition_4 = new Next_GetPartition_4 (n, getpartition, this);
	next->addTransition(next_getpartition_4);
	GetPartition_PreActive_5 *getpartition_preactive_5 = new GetPartition_PreActive_5 (n, preactive, this);
	getpartition->addTransition(getpartition_preactive_5);
	Active_Stop_6 *active_stop_6 = new Active_Stop_6 (n, stop, this);
	active->addTransition(active_stop_6);
	PreActive_Active_7 *preactive_active_7 = new PreActive_Active_7 (n, active, this);
	preactive->addTransition(preactive_active_7);

	automaton = this;
	automaton->timers.push_back(&time);


}

}

