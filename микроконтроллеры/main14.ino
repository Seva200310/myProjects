#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include "TFLidar.h"
// Библиотека для работы программного Serial
#include <SoftwareSerial.h>
#include <SPI.h>
#include <SD.h>
#include <GyverOLED.h>
const int chipSelect = 10;
GyverOLED<SSD1306_128x64, OLED_NO_BUFFER> oled;

//В предыдущей версии тут была функция oled_print, на вход она принимала размер текста и сам текст,тут ее нет,но в коде осталась
//Идея следующая. Пользователь сначала отмечает лазером точку наблюдения,затем подходит к ней, прислоняется к ней спиной и может оттуда отметить либо линию(массив точек) 
//либо точку пикета(одна точка) либо новую точку обзора.

uint8_t fifoBuffer[45];    
//для лидара
// Serial-порт к которому подключён дальномер
#define LIDAR_SERIAL1    mySerial1
SoftwareSerial mySerial1(7,8);
TFLidar lidar1;
int dist1;
short  btn_line_ratt=0;
short  btn_piket_ratt=0;
short  btn_view_ratt=0;
short  btn_accept_ratt=0;
short  btn_decline_ratt=0;

#define laser_pin 5
#define confirmation_lamp 3
//для MPU 
MPU6050 mpu;
struct angles
{
float yaw;
float pitch;
float roll;
} ;
struct point{
   float coords[3];
};
point view_point;
point view_point_new;
angles ang;
point point_meas;
#define max_point 3
point line_point_arr[max_point];
short int array_len=0;
point piket;
bool unsaved_changes_view;
bool unsaved_changes_piket;
bool unsaved_changes_line;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  Serial.print("alive ");
  mpu.initialize();
  Serial.print("initmpu ");
  mpu.dmpInitialize();
  Serial.print("initdmp");
  mpu.setDMPEnabled(true);//Инициализация MPU

  Serial.print("alive ");

  pinMode(chipSelect,OUTPUT);
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");//Инициализация SD карты 
  }
  oled.init();        // инициализация
  oled.clear();       // очистка
  oled.setScale(2);   // масштаб текста (2)
  oled.home(); 
  oled.print("Вкл"); 
  pinMode(A0, INPUT_PULLUP);
  pinMode(A1, INPUT_PULLUP);
  pinMode(A2, INPUT_PULLUP);
  pinMode(A3, INPUT_PULLUP);
  pinMode(4, INPUT_PULLUP);//Инициализация кнопок
  //Serial.print("oled a;ive");
}


void loop() {

bool btn_line=digitalRead(A1);
bool btn_view_point=digitalRead(A2);
bool btn_piket=digitalRead(A0);

if (!btn_line){btn_line_ratt+=1;}
  else{btn_line_ratt=0;}
if (!btn_piket){btn_piket_ratt+=1;}
  else{btn_piket_ratt=0;}
if (!btn_view_point){btn_view_ratt+=1;}
  else{btn_view_ratt=0;}//Предотвращение дребезжания контакта

if (((btn_line_ratt+btn_piket_ratt+btn_view_ratt)==0)||array_len>=max_point) {//Если не будет нажата ни одна кнопка либо количество точек превысет допустимое
    digitalWrite(laser_pin, 0);//выключаем лазер
    if(array_len>=max_point){//если превышено количество точек в линии
      oled_print(2,"ovf");
    }
    if(unsaved_changes_view||unsaved_changes_line||unsaved_changes_piket){//если есть несохраненные точки
    bool btn_accept=digitalRead(A3);
    bool btn_decline=digitalRead(4);
    if (!btn_accept){btn_accept_ratt+=1;}
      else{btn_accept_ratt=0;}
    if (!btn_decline){
      btn_decline_ratt+=1;
      //Serial.println(btn_decline_ratt);
    }
      else{btn_decline_ratt=0;}
    digitalWrite(confirmation_lamp, HIGH);//зажигаем сигнальный светодиодик
    oled_print(2,"Сохранить изменения?");
    if(btn_accept_ratt==5){
        digitalWrite(confirmation_lamp, LOW);
        Serial.println("Изменения сохранены");
        oled_print(2,"Изменения сохранены");
        if(unsaved_changes_view){save_view();}
        if(unsaved_changes_line){save_line();}
        if(unsaved_changes_piket){save_piket();}//сохраняем несохраненные данные
        array_len=0;

        btn_decline_ratt=0;
        btn_accept_ratt=0;
        btn_view_ratt=0;
        btn_line_ratt=0;
        btn_piket_ratt=0;//обнуляем счетчики кнопок

        unsaved_changes_view=false;
        unsaved_changes_line=false;
        unsaved_changes_piket=false;
        }

    else if(btn_decline_ratt==5){
      digitalWrite(confirmation_lamp, LOW);
        Serial.println("Изменения не сохранены");
        oled_print(2,"Изменения не сохранены");
        array_len=0;

        btn_decline_ratt=0;
        btn_accept_ratt=0;
        btn_view_ratt=0;
        btn_line_ratt=0;
        btn_piket_ratt=0;//обнуляем счетчики кнопок

        unsaved_changes_view=false;
        unsaved_changes_line=false;
        unsaved_changes_piket=false;
    }


    }
  oled_print(2,"Вкл");
    
  } 


else if(btn_view_ratt==5){
  btn_view_ratt=0;
  //Serial.print(',');
  digitalWrite(laser_pin, HIGH);
  ang=get_angles();
  get_dist();
  delay(50);
  view_point_new=calc_point(ang,view_point,dist1);
  oled_print(2,"Точка обзора");
  Serial.println("Новая точка обзора");
  unsaved_changes_view=true;
  unsaved_changes_line=false;
  unsaved_changes_piket=false;
}
else if(btn_piket_ratt==5){
  btn_piket_ratt=0;
  //Serial.print(',');
  digitalWrite(laser_pin, HIGH);

  ang=get_angles();
  //Serial.print(ang.yaw); // вокруг оси Z
  //Serial.print(',');
  //Serial.print(ang.roll); // вокруг оси Y
  //Serial.print(',');
  //Serial.print(ang.pitch); // вокруг оси X
  //Serial.print(',');
  get_dist();
  //Serial.print(dist1);
  //Serial.println();
  //view_point.coords={0,0,0};
  delay(50);
  piket=calc_point(ang,view_point,dist1);
  oled_print(2,"Точка пикета");
  //Serial.print("точка пикета:");
  unsaved_changes_piket=true;
  unsaved_changes_view=false;
  unsaved_changes_line=false;
  Serial.print("точка пикета:");
  Serial.print(point_meas.coords[0]);
  Serial.print(',');
  Serial.print(point_meas.coords[1]);
  Serial.print(',');
  Serial.print(point_meas.coords[2]);
  Serial.print("расстояне:");
  Serial.print(dist1);
  Serial.println();
 
}
else if(btn_line_ratt==5){
  btn_line_ratt=0;
  //Serial.print(',');
  digitalWrite(laser_pin, HIGH);
  ang=get_angles();
  //Serial.print(ang.yaw); // вокруг оси Z
  //Serial.print(',');
  //Serial.print(ang.roll); // вокруг оси Y
  //Serial.print(',');
  //Serial.print(ang.pitch); // вокруг оси X
  //Serial.print(',');
  get_dist();
  //Serial.print(dist1);
  //Serial.println();
  //view_point.coords={0,0,0};
  delay(50);
  point_meas=calc_point(ang,view_point,dist1);
  line_point_arr[array_len]=point_meas;
  array_len+=1;

  oled_print(2,"Точка линии");
  unsaved_changes_line=true;
  unsaved_changes_piket=false;
  unsaved_changes_view=false;
  Serial.print(point_meas.coords[0]);
  Serial.print(';');
  Serial.print(point_meas.coords[1]);
  Serial.print(';');
  Serial.print(point_meas.coords[2]);
  Serial.print(";");
  Serial.println("Линия записана");
  /*Serial.print("точка пикета:");
  Serial.print(point_meas.coords[0]);
  Serial.print(',');
  Serial.print(point_meas.coords[1]);
  Serial.print(',');
  Serial.print(point_meas.coords[2]);
  Serial.print("расстояне:");
  Serial.print(dist1);
  Serial.println();*/
}

}





struct angles get_angles(){//получаем углы ориентации с mpu

  if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) {
    // переменные для расчёта (ypr можно вынести в глобал)
    Quaternion q;
    VectorFloat gravity;
    float ypr[3];
    // расчёты
    mpu.dmpGetQuaternion(&q, fifoBuffer);
    mpu.dmpGetGravity(&gravity, &q);
    mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
    angles ang = {ypr[2],ypr[1],ypr[0]};
    //ang.roll=ypr[2]*57.3;
    //ang.pitch=ypr[1]*57.3;
    //ang.yaw=ypr[0]*57.3;
    // выводим результат в радианах (-3.14, 3.14)
    // для градусов можно использовать degrees()
    return ang;
  }
}

/*void turn_laser(int mode){//функция включения лазера
    digitalWrite(laser_pin, mode);
}*/

void get_dist(){//получаем расстояение от лидара
  mySerial1.begin(115200);
  lidar1.begin(&LIDAR_SERIAL1);
  lidar1.getData(dist1);    
}

struct point calc_point(struct angles ang,struct point view_point,int dist){//расчитываем точку
  float res_vector[3]={0,0,0};

  float roll=ang.roll;
  float pitch=ang.pitch;
  float yaw=ang.yaw;


  
  //Serial.print(roll); // вокруг оси X
  //Serial.print(',');
  //Serial.print(pitch); // вокруг Y
  //Serial.print(',');
  //Serial.print(yaw); // вокруг оси Z
  //Serial.println();

  float rotation_matrix[3][3] = {
        {(cos(roll) * cos(pitch)),  (cos(roll) * sin(pitch) * sin(yaw) - sin(roll) * cos(yaw)),     (cos(roll) * sin(pitch) * cos(yaw) + sin(roll) * sin(yaw))},
        {(sin(roll) * cos(pitch)),  (sin(roll) * sin(pitch) * sin(yaw) + cos(roll) * cos(yaw)),   (sin(roll) * sin(pitch) * cos(yaw) - cos(roll) * sin(yaw))},
        {(-sin(pitch)) ,cos(pitch) * sin(yaw),cos(pitch) * cos(yaw)}
    };//матрица поворота
  //dist=134;
  int base_vector[3]={0,0,0};
  base_vector[0]=dist;
  int i;
    int j;
    for (i = 0; i < 3; i++) {
        for (j = 0; j < 3; j++) {
            res_vector[i] = res_vector[i]+ base_vector[j] * rotation_matrix[i][j];
        }
    }
  point point_meas;
  for (i = 0; i < 3; i++){
    point_meas.coords[i]=view_point.coords[i]+res_vector[i];
  }
  delay(100);
  //Serial.print("точка:");
  //Serial.print(point_meas.coords[0]);
  //Serial.print(',');
  //Serial.print(point_meas.coords[1]);
  //Serial.print(',');
  //Serial.print(point_meas.coords[2]);
  //Serial.print("расстояне:");
  //Serial.print(dist);
  //Serial.println();
  return point_meas;

}

bool compare_points(struct point point_a,struct point point_b){//находим новую точку относительно точки обзора
  bool res=true;
  for(int i=0;i<3;i++){
    if(point_a.coords[i]!=point_b.coords[i]){
      res=false;
    }
  }
  return res;
}

void save_piket(){//сохраняем пикет
          File dataFile = SD.open("pikets.txt", FILE_WRITE);
          Serial.println("file pikets");
        delay(50);
        if (dataFile) {
          // записываем строку в файл
          dataFile.print(piket.coords[0]);
          dataFile.print(',');
          dataFile.print(piket.coords[1]);
          dataFile.print(',');
          dataFile.print(piket.coords[2]);
          dataFile.println(";");
          Serial.println("Пикет записан");
          dataFile.close();
        } else {
        // выводим ошибку если не удалось открыть файл
          Serial.println("error opening file line");
        }
        }  
void save_line(){//сохранение линии
          File dataFile = SD.open("lines.txt", FILE_WRITE);
          Serial.println("file line");
          delay(50);
        if (dataFile) {
          // записываем строку в файл
          for(int i = 0; i < array_len; ++i){
            dataFile.print(line_point_arr[i].coords[0]);
            dataFile.print(',');
            dataFile.print(line_point_arr[i].coords[1]);
            dataFile.print(',');
            dataFile.print(line_point_arr[i].coords[2]);
            dataFile.println(';');
            Serial.println("Линия записана");}
            dataFile.close();
          } else {
            // выводим ошибку если не удалось открыть файл
            Serial.println("error opening file line");
         }  
}

void save_view(){//
        view_point.coords[0]=view_point_new.coords[0];
        view_point.coords[1]=view_point_new.coords[1];
        view_point.coords[2]=view_point_new.coords[2];
        }


