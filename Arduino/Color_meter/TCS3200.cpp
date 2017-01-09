#include "TCS3200.h"

#define PORT_ISR    (digitalPinToPort(TCS3200_OUT_PIN))
#define PIN_ISR     (digitalPinToBitMask(TCS3200_OUT_PIN))
#define VECTOR_ISR  (PCINT0_vect_num+(PORT_ISR-0x02))

#define DEFAULT_SCALING 1

uint8_t scal = DEFAULT_SCALING;


void TCS3200::begin(uint8_t S0, uint8_t S1, uint8_t S2, uint8_t S3, uint8_t OUT) {
  _S0 = S0;
  _S1 = S1;
  _S2 = S2;
  _S3 = S3;
  _OUT = OUT;
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(OUT, INPUT);

}

COLORS TCS3200:: update() {
  digitalWrite(_S0, (scal & 0x3) > 1);
  digitalWrite(_S1, (scal & 0x1));
  col.red = read(TCS3200_RED);
  col.green = read(TCS3200_GREEN);
  col.blue = read(TCS3200_BLUE);
  col.all = read(TCS3200_CLEAR);
  digitalWrite(_S0, LOW);
  digitalWrite(_S1, LOW);
  return col;
}

uint16_t TCS3200::read(uint8_t color) {
  uint16_t pulse;
  digitalWrite(_S2, (color & 0x3) > 1);
  digitalWrite(_S3, (color & 0x1));
  pulse = pulseIn(_OUT, HIGH,5000000);
  return pulse;
}

void TCS3200::scaling(uint8_t mode) {
  scal = mode;
}

void TCS3200::wakeup() {
  digitalWrite(_S0, (scal & 0x3) > 1);
  digitalWrite(_S1, (scal & 0x1));
}

void TCS3200::sleep() {
  digitalWrite(_S0, LOW);
  digitalWrite(_S1, LOW);
}


