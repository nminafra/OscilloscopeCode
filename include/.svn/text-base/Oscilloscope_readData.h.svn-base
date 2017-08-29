#ifndef OSCILLOSCOPE_READDATA_H
#define OSCILLOSCOPE_READDATA_H
#include <TROOT.h>
#include "TFile.h"
#include "TTree.h"
#include "TGraph.h"
#include "TF1.h"

#include <string>
#include <vector>
#include <set>
#include <iostream>
#include <stdint.h>

#pragma pack(push,1)
struct FileHeader {
  char FileCookie[2];
  char FileVersion[2];
  int32_t FileSize;
  int32_t NumberOfWaveform;
};
#pragma pack(pop)

#pragma pack(push,1)
struct Waveform {
  int32_t HeaderSize;
  int32_t WaveformType;
  int32_t NWaveformBuffers;
  int32_t Points;
  int32_t Count;
  float XDisplayRange;
  double XDisplayOrigin;
  double XIncrement;
  double XOrigin;
  int32_t XUnits;
  int32_t YUnits;
  char Date[16];
  char Time[16];
  char Frame[24];
  char WaveformLabel[16];
  double TimeTag;
  uint32_t SegmentedIndex;
};
#pragma pack(pop)

#pragma pack(push,1)
struct WaveformHeader {
  int32_t HeaderSize;
  int16_t BufferType;
  int16_t BytesPerPoint;
  int32_t BufferSize;
};
#pragma pack(pop)

typedef std::vector< std::vector<double> > HitData;
typedef std::vector<double> HitTime;

struct FileData {
  std::string FileName;
  int FileNumber;
  std::vector<HitTime> Time;
  std::vector<HitData> Data;
  
  FileData(): FileNumber(-1) {}; //Dummy
};

typedef std::vector< std::vector<FileData>::iterator > fileIt_vec_t;

using namespace std;

double computeBaseLine(const std::vector<double>&, const int);


class Oscilloscope_readData {
   string testName_;
//    vector<string> fileName_;
   int N_bline;
   
   //For the TTree
   int HitNumber_;
   int FileNumber_;
   int NumberOfChannels_;
   int waveform_number_tmp_;
   int channel_number_tmp_;
   int data_size_tmp_;
   int bad_points_;
   double base_line_tmp_;
   double SamplingPeriod_tmp_;
   double start_time_tmp_;
   std::vector<double> data_tmp_;
   std::vector<double> time_tmp_;
   
   double peak2peakThreshold_;
   
   bool segmentedFile_;
   
   TFile *f;
   TTree *t;

   std::vector<FileData> fileDataV_;
   
   void readBinary(const std::string&, const int fileNumber=-1);
   void readSegmentedBinary(const std::string&, const int fileNumber=-1);
   
public:
   Oscilloscope_readData(TFile*, const int, const double peak2peakThreshold=.0);
   
   void readFiles( const std::vector<std::string>& );
   void writeTree();
   void finalize();
   void clear();

};

#endif
