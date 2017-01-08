#include "TCS3200.h"

TCS3200 Colormeter;
COLORS  RGB;

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete


void setup() {
  Serial.begin(115200);
  Colormeter.begin(8, 9, 10, 11, 12);
  pinMode(13, OUTPUT);
  inputString.reserve(200);
}

void loop() {
  RGB = Colormeter.update();
  Serial.print("@R:\t");
  Serial.print(RGB.red);
  Serial.print("\tB:\t");
  Serial.print(RGB.blue);
  Serial.print("\tG:\t");
  Serial.print(RGB.green);
  Serial.print("\tC:\t");
  Serial.print(RGB.all);
  Serial.println("*");

}




