%module Arcus
%{
#include "Arcus.h"
%}

// Swig interface file to wrap PerformaxCom.lib into python

//!!!run "swig -python -c++ Arcus.i" in the Arcus wrapper sources directory to generate new Arcus_wrap.cxx file i.e. after changing this file!!!

class Arcus {
public:
  Arcus();
  ~Arcus();
  int Connect();
  void SendAndRecive(char *input_buf, char *output_buf);
  void Close();
};