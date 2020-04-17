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

//initiate and test if the designated motor respond
void init_motor(int motor)
{
  uint16_t model_number = 0;
  const char *log;
  bool result = false;
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

  result = dxl_wb.ping(motor, &model_number, &log);
  if (result == false)
  {
    Serial.println(log);
    Serial.println("Failed to ping");
  }
  else
  {
    Serial.println("Succeeded to ping");
    Serial.print("id : ");
    Serial.print(motor);
    Serial.print(" model_number : ");
    Serial.println(model_number);
  }
  result = dxl_wb.wheelMode(motor, 0, &log);
  if (result == false)
  {
    Serial.println(log);
    Serial.println("Failed to change wheel mode");
  }
  else
  {
    Serial.println("Succeed to change wheel mode");
  }
}

int motor_number_to_int(String motor_number)
{
  if (motor_number == "1"){
    return DXL_ID1;
  }
  if (motor_number == "2"){
    return DXL_ID2;
  }
  if (motor_number == "3"){
    return DXL_ID3;
  }
  else {
    Serial.println("wrong motor number input");
    return -1;
  }
}

int motor_command_to_int(String motor_command)
{
  if (motor_command == "start"){
    return 1;
  }
  if (motor_command == "stop"){
    return 2;
  }
  if (motor_command == "restart"){
    return 3;
  }
  if (motor_command == "position"){
    return 4;
  }
  else {
    return 5;
  }
}

int motor_argument_to_int(String motor_argument)
{
  int argument = motor_argument.toInt();
  return argument;
}

void laser_ON(){
  digitalWrite(laser_pin, HIGH);
}

void laser_OFF(){
 digitalWrite(laser_pin, HIGH);
}

void setup()
{
  Serial.begin(9600);
  // uncomment next line to wait for Opening Serial Monitor
  //while(!Serial); 

  uint8_t dxl_id1 = DXL_ID1;
  uint8_t dxl_id2 = DXL_ID2;
  uint8_t dxl_id3 = DXL_ID3;
  init_motor(dxl_id1);
  init_motor(dxl_id2);
  init_motor(dxl_id3);
  pinMode(laser_pin, OUTPUT);
  pinMode(laser_5V, OUTPUT);
  digitalWrite(laser_5V, HIGH);
  laser_OFF();
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
    //String command_received = Serial.readString();
    String command_received = Serial.readString();
    if(command_received != 0){
      //*************************************************************
      int n = command_received.length();
      // declaring character array
      char char_array[n + 1];
      // copying the contents of the
      // string to char array
      strcpy(char_array, command_received.c_str());
      const char s[2] = "-";
      char *token;
      String info_command[3];

      /* get the first token */
      token = strtok(char_array, s);
      info_command[0] = token;
      int command_number = 1;
      /* walk through other tokens */
      while ( token != NULL ) {
         token = strtok(NULL, s);
         info_command[command_number] = token;
         command_number = command_number + 1;
         if (command_number == 3){
           token = NULL;
           //Serial.println("max iteration reached");
         }
      }
      //***************************************************************
      String motor_number = info_command[0];
      String motor_command = info_command[1];
      String motor_argument = info_command[2];

      //convert string to int
      int motor_number_int = motor_number_to_int(motor_number);
      int motor_command_int = motor_command_to_int(motor_command);
      int motor_argument_int = motor_argument_to_int(motor_argument);

      switch (motor_command_int) {

        //start
        case 1:
          laser_ON();
          if (motor_argument_int > 500){
             motor_argument_int = 1000 - motor_argument_int;
          }
          dxl_wb.wheelMode(motor_number_int, 0);
          dxl_wb.goalVelocity(motor_number_int, (int32_t)motor_argument_int);
          break;

        //stop
        case 2:
          laser_OFF();
          dxl_wb.wheelMode(motor_number_int, 0);
          dxl_wb.goalVelocity(motor_number_int, (int32_t)0);
          break;

        //restart
        case 3:
          laser_OFF();
          dxl_wb.jointMode(motor_number_int, 0, 0);
          dxl_wb.goalPosition(motor_number_int, (int32_t)0);
          break;

         //go_to_position
        case 4:
          dxl_wb.jointMode(motor_number_int, 0, 0);
          dxl_wb.goalPosition(motor_number_int, (int32_t)motor_argument_int);
          break;
          
        case 5:
          Serial.println("wrong motor command");
          break;
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
    Serial.println(angle1);
    Serial.println(angle2);
    Serial.println(angle3);
    delay(10);
    }
}
