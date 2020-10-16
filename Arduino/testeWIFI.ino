#include <ESP8266WiFi.h>

//criar um server na porta 80
WiFiServer server(80);

void setup()
{
  //inicia a serial
  Serial.begin(115200);

  //configura a GPI00 e 02 como output (saida)
  pinMode(0, OUTPUT);
  pinMode(2, OUTPUT);
  //GPI00 e 02 LOW
  digitalWrite(0, LOW);
  digitalWrite(2, LOW);

  Serial.print("Conectado");
  //Conecta o ESP01 ao WIFI, SSID da rede e senha
  WiFi.begin("Danilo", "Daniloboy");

  //Menssagem enquanto nao estiver conectado a rede
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(100);
    Serial.println(".");
  }

  //feedback do monitor serial quando conectar
  Serial.println("");
  Serial.println("conectado");

  //Configuração para IP FIXO
  IPAddress ip(192, 168, 2, 106);
  IPAddress gateway(192, 168, 2, 1);
  IPAddress subnet(255, 255, 255, 0);
  Serial.print("configurando IP FIXO para: ");
  Serial.println(ip);

  //Envia configuração de ip
  WiFi.config(ip, gateway, subnet);
  //inicia o server na porta 80
  server.begin();
  //mostra no monitor serial o IP do ESP
  Serial.print("servidor em: ");
  Serial.println(WiFi.localIP());
}

void loop()
{
  //verifica se o cliente esta tentando conectar
  WiFiClient client = server.available();
  if (!client)
  {
    return;
  }
  
  Serial.println("cliente conectado");
  //Leitura da requisição
  String req = client.readStringUntil('\r');
  Serial.print("Requisição: ");
  Serial.println(req);

  //inicio do html, com botao de off e on

  String html = 
  "<html>"
    "<head>"
      "<meta name='viewport' content='width=device-width, initial-scale=1, user-scalable=no'/>"
      "<title>ESP8266</title>"
      "<style>"
        "body{"
          "text-align: center;"
          "font-family: sans-serif;"
          "font-size:14px;"
          "padding: 25px;"
        "}"

        "p{"
          "color:#444;"
        "}"

        "button{"
          "outline: none;"
          "border: 2px solid #1fa3ec;"
          "border-radius:18px;"
          "background-color:#FFF;"
          "color: #1fa3ec;"
          "padding: 10px 50px;"
        "}"

        "button:active{"
          "color: #fff;"
          "background-color:#1fa3ec;"
        "}"
      "</style>"
    "</head>"
    "<body>"
    "<p>GPIO0</p>"
    "<p><a href='?acao=gpio0On'><button>ON</button></a></p>"
    "<p><a href='?acao=gpio0Off'><button>OFF</button></a></p>"
    "<p>GPIO2</p>"
    "<p><a href='?acao=gpio2On'><button>ON</button></a></p>"
    "<p><a href='?acao=gpio2Off'><button>OFF</button></a></p>"
    "</body>"
  "</html>";
  //escrever o html no buffer que sera enviado ao cliente
  client.print(html);
  //envia os dados do buffer para o cliente
  client.flush();

  //verifica se a requisicao possui acao gpio0
  if (req.indexOf("acao=gpio0On") != -1)
  {
    digitalWrite(0, HIGH);
  }
  else if (req.indexOf("acao=gpio0Off") != -1)
  {
    digitalWrite(0, LOW);
  }
  else if (req.indexOf("acao=gpio2On") != -1)
  {
    digitalWrite(2, HIGH);
  }
  else if (req.indexOf("acao=gpio2Off") != -1)
  {
    digitalWrite(2, LOW);
  }
  
  //Fecha a conexao com o cliente
  client.stop();
  Serial.println("cliente desconectado");

}
