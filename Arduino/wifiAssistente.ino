#include <ESP8266WiFi.h>
#include <WiFiUdp.h>


WiFiUDP udp; //Cria um objeto da classe UDP

String req; //String que armazena os dados recebidos pela rede

//configuracoes do Wifi, nome da rede, senha, ip estatico
const char* ssid = "Danilo";
const char* password = "Daniloboy";

IPAddress staticIP(192,168,2,106);
IPAddress gateway(192,168,2,1);
IPAddress subnet(255,255,255,0);

//Configuracoes da classe UDP, a porta para receber msg, e envio de msg


void setup(void)
{
  Serial.begin(115200);
  Serial.println();

  Serial.printf("conectado ao endereco %s\n", ssid);
  WiFi.config(staticIP, gateway, subnet);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Conectado ao IP: ");
  Serial.println(WiFi.localIP());

  udp.begin(555); //inicia a recepcao de dados UDP na porta 555

  pinMode(0, OUTPUT);
  pinMode(2, OUTPUT);
  //define os pinos 0 e 2 como low
  digitalWrite(0, LOW);
  digitalWrite(2, LOW);

}


void loop()
{
  listen(); //sub rotina para verificar se ha pacotes UDP`s a serem lidos
  comando(); //

}

void comando() 
{
  if (req == "acender a luz")
  {
    digitalWrite(0, HIGH);
  }
  else if (req == "apagar a luz")
  {
    digitalWrite(0, LOW);
  }
}

void listen()
{
  if (udp.parsePacket() > 0)// Se houver pacotes para serem lidos
  {
    req = ""; //reseta a string 
    while (udp.available() > 0) //enquanto hover dados para serem lidos
    {
      char z = udp.read(); //adiciona o byte lido em um char
      req += z; //adiciona o char a string
    }

    Serial.println(req);//Print a string recebida 
  }
}
