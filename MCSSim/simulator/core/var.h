#ifndef SIMULATOR_VAR_H
#define SIMULATOR_VAR_H

#include <string>
#include <vector>

class Network;

//TODO класс с шаблонами
class Var {
	int value;
	Network *net;
public:
	Var(Network *_net, std::string _name);
	Var& operator =(int x);
	Var& operator =( const Var& other );
	operator int();
};

#endif //SIMULATOR_VAR_H
