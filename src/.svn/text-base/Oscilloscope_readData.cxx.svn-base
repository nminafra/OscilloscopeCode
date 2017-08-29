#include "Oscilloscope_readData.h"

#include "TROOT.h"
#include "TInterpreter.h"
#include "TMath.h"

#include <iostream>
#include <fstream>
#include <sstream>
#include <streambuf>
#include <iterator>

#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>

//constructor
Oscilloscope_readData::Oscilloscope_readData(TFile* root_file, const int N_bline, const double peak2peakThreshold) : f(root_file), N_bline(N_bline), HitNumber_(1), FileNumber_(0), NumberOfChannels_(0), bad_points_(0), peak2peakThreshold_(peak2peakThreshold), segmentedFile_(false) {
//   string ext =".root";
//   string fname = testName_ + ext;
//   f = new TFile(fname.c_str(),"RECREATE");
  t = new TTree("t_v2","rootuple");
  t->Branch("FileNumber", &(this->FileNumber_), "FileNumber/I");
  t->Branch("NumberOfChannels", &(this->NumberOfChannels_), "NumberOfChannels/I");
  t->Branch("HitNumber", &(this->HitNumber_), "HitNumber/I");
  t->Branch("Channel", &(this->channel_number_tmp_), "Channel/I" );
  t->Branch("DataSize", &(this->data_size_tmp_), "DataSize/I" );
  t->Branch("BaseLine", &(this->base_line_tmp_), "BaseLine/D" );
  t->Branch("SamplingPeriod", &(this->SamplingPeriod_tmp_), "SamplingPeriod/D" );
  t->Branch("StartTime", &(this->start_time_tmp_), "StartTime/D" );
  t->Branch("BadPoints", &(this->bad_points_), "BadPoints/I" );
  t->Branch("DataSamples", "vector<double>", &(this->data_tmp_) );
  t->Branch("TimeSamples", "vector<double>", &(this->time_tmp_) );
}

void Oscilloscope_readData::clear() {
  fileDataV_.clear();
}

void Oscilloscope_readData::readFiles(const std::vector<std::string>& df) {
  if (df.size() == 0) return;
  std::cout << "Reading file from " <<*(df.begin())<< std::endl;
  std::cout << "\tto " <<*(df.rbegin())<< std::endl;
  int lastdone=-1;
  int doing=-1;
  for(unsigned int i=0;i<df.size();i++)
  {
//     std::cout << "Reading file " << i+1 << ": " <<df[i]<< std::endl;
    if ( boost::iends_with(df[i], ".bin") ) { 
      if (boost::iends_with(df[i].substr(0,df[i].size()-5), "_CH")) {
	segmentedFile_=true;
	std::string segmentedFilename = df[i].substr(0,df[i].size()-8);
	doing = boost::lexical_cast<int>(segmentedFilename.substr(segmentedFilename.find_last_of("_")+1,segmentedFilename.size()-segmentedFilename.find_last_of("_")));
	if (doing!=lastdone) {
	  readSegmentedBinary(segmentedFilename,doing);
	  lastdone=doing;
	}
      }
      else {
	if (segmentedFile_) std::cerr << "*****Segmented o not segmented? this is the question!*******" << std::endl; 
	readBinary(df[i]);
      }
    }
    else std::cout<<"I have no idea how to process this: "<<df[i]<<std::endl;
  }
  std::cout << "*****DATA SUCESSFULLY READ*******" << std::endl; 
}

void Oscilloscope_readData::finalize() {
//   f->Close();
}

void Oscilloscope_readData::writeTree() {
  if (fileDataV_.size()==0) return;
  if(!f) return;
  if(!t) return;
  std::cout << "**********MAKING THE TREE***********" << std::endl; 
  
  waveform_number_tmp_=-1;
  channel_number_tmp_=-1;
  data_size_tmp_=-1;
  base_line_tmp_=.0;
  SamplingPeriod_tmp_=.0;
  start_time_tmp_=.0;
  
  std::vector<FileData>::iterator fileIt = fileDataV_.begin();
  
  if (segmentedFile_) {
    TGraph rate_graph;
    int rate_graph_i(0);
    fileIt_vec_t fileIt_vec;
    int processingHitNumber=fileIt->FileNumber;
//     HitNumber_=1;
    for (fileIt=fileDataV_.begin(); fileIt!=fileDataV_.end(); ++fileIt) {
      if (fileIt->FileNumber == processingHitNumber && fileIt!=fileDataV_.end()-1) fileIt_vec.push_back(fileIt);
      else {
	if (fileIt==fileDataV_.end()-1) fileIt_vec.push_back(fileIt);
	int timeSize = (*fileIt_vec.begin())->Time.size();
	NumberOfChannels_= fileIt_vec.size();
	for (fileIt_vec_t::iterator fileIt_vecIt=fileIt_vec.begin(); fileIt_vecIt!=fileIt_vec.end(); ++fileIt_vecIt) {
	  if ((*fileIt_vecIt)->Time.size() != timeSize) {
	    std::cerr << "##### Different number of segments for the channels! #####" << std::endl;
	    return;
	  }
	}
	for (waveform_number_tmp_=0; waveform_number_tmp_<timeSize; ++waveform_number_tmp_) {  
	  for (fileIt_vec_t::iterator fileIt_vecIt=fileIt_vec.begin(); fileIt_vecIt!=fileIt_vec.end(); ++fileIt_vecIt) {
	    channel_number_tmp_ = boost::lexical_cast<int>((*fileIt_vecIt)->FileName.substr((*fileIt_vecIt)->FileName.size()-5,1));
// 	      std::cout << "\twriting channel " << channel_number_tmp_ << " of event " << processingHitNumber << std::endl;
	    time_tmp_ = (*fileIt_vecIt)->Time.at(waveform_number_tmp_);
	    start_time_tmp_ = time_tmp_.at(0);
	    SamplingPeriod_tmp_ = time_tmp_.at(1) - time_tmp_.at(0);
	    data_size_tmp_ = time_tmp_.size();
	    
	    data_tmp_ =  (*fileIt_vecIt)->Data.at(waveform_number_tmp_).at(0);
      //       base_line_tmp_ = computeBaseLine(data_tmp_, N_bline);
	    
	    if (FileNumber_ != fileIt->FileNumber) {
	      HitNumber_ = fileIt->FileNumber * timeSize+1;
	    }
	    FileNumber_ = fileIt->FileNumber;
	    
	    
	    if (peak2peakThreshold_!=.0) {
	      std::vector<double>::const_iterator max = std::max_element(data_tmp_.begin(), data_tmp_.end());
	      std::vector<double>::const_iterator min = std::min_element(data_tmp_.begin(), data_tmp_.end());
	      if (*max-*min>peak2peakThreshold_)
		t->Fill();
	    }
	    else t->Fill();
	    
// 	    rate_graph.SetPoint(rate_graph_i++,start_time_tmp_,HitNumber_);
	  }
	  ++HitNumber_;
	}
	
	if (fileIt!=fileDataV_.end()-1) {
	  processingHitNumber=fileIt->FileNumber;
	  fileIt_vec.clear();
	  fileIt_vec.push_back(fileIt);
	}
      }
  
//       TF1 rateLin("rateLin","pol1",0,50);
//       rateLin.FixParameter(0,.0);
//       rate_graph.Fit(&rateLin,"FQ");
//       rate_graph.Write();
//       std::cout<<"Measured rate: "<<rateLin.GetParameter(1)<<" +- "<<rateLin.GetParError(1)<<" Hz; file: "<<fileIt->FileName<<std::endl;
    }
    
    
  }	//end if segmented
  else {
    for (fileIt=fileDataV_.begin(); fileIt!=fileDataV_.end(); ++fileIt) {
      for (waveform_number_tmp_=0; waveform_number_tmp_<fileIt->Time.size(); ++waveform_number_tmp_) {   
	if (waveform_number_tmp_>4) std::cout << "####Are you sure it is not a segmented acquisition??#####" << std::endl;
	channel_number_tmp_ = waveform_number_tmp_;
	time_tmp_ = fileIt->Time.at(waveform_number_tmp_);
	start_time_tmp_ = time_tmp_.at(0);
	SamplingPeriod_tmp_ = time_tmp_.at(1) - time_tmp_.at(0);
	data_size_tmp_ = time_tmp_.size();
	
	data_tmp_ =  fileIt->Data.at(waveform_number_tmp_).at(0);
  //       base_line_tmp_ = computeBaseLine(data_tmp_, N_bline);
	if (peak2peakThreshold_!=.0) {
	  std::vector<double>::const_iterator max = std::max_element(data_tmp_.begin(), data_tmp_.end());
	  std::vector<double>::const_iterator min = std::min_element(data_tmp_.begin(), data_tmp_.end());
	  if (*max-*min>peak2peakThreshold_)
	    t->Fill();
	}
	else t->Fill();
      }
      ++HitNumber_;
    }
  }
  t->Write();
  std::cout<<"HitNumber: "<<HitNumber_<<std::endl;

  std::cout << "*****TREE SUCESSFULLY WRITTEN******* with "<< t->GetEntries() << " Entries"<< std::endl; 
}

void Oscilloscope_readData::readBinary(const std::string& filename, const int fileNumber) { 
  ifstream data(filename.c_str(),std::fstream::in | std::fstream::binary);  // read only mode
  if(!data) std::cout << "************Missing*file**************" << std::endl; 
  else {
    FileData fileData_tmp; 
    fileData_tmp.FileName = filename;
    fileData_tmp.FileNumber = fileNumber;
    
    //Read File Header
    FileHeader fileHeader;
    Waveform waveform;
    WaveformHeader waveformHeader;
    data.read((char*) &fileHeader,sizeof(FileHeader));
    if ( (fileHeader.FileCookie[0] != 'A') || (fileHeader.FileCookie[1] != 'G') ) {
      std::cout << "File Header Wrong: " << fileHeader.FileCookie[0] << " " << fileHeader.FileCookie[1] << std::endl;
      return;	//TODO
    }
//     std::cout<< fileHeader.NumberOfWaveform << " Waveform to read" << std::endl;
    // std::cout<< sizeof(fileHeader) << " Bytes of header" << std::endl;
    NumberOfChannels_ = fileHeader.NumberOfWaveform;
    for (int waveform_i=0; waveform_i<fileHeader.NumberOfWaveform; ++waveform_i) {
      data.read((char*) &waveform,sizeof(waveform));
      
      // Compute Time samples
      // std::cout<< '\t'<< waveform.Points << " Points in the Waveform to read" << std::endl;
      // std::cout<< '\t'<< sizeof(waveform) << " Bytes of waveform header " << waveform.HeaderSize << std::endl;
      HitTime time_tmp(waveform.Points);
      for (int point_i=0; point_i<waveform.Points; ++point_i) {
	time_tmp.at(point_i) = waveform.TimeTag + waveform.XOrigin + point_i * waveform.XIncrement;
      }
      fileData_tmp.Time.push_back(time_tmp);
      
      if (waveform.NWaveformBuffers > 1) std::cout << "!!! More than one buffer in each waveform... others will be ignored" << std::endl;
//       std::cout<<"TimeTag:\t"<<waveform.TimeTag<<std::endl;
//       std::cout<<"SegmentedIndex:\t"<<waveform.SegmentedIndex<<std::endl;
      //Compute Data samples
      HitData data_tmp(waveform.NWaveformBuffers);
      for (int buffer_i=0; buffer_i<waveform.NWaveformBuffers; ++buffer_i) {
	data.read((char*) &waveformHeader,sizeof(waveformHeader));
	// std::cout<< '\t'<< sizeof(waveformHeader) << " Bytes of waveformHeader header " << waveformHeader.HeaderSize << "\tBytes per point:" << waveformHeader.BytesPerPoint << std::endl;
	switch (waveformHeader.BufferType) {
	  case 1:
	  case 2:
	  case 3:
	    float value_float;
	    for (int point_i=0; point_i<waveform.Points; ++point_i) {
	      data.read( (char*) &value_float, sizeof(value_float));
	      data_tmp.at(buffer_i).push_back( (double) value_float);
	    }
	    break;
	  case 4:
	    int32_t value_int;
	    for (int point_i=0; point_i<waveform.Points; ++point_i) {
	      data.read( (char*) &value_int, sizeof(value_int));
	      data_tmp.at(buffer_i).push_back( (double) value_int);
	    }
	    break;
	  default:
	    // std::cout<< "\t\tBuffer of unknown type: " << waveformHeader.BufferType << std::endl;
	    for (int point_i=0; point_i<waveform.Points; ++point_i) {
	      data_tmp.at(buffer_i).push_back( .0);
	    }
	    break;
	    }
	}
	fileData_tmp.Data.push_back(data_tmp);
// 	for (int i=0; i<data_tmp.at(0).size(); ++i) std::cout << data_tmp.at(0).at(i) << '\t';
// 	std::cout<<std::endl;
      }

    fileDataV_.push_back( fileData_tmp );
    data.close();
  } // end if file
}

void Oscilloscope_readData::readSegmentedBinary(const std::string& filename, const int fileNumber) {
  for (int ch=1; ch<=4; ++ch) {
    std::string filename_ch(filename);	//remove "_CH*.bin"
    filename_ch+="_CH";
    filename_ch+=std::to_string(ch);
    filename_ch+=".bin";
    ifstream data(filename_ch.c_str(),std::fstream::in | std::fstream::binary);  // read only mode
    if(!data) {
      std::cout << "************Missing*channel*"<<ch<<"**************" << std::endl; 
      data.close();
    }
    else {
      data.close();
      readBinary(filename_ch,fileNumber);
    }
  }
}

double computeBaseLine(const std::vector<double> &data, const int N_bline) {
  double baseline = .0;
  int numbOfSamples=(N_bline<data.size())?N_bline:data.size();
  //Determine numbOfSamples to consider
  //TODO
  
  //Compute base line
  for (int i=1; i<numbOfSamples; ++i) {
    baseline += data.at(i);
  }
  baseline = baseline/(numbOfSamples-1);
  
  //Subtract BaseLine
//   hit.BaseLine = baseline;
//   for (int i=0; i<DATA_SAMPLES; ++i) {
//     hit.DataSamples[i] = hit.DataSamples[i] - baseline;
//   }
  return baseline;
}
