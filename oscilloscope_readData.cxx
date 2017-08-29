#include <Oscilloscope_readData.h>

#include <iostream>
#include <sstream>
#include <vector>
#include <boost/lexical_cast.hpp>

/**
 * How To:
 * export a variable to environment to set the working directory, than run the program for all the file in the directory:
 * 
 * $$> export FILEPATH=/afs/cern.ch/user/n/nminafra/Work/public/PSTestBeam/Dia500V_CSA_TriggerScint/
 * $$> ./oscilloscope_readData threshold $FILEPATH $(ls -1v $FILEPATH | grep .bin)
 * 
 * Change the PATH of the terget in the main!!
 * 
 * enjoy!
 **/

int main (int argc, char** argv)
{

  // Name of the input files
  std::vector<std::string> filename;
  int n_bline = 0;
  double th = boost::lexical_cast<double>(argv[1]);
	
  std::string path = argv[2];
  
  for (unsigned int i=3; i<argc; ++i) {
    std::string file = path;
    file += argv[i];
    filename.push_back(file);
  }
  
  //Name of the root file
  std::string root_name_tmp(argv[2]);
  std::string root_name = root_name_tmp.substr(root_name_tmp.find_last_of('/',root_name_tmp.size()-2)+1,root_name_tmp.size()-root_name_tmp.find_last_of('/',root_name_tmp.size()-2)-2);
  
  
  //######## Target directory here!
//   root_name.insert(0,"/afs/cern.ch/work/n/nminafra/public/November2015/");
  root_name.insert(0,"/afs/cern.ch/user/n/nminafra/Eos/totem/user/n/nminafra/H8November/");
    
  
  root_name.append(".root");
  std::cout<<root_name<<std::endl;
  TFile* f = new TFile(root_name.c_str(),"RECREATE");
  

  const int max_numb_of_file = 12;
  int i=1;
  
  std::vector<std::string>::const_iterator start_ptr=filename.begin();
  std::vector<std::string>::const_iterator stop_ptr=filename.begin()+std::min(max_numb_of_file, argc-3);
  
  Oscilloscope_readData example_readData(f, n_bline, th );
  while ( (start_ptr>=filename.begin()) && (stop_ptr<=filename.end()) && (stop_ptr-start_ptr>0)) {
    // Read Data
    //   (  path + name of the NTuple (without the ".root"), vector of string filenames, number of point to be used for baseline )
    std::vector<std::string> filename_tmp(start_ptr, stop_ptr);

    example_readData.readFiles(filename_tmp);
    example_readData.writeTree();
    example_readData.clear();
    
    start_ptr = stop_ptr;
    stop_ptr=filename.begin()+std::min(max_numb_of_file*(++i), argc-3);
    std::cout<<(int) (stop_ptr-start_ptr)<<std::endl;
  
  }
//   example_readData.finalize();
  f->Close();
}
