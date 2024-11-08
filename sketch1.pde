// Read data from a serial port and export to a file
import processing.serial.*;
Serial myPort;
String val, portName;
PrintWriter output;

void setup()
{
  portName = Serial.list()[0];
  myPort = new Serial(this, portName, 9600);
  output = createWriter("Data.csv");
  output.println("Time(s), Thermistor Temp(F), Humiture Temp (C), Humidity (%), Barometer (C), Barometer (mb) ");
  output.println("");
}

void draw()
{
  while (myPort.available() > 0)
  {
    val = myPort.readStringUntil('\n');
    if (val != null)
    {
    int m = millis();
      output.print(m/1000);
      output.print(',');
      output.print(val);
      println(val);
    }
  }
}

void keyPressed()
{// Press a key to save the data, make sure your cursor is in the small box when you click any button to stop the code.
  output.flush();
  output.close();
  exit();
}
  
