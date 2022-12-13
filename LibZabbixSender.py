from pyzabbix import ZabbixMetric, ZabbixSender
import time
from threading import Thread


class MyZabbixSender:
    """
    Classe que implementa o sistema de envio de metricas para o Zabbix \n
    Recebe os seguintes parametros: \n
    metric_interval - intervalo entre o envio das metricas para o servidor \n
    hostname - zabbix hostname \n
    key - zabbix key \n
    server - zabbix serve ip address \n
    port - zabbix port number \n
    idx -  indice da variavel de lista que possui os dados de metrica a serem enviados \n
    status - lista que traz os dados de metrica

    """
    def __init__(self, metric_interval, hostname, key, server, port, metrica):
        self.metric_interval = int(metric_interval)
        self.hostname = hostname
        self.key = key
        self.server = server
        self.port = int(port)
        self.metrica = metrica
        u = Thread(target=self.send_metric, daemon=True)
        u.start()
        
    def send_metric(self):
        '''Rotina que continuamente envia as metricas               
        Recebe um array do tipo lista e utiliza os dados de indice da classe criada. Funcionam como ponteiro, \n
        portanto ao alterar os valores na lista se altera também o valor da metrica enviada.
        '''
        try:
            while True:
                print(self.metrica)
                time.sleep(self.metric_interval)       
                texto_metrica = ""
                #print(type(self.metrica))
                if (self.metrica[0] & (1<<0)):
                    texto_metrica += ' rightsilence'
                if (self.metrica[0] & (1<<1)): #or produto):
                    texto_metrica += ' leftsilence'
                if (self.metrica[0] & (1<<2)): #or produto):
                    texto_metrica += ' linkdown'    
                if (not self.metrica[0]):
                    texto_metrica = "operacaonormal"

                try:
                    packet = [
                        ZabbixMetric(self.hostname, self.key, texto_metrica)
                    ]
                    ZabbixSender(zabbix_server=self.server, zabbix_port=self.port).send(packet)
                except Exception as Err:
                    print(f"Falha de conexão com o Zabbix - {Err}")
        except Exception as Err:
            print(f"Erro: {Err}")
            time.sleep(30)

if __name__ == '__main__':
    """
    Metodo que permite testar a funcao individualmente e fornece um exemplo de uso
    """
    HOSTNAME = "FLS - SERVER-RADIOS"
    ZABBIX_SERVER = "10.51.23.101"
    PORT = 10051
    SEND_METRICS_INTERVAL = 5
    data = [1]
    zsender = ZabbixSender(SEND_METRICS_INTERVAL, HOSTNAME, 'key', ZABBIX_SERVER, PORT, 0, data )
    zsender.start_zabbix_thread()
    while(True):
        time.sleep(1)
        pass