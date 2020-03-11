/*******************************************************************************
* Copyright 2016 ROBOTIS CO., LTD.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/

/* Authors: Taehun Lim (Darby) */

#include <DynamixelWorkbench.h>

#if defined(__OPENCM904__)
  #define DEVICE_NAME "3" //Dynamixel on Serial3(USART3)  <-OpenCM 485EXP
#elif defined(__OPENCR__)
  #define DEVICE_NAME ""
#endif   

#define NOMBRE_TIC 4096
#define BAUDRATE   57600
#define DXL_ID     101
#define laser_pin 4 // pin 4 on board
#define laser_5V  6 // pin 6 on board

DynamixelWorkbench dxl_wb;

void laser_ON(void);
void laser_OFF(void);

void setup() 
{
  Serial.begin(9600);
  while(!Serial); // Wait for Opening Serial Monitor

  const char *log;
  bool result = false;

  uint8_t dxl_id = DXL_ID;
  uint16_t model_number = 0;

  result = dxl_wb.init(DEVICE_NAME, BAUDRATE, &log);
  if (result == false)
  {
    Serial.println(log);
    Serial.println("Failed to init");
  }
  else
  {
    Serial.print("Succeeded to init : ");
    Serial.println(BAUDRATE);  
  }

  result = dxl_wb.ping(dxl_id, &model_number, &log);
  if (result == false)
  {
    Serial.println(log);
    Serial.println("Failed to ping");
  }
  else
  {
    Serial.println("Succeeded to ping");
    Serial.print("id : ");
    Serial.print(dxl_id);
    Serial.print(" model_number : ");
    Serial.println(model_number);
  }
  result = dxl_wb.wheelMode(dxl_id, 0, &log);
  if (result == false)
  {
    Serial.println(log);
    Serial.println("Failed to change wheel mode");
  }
  else
  {
    Serial.println("Succeed to change wheel mode");
  }
  pinMode(laser_pin, OUTPUT)
  pinMode(laser_5V, OUTPUT)
  digitalWrite(laser_5V, HIGH);
  laser_OFF();
}
// change the received command into an integer from 1 to 4
int convert_command(String command) {
    //Serial.println(command);
    int command_number;
    if (command=="run\n") {
      command_number = 1;
    }
    else if (command=="stop\n") {
      command_number = 2;
    }
    else if (command=="restart\n") {
      command_number = 3;
    }
    else {
      command_number = 4;
    }
    return command_number;
}

void laser_ON(){
  digitalWrite(laser_pin, HIGH);
}

void laser_OFF(){
 digitalWrite(laser_pin, HIGH);
}

void loop() {
  uint8_t dxl_id = DXL_ID;
  int32_t Position = 0;
  //get the command from serial port
  if (Serial.available() > 0) {
    String command = Serial.readString();
    int command_number = convert_command(command);
    switch (command_number){

      //start
      case 1:
        //Serial.println("Running");
        laser_ON();
        dxl_wb.wheelMode(dxl_id, 0);
        dxl_wb.goalVelocity(dxl_id, (int32_t)10);
        break;

      //stop
      case 2:
        //Serial.println("Stop");
        laser_OFF();
        dxl_wb.wheelMode(dxl_id, 0);
        dxl_wb.goalVelocity(dxl_id, (int32_t)0);
        break;

      //restart
      case 3:
        //Serial.println("Restarting");
        laser_OFF();
        dxl_wb.jointMode(dxl_id, 0, 0);
        dxl_wb.goalPosition(dxl_id, (int32_t)0);
        break;

      //error in the command
      case 4:
        //Serial.println("Wrong command");
        break;

      default:
        Serial.println("Should not be able to come here");
    }
  }
  else{
    //send the motor angle through the serial port
    dxl_wb.getPresentPositionData(dxl_id, &Position);
    Position = Position%4095;
    float angle = Position*2*PI/NOMBRE_TIC;
    Serial.println(angle);
    delay(10);
    }
}
