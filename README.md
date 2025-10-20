#final_exam_sender => on_arduino => Arduino:
  - SHT31 => Arduino
  - VDD => 3.3v
  - GND => GND
  - DATA => SDA
  - SCK => SCL

#on_raspi => Rasberry pi:
  - I2C LCD => Rasberry pi
  - VCC => 5v (pin 4)
  - GND => GND (pin 6)
  - SDA => gpio 2 (pin 3)
  - SCL => gpio 3 (pin 5)

#arduino library:
  - Adafruit SHT31 by adafruit
  - MQTT by joel
