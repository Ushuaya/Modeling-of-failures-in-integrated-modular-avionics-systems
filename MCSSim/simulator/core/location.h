#ifndef SIMULATOR_STATE_H
#define SIMULATOR_STATE_H

#include <string>
#include <vector>

class Network;
class Transition;
class Automaton;
class Timer;

class Location {
public:
    Network * net; //может пригодиться для использования глобальных переменных в inv
    std::string name; //имя состояния
    bool is_init; //является ли состояние начальным
    bool is_committed; //является ли состояние срочным
    int numOfTransitions;
    std::vector<Transition *> transitions; //все переходы из данного состояния

    Location(Network *n, std::string _name, bool init, bool committed): net(n), name(_name), is_init(init), is_committed(committed), numOfTransitions(0) {};
    virtual bool inv() { return true; }; //инвариант состояния (эта функция должна всегда возвращать true, если мы находимся в данном состоянии
    void addTransition(Transition* t) {transitions.push_back(t); numOfTransitions++;}

    virtual bool checkTimer(Timer *t) {return true;}

    bool isCommitted() {return is_committed;}
};


#endif //SIMULATOR_STATE_H
