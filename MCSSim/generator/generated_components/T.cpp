#include "T.h"

using namespace std;

namespace T {

T::T(string _name, Network *n, int p, bool __t, TaskData* _data, Var* _abs_deadline, Var* _is_ready, Var* _prio, vector <Var*> &_is_data_ready
, Channel* _exec, Channel* _preempt, Channel* _ready, Channel* _finished, Channel* _send, Channel* _receive
): Automaton(n, _name, p, __t), data(_data), abs_deadline(_abs_deadline), is_ready(_is_ready), prio(_prio), is_data_ready(_is_data_ready), exec(_exec), preempt(_preempt), ready(_ready), finished(_finished), send(_send), receive(_receive), exec_timer(n, "T_exec_timer"), local_timer(n, "T_local_timer")


{
	Dormant* dormant = new Dormant (n, "Dormant", false, false, this);
	addLocation(dormant);
	Ready* ready = new Ready (n, "Ready", false, false, this);
	addLocation(ready);
	SendReadySig* sendreadysig = new SendReadySig (n, "SendReadySig", false, true, this);
	addLocation(sendreadysig);
	Finished* finished = new Finished (n, "Finished", false, true, this);
	addLocation(finished);
	Exec* exec = new Exec (n, "Exec", false, false, this);
	addLocation(exec);
	WaitingForData* waitingfordata = new WaitingForData (n, "WaitingForData", false, false, this);
	addLocation(waitingfordata);
	WaitingForNewPeriod* waitingfornewperiod = new WaitingForNewPeriod (n, "WaitingForNewPeriod", false, false, this);
	addLocation(waitingfornewperiod);
	Start* start = new Start (n, "Start", true, true, this);
	addLocation(start);
	Send* send = new Send (n, "Send", false, true, this);
	addLocation(send);

	Start_Dormant_0 *start_dormant_0 = new Start_Dormant_0 (n, dormant, this);
	start->addTransition(start_dormant_0);
	WaitingForData_WaitingForData_1 *waitingfordata_waitingfordata_1 = new WaitingForData_WaitingForData_1 (n, waitingfordata, this);
	waitingfordata->addTransition(waitingfordata_waitingfordata_1);
	Dormant_Dormant_2 *dormant_dormant_2 = new Dormant_Dormant_2 (n, dormant, this);
	dormant->addTransition(dormant_dormant_2);
	WaitingForNewPeriod_Dormant_3 *waitingfornewperiod_dormant_3 = new WaitingForNewPeriod_Dormant_3 (n, dormant, this);
	waitingfornewperiod->addTransition(waitingfornewperiod_dormant_3);
	Exec_Finished_4 *exec_finished_4 = new Exec_Finished_4 (n, finished, this);
	exec->addTransition(exec_finished_4);
	Send_Finished_5 *send_finished_5 = new Send_Finished_5 (n, finished, this);
	send->addTransition(send_finished_5);
	Exec_Send_6 *exec_send_6 = new Exec_Send_6 (n, send, this);
	exec->addTransition(exec_send_6);
	WaitingForData_WaitingForNewPeriod_7 *waitingfordata_waitingfornewperiod_7 = new WaitingForData_WaitingForNewPeriod_7 (n, waitingfornewperiod, this);
	waitingfordata->addTransition(waitingfordata_waitingfornewperiod_7);
	Ready_WaitingForNewPeriod_8 *ready_waitingfornewperiod_8 = new Ready_WaitingForNewPeriod_8 (n, waitingfornewperiod, this);
	ready->addTransition(ready_waitingfornewperiod_8);
	WaitingForData_SendReadySig_9 *waitingfordata_sendreadysig_9 = new WaitingForData_SendReadySig_9 (n, sendreadysig, this);
	waitingfordata->addTransition(waitingfordata_sendreadysig_9);
	WaitingForData_WaitingForData_10 *waitingfordata_waitingfordata_10 = new WaitingForData_WaitingForData_10 (n, waitingfordata, this);
	waitingfordata->addTransition(waitingfordata_waitingfordata_10);
	Dormant_WaitingForData_11 *dormant_waitingfordata_11 = new Dormant_WaitingForData_11 (n, waitingfordata, this);
	dormant->addTransition(dormant_waitingfordata_11);
	Finished_WaitingForNewPeriod_12 *finished_waitingfornewperiod_12 = new Finished_WaitingForNewPeriod_12 (n, waitingfornewperiod, this);
	finished->addTransition(finished_waitingfornewperiod_12);
	Exec_Ready_13 *exec_ready_13 = new Exec_Ready_13 (n, ready, this);
	exec->addTransition(exec_ready_13);
	Ready_Exec_14 *ready_exec_14 = new Ready_Exec_14 (n, exec, this);
	ready->addTransition(ready_exec_14);
	SendReadySig_Ready_15 *sendreadysig_ready_15 = new SendReadySig_Ready_15 (n, ready, this);
	sendreadysig->addTransition(sendreadysig_ready_15);
	Dormant_SendReadySig_16 *dormant_sendreadysig_16 = new Dormant_SendReadySig_16 (n, sendreadysig, this);
	dormant->addTransition(dormant_sendreadysig_16);

	automaton = this;
	automaton->timers.push_back(&exec_timer);
	automaton->timers.push_back(&local_timer);


}

}

