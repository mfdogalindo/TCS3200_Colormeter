#include "TCS3200.h"
//#define CONTINUOUS_MODE

TCS3200 Colormeter;
COLORS  RGB;


void setup() {
  Serial.begin(115200);
  Colormeter.begin(8, 9, 10, 11, 12);
}

void loop() {
#ifndef CONTINUOUS_MODE  
  if (Serial.available()) {
#endif    
    RGB = Colormeter.update();
    Serial.print("@");
    Serial.print("R:\t");
    Serial.print(RGB.red);
    Serial.print("\tG:\t");
    Serial.print(RGB.green);
    Serial.print("\tB:\t");
    Serial.print(RGB.blue);
    Serial.print("\tC:\t");
    Serial.print(RGB.all);
    Serial.print("*");  
#ifdef CONTINUOUS_MODE
    Serial.println();
#endif      
#ifndef CONTINUOUS_MODE    
    while (Serial.available()) {
      int x = Serial.read();
    }   
  }
#endif   
}





