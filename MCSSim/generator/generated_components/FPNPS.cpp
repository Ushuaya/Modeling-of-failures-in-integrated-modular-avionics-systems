#include "FPNPS.h"

using namespace std;

namespace FPNPS {

FPNPS::FPNPS(string _name, Network *n, int p, bool __t, TaskSchedulerData* _data, vector <Var*> &_abs_deadline, vector <Var*> &_is_ready, vector <Var*> &_prio, vector <Var*> &_id
, Channel* _wakeup, Channel* _sleep, Channel* _ready, Channel* _finished, vector <Channel*> &_exec, vector <Channel*> &_preempt
): Automaton(n, _name, p, __t), data(_data), abs_deadline(_abs_deadline), is_ready(_is_ready), prio(_prio), id(_id), wakeup(_wakeup), sleep(_sleep), ready(_ready), finished(_finished), exec(_exec), preempt(_preempt), current(n, "FPNPS_current")


{
	Waiting* waiting = new Waiting (n, "Waiting", false, false, this);
	addLocation(waiting);
	Executing* executing = new Executing (n, "Executing", false, false, this);
	addLocation(executing);
	Scheduling* scheduling = new Scheduling (n, "Scheduling", false, true, this);
	addLocation(scheduling);
	Sleeping* sleeping = new Sleeping (n, "Sleeping", true, false, this);
	addLocation(sleeping);
	SendPreempt* sendpreempt = new SendPreempt (n, "SendPreempt", false, true, this);
	addLocation(sendpreempt);

	SendPreempt_Sleeping_0 *sendpreempt_sleeping_0 = new SendPreempt_Sleeping_0 (n, sleeping, this);
	sendpreempt->addTransition(sendpreempt_sleeping_0);
	Executing_Executing_1 *executing_executing_1 = new Executing_Executing_1 (n, executing, this);
	executing->addTransition(executing_executing_1);
	Waiting_Scheduling_2 *waiting_scheduling_2 = new Waiting_Scheduling_2 (n, scheduling, this);
	waiting->addTransition(waiting_scheduling_2);
	Sleeping_Sleeping_3 *sleeping_sleeping_3 = new Sleeping_Sleeping_3 (n, sleeping, this);
	sleeping->addTransition(sleeping_sleeping_3);
	Waiting_Sleeping_4 *waiting_sleeping_4 = new Waiting_Sleeping_4 (n, sleeping, this);
	waiting->addTransition(waiting_sleeping_4);
	Executing_Scheduling_5 *executing_scheduling_5 = new Executing_Scheduling_5 (n, scheduling, this);
	executing->addTransition(executing_scheduling_5);
	Sleeping_Scheduling_6 *sleeping_scheduling_6 = new Sleeping_Scheduling_6 (n, scheduling, this);
	sleeping->addTransition(sleeping_scheduling_6);
	Scheduling_Sleeping_7 *scheduling_sleeping_7 = new Scheduling_Sleeping_7 (n, sleeping, this);
	scheduling->addTransition(scheduling_sleeping_7);
	Scheduling_Scheduling_8 *scheduling_scheduling_8 = new Scheduling_Scheduling_8 (n, scheduling, this);
	scheduling->addTransition(scheduling_scheduling_8);
	SendPreempt_Sleeping_9 *sendpreempt_sleeping_9 = new SendPreempt_Sleeping_9 (n, sleeping, this);
	sendpreempt->addTransition(sendpreempt_sleeping_9);
	Executing_SendPreempt_10 *executing_sendpreempt_10 = new Executing_SendPreempt_10 (n, sendpreempt, this);
	executing->addTransition(executing_sendpreempt_10);
	Scheduling_Executing_11 *scheduling_executing_11 = new Scheduling_Executing_11 (n, executing, this);
	scheduling->addTransition(scheduling_executing_11);
	Scheduling_Waiting_12 *scheduling_waiting_12 = new Scheduling_Waiting_12 (n, waiting, this);
	scheduling->addTransition(scheduling_waiting_12);

	automaton = this;


}

}

