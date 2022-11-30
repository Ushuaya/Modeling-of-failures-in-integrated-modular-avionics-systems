#include "EDF.h"

using namespace std;

namespace EDF {

EDF::EDF(string _name, Network *n, int p, bool __t, TaskSchedulerData* _data, vector <Var*> &_abs_deadline, vector <Var*> &_is_ready, vector <Var*> &_prio, vector <Var*> &_id
, Channel* _wakeup, Channel* _sleep, Channel* _ready, Channel* _finished, vector <Channel*> &_exec, vector <Channel*> &_preempt
): Automaton(n, _name, p, __t), data(_data), abs_deadline(_abs_deadline), is_ready(_is_ready), prio(_prio), id(_id), wakeup(_wakeup), sleep(_sleep), ready(_ready), finished(_finished), exec(_exec), preempt(_preempt), current(n, "EDF_current")


{
	Waiting* waiting = new Waiting (n, "Waiting", false, false, this);
	addLocation(waiting);
	Executing* executing = new Executing (n, "Executing", false, false, this);
	addLocation(executing);
	Scheduling* scheduling = new Scheduling (n, "Scheduling", false, true, this);
	addLocation(scheduling);
	SendPreempt* sendpreempt = new SendPreempt (n, "SendPreempt", false, true, this);
	addLocation(sendpreempt);
	Preempting* preempting = new Preempting (n, "Preempting", false, true, this);
	addLocation(preempting);
	NewJob* newjob = new NewJob (n, "NewJob", false, true, this);
	addLocation(newjob);
	Sleeping* sleeping = new Sleeping (n, "Sleeping", true, false, this);
	addLocation(sleeping);

	Preempting_Scheduling_0 *preempting_scheduling_0 = new Preempting_Scheduling_0 (n, scheduling, this);
	preempting->addTransition(preempting_scheduling_0);
	SendPreempt_Sleeping_1 *sendpreempt_sleeping_1 = new SendPreempt_Sleeping_1 (n, sleeping, this);
	sendpreempt->addTransition(sendpreempt_sleeping_1);
	NewJob_Executing_2 *newjob_executing_2 = new NewJob_Executing_2 (n, executing, this);
	newjob->addTransition(newjob_executing_2);
	NewJob_Preempting_3 *newjob_preempting_3 = new NewJob_Preempting_3 (n, preempting, this);
	newjob->addTransition(newjob_preempting_3);
	Scheduling_Waiting_4 *scheduling_waiting_4 = new Scheduling_Waiting_4 (n, waiting, this);
	scheduling->addTransition(scheduling_waiting_4);
	Executing_Scheduling_5 *executing_scheduling_5 = new Executing_Scheduling_5 (n, scheduling, this);
	executing->addTransition(executing_scheduling_5);
	SendPreempt_Sleeping_6 *sendpreempt_sleeping_6 = new SendPreempt_Sleeping_6 (n, sleeping, this);
	sendpreempt->addTransition(sendpreempt_sleeping_6);
	Preempting_Scheduling_7 *preempting_scheduling_7 = new Preempting_Scheduling_7 (n, scheduling, this);
	preempting->addTransition(preempting_scheduling_7);
	Waiting_Sleeping_8 *waiting_sleeping_8 = new Waiting_Sleeping_8 (n, sleeping, this);
	waiting->addTransition(waiting_sleeping_8);
	Sleeping_Scheduling_9 *sleeping_scheduling_9 = new Sleeping_Scheduling_9 (n, scheduling, this);
	sleeping->addTransition(sleeping_scheduling_9);
	Scheduling_Sleeping_10 *scheduling_sleeping_10 = new Scheduling_Sleeping_10 (n, sleeping, this);
	scheduling->addTransition(scheduling_sleeping_10);
	Executing_SendPreempt_11 *executing_sendpreempt_11 = new Executing_SendPreempt_11 (n, sendpreempt, this);
	executing->addTransition(executing_sendpreempt_11);
	Waiting_Scheduling_12 *waiting_scheduling_12 = new Waiting_Scheduling_12 (n, scheduling, this);
	waiting->addTransition(waiting_scheduling_12);
	Sleeping_Sleeping_13 *sleeping_sleeping_13 = new Sleeping_Sleeping_13 (n, sleeping, this);
	sleeping->addTransition(sleeping_sleeping_13);
	Scheduling_Scheduling_14 *scheduling_scheduling_14 = new Scheduling_Scheduling_14 (n, scheduling, this);
	scheduling->addTransition(scheduling_scheduling_14);
	Executing_NewJob_15 *executing_newjob_15 = new Executing_NewJob_15 (n, newjob, this);
	executing->addTransition(executing_newjob_15);
	Scheduling_Executing_16 *scheduling_executing_16 = new Scheduling_Executing_16 (n, executing, this);
	scheduling->addTransition(scheduling_executing_16);

	automaton = this;


}

}

