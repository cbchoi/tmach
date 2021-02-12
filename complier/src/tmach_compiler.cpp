#include <iostream>
#include <fstream>
#include <sstream>
#include <cstring>
#include "tcompiler.h"

int main(int argc, char** argv)
{
	std::stringstream sstream;
	if (argc != 2)
	{
		std::cerr<< "usage: " << argv[0] << " <filename>" << std::endl;
		exit(1);
	}

	sstream << argv[1];
	if (strchr(sstream.str().c_str(), '.') == NULL)
		sstream << ".tny";
	
	std::ifstream fin(sstream.str().c_str());
	if(!fin.good())
	{
		std::cerr << "File " << sstream.str() << " not found." << std::endl;
		exit(1);
	}

	TCompiler t(fin);
    
	return 0;
}