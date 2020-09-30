//Teste com Sensor de temperatura e luz
//Autor: Danilo

#include<limits.h>
#include<LiquidCrystal.h>
#include<Thermistor.h>

const int sensorLuz = 7; // Define o pino analogico que se encontra o sensor de luz
const int sensorTemperatura = 0; //Define pino analofico que se encontra o sensor de temperatura

//Pinos que serão utilizados no LCD
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

//Variaveis
int valorLuz = 0; //le o valor do sensor de luz
int valorTemp = 0; //le o valor do sensor de temperatura
int menorValor = INT_MAX; //armazena o menor valor da temperatura
void setup()
{
  //inicializa o LCD 
  lcd.begin(16, 2);
}

void loop()
{
  //le o valor do sensor de luz
  valorLuz = analogRead(sensorLuz);

  //Para mais precisao, sao feitas 8 leituras
  menorValor = INT_MAX;
  for (int i = 1; i<= 8; i++){
    valorTemp = analogRead(sensorTemperatura);
    //converte o valor lido em graus celsius
    valorTemp *= 0.54;
    //mantem o menor valor lido
    if (valorTemp < menorValor){
      menorValor = valorTemp;
    }
    delay(200);
  }

  //Exibe o valor da leitura do sensor de temperatura no LCD
  lcd.clear();
  lcd.print("Temp: ");
  lcd.print(menorValor);
  lcd.write(B11011111);
  lcd.print("C");

  //Exibe o valor da leitura do sensor de luz
  lcd.setCursor(0,1);
  lcd.print("Luz: ");
  lcd.print(valorLuz);

  delay(2000);
  
}
