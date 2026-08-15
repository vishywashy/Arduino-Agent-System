const int ledpinred = 7;
int i;
long duration;//date time datatype
float distance;
const int trig_pin = 12;
const int echo_pin = 10;
void setup() {
  Serial.begin(9600);
  pinMode(ledpinred, OUTPUT);
  pinMode(trig_pin, OUTPUT);
  pinMode(echo_pin, INPUT);

  // put your setup code here, to run once:

}

void loop() {
  if (Serial.available()>0){
      String command = Serial.readStringUntil('\n');
      command.trim();
      if (command == "red on"){
          digitalWrite(ledpinred, HIGH);
        
          
          
    }
    else if (command == "red off"){
      digitalWrite(ledpinred, LOW);
    
 
    }
  }
  digitalWrite(trig_pin, LOW);//Make sure it is low
  delayMicroseconds(2);//2 microseconds.
  digitalWrite(trig_pin, HIGH);//Turns it high
  delayMicroseconds(10);//Keeps it for that duration
  digitalWrite(trig_pin, LOW);//Then turns it low
  duration = pulseIn(echo_pin, HIGH);//Checks the amount of time that the echo_pin was on to check the signal
  distance = duration*0.034/2;//cm per microseconds. Calculates distance by using speed/time and dividing by two as signal travels twice the distance
  Serial.println(distance);
  
  

  
  // put your main code here, to run repeatedly:

}
