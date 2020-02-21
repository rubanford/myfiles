
#define AnalogPin A0
#define DigitalPin 12

int ana;
bool digi;
void setup() {
  // put your setup code here, to run once:
  pinMode(AnalogPin,INPUT);
  pinMode(DigitalPin,INPUT);
  pinMode(13,OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  ana = analogRead(AnalogPin);
  digi = digitalRead(DigitalPin);

  if(digi==1)
  {
    digitalWrite(13,HIGH);
  }
  else if(digi==0)
  {
    digitalWrite(13,LOW);
  }

}
