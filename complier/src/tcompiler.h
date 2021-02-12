#pragma once
#include <fstream>
class TCompiler
{
public: 
	TCompiler(std::ifstream &in);

private:
	std::ifstream& fin;
};