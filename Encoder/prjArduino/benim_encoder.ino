#define ENCA 2 // encoderA
#define ENCB 3 // encoderB
#define PWM 5 //motor controller en
#define IN2 9 //motor controller in2  & encoder + out2
#define IN1 10 //motor controller in1  & encoder - out1

volatile float rpm,out;
volatile float timestep,now;
volatile float prev=0;
volatile int posi = 0;

int kp=100;
int ki=200;
int kd=10;
int vel=100;
const float ts = 0.01;

float Acc=0;
float error_prev=0;
float error;
float u,output;

float PID_output(int kp,int kd, int ki, float ts, float error, float error_prev){
  Acc = Acc +ts*error_prev;
  int P = kp*error;
  int I = ki*Acc;
  int D = kd*(error-error_prev)/ts;
  output = P + I + D;
  error_prev=error;
  return output;
}

void setup() {
  Serial.begin(9600);
  delay(30);
  pinMode(ENCA,INPUT); //read A encoder
  pinMode(ENCB,INPUT); //read B encoder
  attachInterrupt(digitalPinToInterrupt(ENCA),readEncoder,RISING);

  pinMode(PWM,OUTPUT);
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  
  Serial.println("target pos");
}
void loop(){
  
  if(Serial.available()){
    fnActuadores(Serial.readString());
  }
  
  out = rpm/1.412;

  error= vel-out;
  u=PID_output(kp,kd,ki,ts,error,error_prev);

  if(u>255)
  {
    u=255;
  }
  if(u<0)
  {
    u=0;
  }

  // motor direction
  int dir = 1;
    if(u<0){
      dir = -1;
    }
    
  // signal the motor   
  setMotor(dir,output,PWM,IN1,IN2);


  Serial.print(posi);
  Serial.println();
}

void setMotor(int dir,int pwmVal, int pwm, int in1, int in2){
  analogWrite(pwm,pwmVal);
  if(dir == 1){
    digitalWrite(in1,HIGH);
    digitalWrite(in2,LOW);
  }
  else if(dir == -1){
    digitalWrite(in1,LOW);
    digitalWrite(in2,HIGH);
  }
  else{
    digitalWrite(in1,LOW);
    digitalWrite(in2,LOW);
  }  
}

void fnActuadores(String cad){
  int pos;
  String label,value;
  cad.trim();
  cad.toLowerCase();
  pos = cad.indexOf(':');
  label= cad.substring(0,pos);
  value= cad.substring(pos+1); 

  if (label.equals("KP")){
    if(kp != value.toInt()){
      kp = value.toInt();  
    }    
  }
  if (label.equals("KI")){
    if(ki != value.toInt()){
      ki = value.toInt();  
    }    
  }
  if (label.equals("KD")){
    if(kd != value.toInt()){
      kd = value.toInt();  
    }    
  }
  if (label.equals("VEL")){
    if(vel != value.toInt()){
      vel = value.toInt();  
    }    
  }
}
void readEncoder(){
  now = micros();
  timestep = now -prev;
  prev=now;
  rpm = 60*1000000/(24*timestep);
  int b = digitalRead(ENCB);
  if(b > 0){
    posi++;
  }
  else{
    posi--;
  }
}
