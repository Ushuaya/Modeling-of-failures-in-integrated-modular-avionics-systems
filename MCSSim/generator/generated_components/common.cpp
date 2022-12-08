#include "common.h"

#include "CS.h"
#include "T.h"
#include "L.h"
#include "FPNPS.h"
#include "EDF.h"
#include "FPPS.h"


void createCS (std::string type, std::string _name, Network *n, int p, bool t, CoreSchedulerData* _data, std::vector <Channel*> &_wakeup, std::vector <Channel*> &_sleep)
{
	if (type == "CS")
		new CS::CS ( _name, n, p, t, _data, _wakeup, _sleep);

}
void createT (std::string type, std::string _name, Network *n, int p, bool t, TaskData* _data, Var* _abs_deadline, Var* _is_ready, Var* _prio, std::vector <Var*> &_is_data_ready, Channel* _exec, Channel* _preempt, Channel* _ready, Channel* _finished, Channel* _send, Channel* _receive)
{
	if (type == "T")
		new T::T ( _name, n, p, t, _data, _abs_deadline, _is_ready, _prio, _is_data_ready, _exec, _preempt, _ready, _finished, _send, _receive);

}
void createL (std::string type, std::string _name, Network *n, int p, bool t, LinkData* _data, Var* _is_data_ready, Channel* _send, Channel* _receive)
{
	if (type == "L")
		new L::L ( _name, n, p, t, _data, _is_data_ready, _send, _receive);

}
void createTS (std::string type, std::string _name, Network *n, int p, bool t, TaskSchedulerData* _data, std::vector <Var*> &_abs_deadline, std::vector <Var*> &_is_ready, std::vector <Var*> &_prio, std::vector <Var*> &_id, Channel* _wakeup, Channel* _sleep, Channel* _ready, Channel* _finished, std::vector <Channel*> &_exec, std::vector <Channel*> &_preempt)
{
	if (type == "FPNPS")
		new FPNPS::FPNPS ( _name, n, p, t, _data, _abs_deadline, _is_ready, _prio, _id, _wakeup, _sleep, _ready, _finished, _exec, _preempt);

	if (type == "EDF")
		new EDF::EDF ( _name, n, p, t, _data, _abs_deadline, _is_ready, _prio, _id, _wakeup, _sleep, _ready, _finished, _exec, _preempt);

	if (type == "FPPS")
		new FPPS::FPPS ( _name, n, p, t, _data, _abs_deadline, _is_ready, _prio, _id, _wakeup, _sleep, _ready, _finished, _exec, _preempt);

}

