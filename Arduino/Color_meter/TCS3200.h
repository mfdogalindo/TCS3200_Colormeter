#include "Arduino.h"

#define TCS3200_SAMPLES   10

#define TCS3200_DOWN    0
#define TCS3200_2       1
#define TCS3200_20      2
#define TCS3200_100     3

#define TCS3200_RED     0
#define TCS3200_BLUE    1
#define TCS3200_CLEAR   2
#define TCS3200_GREEN   3



struct COLORS {
  uint16_t red;
  uint16_t green;
  uint16_t blue;
  uint16_t all;
};

class TCS3200
{
  public:
    
    void begin(uint8_t S0, uint8_t S1, uint8_t S2, uint8_t S3, uint8_t OUT);
    COLORS update();
    void wakeup();
    void sleep();
    void scaling(uint8_t mode);
    uint16_t read(uint8_t color);

 private:
    uint8_t _S0, _S1, _S2, _S3, _OUT;
    COLORS col;   
};
