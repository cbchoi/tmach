#include "tcompiler.h"

#include <fstream>
#include <iostream>

TCompiler::TCompiler(std::ifstream& in): fin(in)
{
	std::cout << "TComp" << std::endl;
	//char buff[120];
	std::string buff;
	getline(fin, buff);
	std::cout << buff << std::endl;
    
}