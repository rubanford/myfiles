#include <SoftwareSerial.h>
SoftwareSerial BTserial(4, 5); // RX | TX
// Connect the HC-05 TX to Arduino pin 4 RX. 
// Connect the HC-05 RX to Arduino pin 5 TX through a voltage divider.
void stops()
{
        digitalWrite(0,LOW); 
      digitalWrite(1,LOW); 
      digitalWrite(2,LOW); 
      digitalWrite(3,LOW);
      BTserial.println("object detected,vehicle stopping");
}

void right()
{
        digitalWrite(0,HIGH); 
        digitalWrite(1,LOW); 
        digitalWrite(2,LOW); 
        digitalWrite(3,HIGH);
        BTserial.println("vehicle taking right");
}

void left()
{
          digitalWrite(0,LOW); 
          digitalWrite(1,HIGH); 
          digitalWrite(2,HIGH); 
          digitalWrite(3,LOW);
          BTserial.println("vehicle taking left"); 
}

void moves()
{
         digitalWrite(0,LOW);
         digitalWrite(1,HIGH); 
         digitalWrite(2,LOW); 
         digitalWrite(3,HIGH);
         BTserial.println("vehhicle going forward");
}

void reverse()
{
         digitalWrite(0,HIGH);
         digitalWrite(1,LOW); 
         digitalWrite(2,HIGH); 
         digitalWrite(3,LOW);
         BTserial.println("vehicle taking reverse");
}

void motor(int l1 , int r1)
{
      if((l1==LOW)&&(r1==LOW)) 
    {
      stops();
      delay(1000);
      reverse();
      delay(1000);
      left();
      delay(500);
      
      
    } else if((l1==HIGH)&&(r1==LOW)) {
        //turns right 
        right();
 
    } else if((l1==LOW)&&(r1==HIGH)) {
          //turns left 
          left();

    } else if((l1==HIGH)&&(r1==HIGH)) {
          //Stop the Boot
          moves();

    }
}

void setup() { 

  //left sensor output to arduno input 
  pinMode(7,INPUT); 
  //Right Sensor output to arduino input 
  pinMode(6,INPUT); 
  //output from audrino to motor drive 
  //Right motor audrino to motor Drive 
  pinMode(0,OUTPUT); 
  pinMode(1,OUTPUT); 
  //left Motor Arduino motor Drive 
  pinMode(2,OUTPUT); 
  pinMode(3,OUTPUT);
  Serial.begin(9600);
  BTserial.begin(9600);

   
} 
  void loop() { 
    //left sensor input 
    int x=digitalRead(7); 
    //Right Sensor Input 
    int y=digitalRead(6); 
    motor(x,y);

 }
