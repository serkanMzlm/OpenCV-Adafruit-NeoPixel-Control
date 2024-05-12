#include <Adafruit_NeoPixel.h>

#ifdef __AVR__
 #include <avr/power.h> 
#endif

#define PIN_NUMBER    6
#define NUMBER_OF_LEDS 60

Adafruit_NeoPixel strip(NUMBER_OF_LEDS, PIN_NUMBER, NEO_GRB + NEO_KHZ800);

class LinearKalman{
public:
  LinearKalman(float mea_e = 0.1, float est_e = 0.5);
  float updateEstimate(float mea);
  void setEstimateError(float est_e);
  void setMeasurementError(float mea_e);
  void setProcesNoise(float q);
private:
  float q;
  float gain;
  float measure_err;
  float estimate_err;
  float last_estimate;
  float current_estimate;
};

typedef enum {RED, GREEN, BLUE, COLOR_SIZE} Color_e;
typedef struct{
  union{
    int red;
    int green;
    int blue;
    int color[COLOR_SIZE];
  };
  union{
    int raw_red;
    int raw_green;
    int raw_blue;
    int raw_color[COLOR_SIZE];
  };
}Color_s;

LinearKalman kalman[3];
Color_s color;

void setup() {
  // put your setup code here, to run once:
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif

  Serial.begin(9600);
  strip.begin();           // INITIALIZE NeoPixel strip object (REQUIRED)
  strip.show();            // Turn OFF all pixels ASAP
  strip.setBrightness(255); // Set BRIGHTNESS to about 1/5 (max = 255)
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available()>1){
    for(int i = 0; i < COLOR_SIZE; i++){
      color.raw_color[i] = Serial.parseInt();
      color.color[i] = map(color.raw_color[i], 0, 100,10, 255);
      color.color[i] = kalman[i].updateEstimate(color.color[i]);
    }
    if(Serial.read() != '\n'){
      for(int i=0 ; i<12; i++){
        strip.setPixelColor(i, strip.Color(color.red, color.green, color.blue));
        strip.show();
      }
    }
  }
}

LinearKalman::LinearKalman(float mea_e, float est_e){
  this->measure_err = mea_e;
  this->estimate_err = est_e;
  last_estimate = 0.0f;
  current_estimate = 0.0f;
  q = 0.5f;
}

float LinearKalman::updateEstimate(float mea){
  gain = estimate_err / (estimate_err + measure_err);
  current_estimate = last_estimate + gain * (mea - last_estimate);
  estimate_err = (1.0f - gain) * estimate_err + fabsf(last_estimate - current_estimate) * q;
  last_estimate = current_estimate;
  return current_estimate;
}

void LinearKalman::setEstimateError(float est_e){
  this->estimate_err = est_e;
}

void LinearKalman::setMeasurementError(float mea_e){
  this->measure_err = mea_e;
}

void LinearKalman::setProcesNoise(float q){
  this->q = q;
}

