#include <Wire.h>
#include <dht.h>
#include <SFE_BMP180.h>
#define analogPin  A0 //the thermistor attach to 
#define beta 3950 //the beta of the thermistor
#define resistance 10 //the value of the pull-up resistor

dht DHT;//create a variable type of dht
const int DHT11_PIN= 7;//Humiture sensor attach to pin7
SFE_BMP180 pressure;

void setup()
{ 
  Serial.begin(9600);//initialize the serial monitor

   // Initialize the sensor (it is important to get calibration values stored on the device).
  if (pressure.begin())
    Serial.println("");
  else
  {
    // Oops, something went wrong, this is usually a connection problem,
    // see the comments at the top of this sketch for the proper connections.

    Serial.println("BMP180 init fail\n\n");
    while(1); // Pause forever.
  }
}

void loop()
{
  //Thermistor Start
  long aa =1023 - analogRead(analogPin);
  float tempC = beta /(log((1025.0 * 10 / aa - 10) / 10) + beta / 298.0) - 273.0;
  float tempF = 1.8*tempC + 32.0;
  //Thermistor Stop

  //Humiture Start
  int chk = DHT.read11(DHT11_PIN);
  //Humiture End

  //Barometer Start
  char status;
  double T,P,p0,a;

  status = pressure.startTemperature();
  if (status != 0)
  {
    // Wait for the measurement to complete:
    delay(status);

    status = pressure.getTemperature(T);
    if (status != 0)
    {

      status = pressure.startPressure(3);
      if (status != 0)

      {

        delay(status);

        status = pressure.getPressure(P,T);
        
      }
      else;
    }
    else;
  }
  else;
  //Barometer End

  //Data Start
  Serial.print(tempF); 
  Serial.print(",");
  Serial.print(" ");
  Serial.print(DHT.temperature,1);
  Serial.print(",");
  Serial.print(" ");
  Serial.print(DHT.humidity,1);
  Serial.print(",");
  Serial.print(" ");  
  Serial.print(T,2);
  Serial.print(",");
  Serial.print(" ");
  Serial.println(P,2); //millibars
  //Data Stop
  
  delay(2000); //wait for 100 milliseconds
}


