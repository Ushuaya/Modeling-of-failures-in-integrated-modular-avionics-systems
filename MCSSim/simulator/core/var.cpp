#include "var.h"
#include "network.h"
#include <iostream>

using namespace std;

Var::Var(Network *__net, std::string __name): value(0), net(__net)
{
	__net->addVar(this);
}

Var& Var::operator = (int x)
{
	value = x;
	return *this;
}

Var::operator int()
{
	return value;
}

Var& Var::operator = (const Var& other)
{
	value = other.value;
	return *this;
}
