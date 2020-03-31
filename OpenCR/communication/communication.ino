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

//DXL_ID1 motor id for the rotative scoop (XM) 101
//DXL_ID2 motor id for the endless screw (XL) 224
//DXL_ID3 motor id for the laser (XM) 110
#define NOMBRE_TIC 4096
#define BAUDRATE   57600
#define DXL_ID1    110
#define DXL_ID2    224
#define DXL_ID3    110
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

  uint8_t dxl_id1 = DXL_ID1;
  uint8_t dxl_id2 = DXL_ID2;
  uint8_t dxl_id3 = DXL_ID3;
  uint16_t model_number = 0;
//************************************************************************************************8
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

  result = dxl_wb.ping(dxl_id1, &model_number, &log);
  if (result == false)
  {
    Serial.println(log);
    Serial.println("Failed to ping");
  }
  else
  {
    Serial.println("Succeeded to ping");
    Serial.print("id : ");
    Serial.print(dxl_id1);
    Serial.print(" model_number : ");
    Serial.println(model_number);
  }
  result = dxl_wb.wheelMode(dxl_id1, 0, &log);
  if (result == false)
  {
    Serial.println(log);
    Serial.println("Failed to change wheel mode");
  }
  else
  {
    Serial.println("Succeed to change wheel mode");
  }
  //************************************************************************************************8
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

  result = dxl_wb.ping(dxl_id2, &model_number, &log);
  if (result == false)
  {
    Serial.println(log);
    Serial.println("Failed to ping");
  }
  else
  {
    Serial.println("Succeeded to ping");
    Serial.print("id : ");
    Serial.print(dxl_id2);
    Serial.print(" model_number : ");
    Serial.println(model_number);
  }
  result = dxl_wb.wheelMode(dxl_id2, 0, &log);
  if (result == false)
  {
    Serial.println(log);
    Serial.println("Failed to change wheel mode");
  }
  else
  {
    Serial.println("Succeed to change wheel mode");
  }
  //************************************************************************************************8
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

  result = dxl_wb.ping(dxl_id3, &model_number, &log);
  if (result == false)
  {
    Serial.println(log);
    Serial.println("Failed to ping");
  }
  else
  {
    Serial.println("Succeeded to ping");
    Serial.print("id : ");
    Serial.print(dxl_id3);
    Serial.print(" model_number : ");
    Serial.println(model_number);
  }
  result = dxl_wb.wheelMode(dxl_id3, 0, &log);
  if (result == false)
  {
    Serial.println(log);
    Serial.println("Failed to change wheel mode");
  }
  else
  {
    Serial.println("Succeed to change wheel mode");
  }
  //************************************************************************************************8
  pinMode(laser_pin, OUTPUT);
  pinMode(laser_5V, OUTPUT);
  digitalWrite(laser_5V, HIGH);
  laser_OFF();
}

// change the received command into an integer from 1 to 4
int convert_command(int command) {
    //comment next line
    Serial.println(command);
    int command_number;
    if (command == -1) {
      command_number = 1;
    }
    else if (command == -2) {
      command_number = 2;
    }
    else if (command == -3) {
      command_number = 3;
    }
    else if (command == -4) {
      command_number = 4;
    }
    else if (command == -5) {
      command_number = 5;
    }
    else if (command == -6) {
      command_number = 6;
    }
    else if (command == -7) {
      command_number = 7;
    }
    else if (command == -8) {
      command_number = 8;
    }
    else if (command == -9) {
      command_number = 9;
    }
    else {
      command_number = command;
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
  uint8_t dxl_id1 = DXL_ID1;
  uint8_t dxl_id2 = DXL_ID2;
  uint8_t dxl_id3 = DXL_ID3;
  int32_t Position1 = 0;
  int32_t Position2 = 0;
  int32_t Position3 = 0;
  //get the command from serial port
  if (Serial.available() > 0) {
    int command = Serial.parseInt();
    if(command != 0){
      int command_number = convert_command(command);
      switch (command_number){
  
        //start motor scoop
        case 1:
          //Serial.println("Running");
          laser_ON();
          dxl_wb.wheelMode(dxl_id1, 0);
          dxl_wb.goalVelocity(dxl_id1, (int32_t)10);
          break;
  
        //stop motor scoop
        case 2:
          //Serial.println("Stop");
          laser_OFF();
          dxl_wb.wheelMode(dxl_id1, 0);
          dxl_wb.goalVelocity(dxl_id1, (int32_t)0);
          break;
  
        //restart motor scoop
        case 3:
          //Serial.println("Restarting");
          laser_OFF();
          dxl_wb.jointMode(dxl_id1, 0, 0);
          dxl_wb.goalPosition(dxl_id1, (int32_t)0);
          break;
     
        //start motor screw
        case 4:
          dxl_wb.wheelMode(dxl_id2, 0);
          dxl_wb.goalVelocity(dxl_id2, (int32_t)10);
          break;

        //stop motor screw
        case 5:
          dxl_wb.wheelMode(dxl_id2, 0);
          dxl_wb.goalVelocity(dxl_id2, (int32_t)0);
          break;

        //restart motor screw
        case 6:
          dxl_wb.jointMode(dxl_id2, 0, 0);
          dxl_wb.goalPosition(dxl_id2, (int32_t)0);
          break;

        //start motor laser
        case 7:
          dxl_wb.wheelMode(dxl_id3, 0);
          dxl_wb.goalVelocity(dxl_id3, (int32_t)5);
          break;

        //stop motor laser
        case 8:
          dxl_wb.wheelMode(dxl_id3, 0);
          dxl_wb.goalVelocity(dxl_id3, (int32_t)0);
          break;

        //restart motor laser
        case 9:
          dxl_wb.jointMode(dxl_id3, 0, 0);
          dxl_wb.goalPosition(dxl_id3, (int32_t)0);
          break;
  
        default:
          Serial.println("Should not be able to come here");
          dxl_wb.jointMode(dxl_id1, 0, 0);
          dxl_wb.goalPosition(dxl_id1, (int32_t)command_number);
      }          
    }
  }
  else{
    //send the motor angle through the serial port
    dxl_wb.getPresentPositionData(dxl_id1, &Position1);
    dxl_wb.getPresentPositionData(dxl_id2, &Position2);
    dxl_wb.getPresentPositionData(dxl_id3, &Position3);
    Position1 = Position1%4095;
    Position2 = Position2%4095;
    Position3 = Position3%4095;
    float angle1 = Position1*2*PI/NOMBRE_TIC;
    float angle2 = Position2*2*PI/NOMBRE_TIC;
    float angle3 = Position3*2*PI/NOMBRE_TIC;
    //uncomment next line
    Serial.println(angle1);
    Serial.println(angle2);
    Serial.println(angle3);
    delay(10);
    }
}
