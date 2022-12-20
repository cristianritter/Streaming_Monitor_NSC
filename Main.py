"""         Streaming Monitor        - Main File -        'Main.py'         """
"""     Este aplicativo realiza a monitoração dos streamings e dispara um aviso no Zabbix em caso de anormalidades    """

"""     INFORMAÇÕES DO DESENVOLVEDOR    """

__author__ = "Cristian Ritter"
__copyright__ = "EngNSC 2023"
__credits__ = ["",]
__license__ = "GPL"
__version__ = "v1.0.0"
__maintainer__ = "Cristian Ritter"
__email__ = "cristianritter@gmail.com"
__status__ = "Production" 


"""     REQUIREMENTS     """
import wx
from threading import Thread
from LibFileOperations import FileOperations
from LibGravacao import Gravacao
from LibAnalyzer import Analyzer
from LibSaveLogFile import SaveLogFile
from time import sleep
from LibZabbixSender import MyZabbixSender
from LibTaskBar import TaskBarIcon
from LibWXInitLlocaleFix import InitLocale

FileOperations_ = FileOperations()
config = FileOperations_.read_json_from_file('config.json')

def realtime_monitor(metrica, nome):
    Analyzer_ = Analyzer()
    Gravacao_ = Gravacao()
    
    for instance in config['zabbix_instances'].keys():
        MyZabbixSender(metric_interval=config['zabbix_instances'][instance]['send_metrics_interval'],
        hostname=config['zabbix_instances'][instance]['hostname'],
        server=config['zabbix_instances'][instance]['server_ip'],
        port=config['zabbix_instances'][instance]['port'],
        key=config['instancias'][nome]['zabbix_key'],
        metrica=metrica
        )
    
    while True:
        try:
            filename = f'R:\\{nome}.wav'
            record_result = Gravacao_.gravar_trecho_de_streaming(config['instancias'][nome]['link'], filename)
            if (record_result != 0):
                print(f"Erro na gravação de {nome}")
                metrica[0] |= (1<<2)
            else:
                pass
                metrica[0] &= ~(1<<2)
            
            if not FileOperations_.verificar_file_exists(filename):
                continue
            
            audio_data = FileOperations_.read_wav_file(filename)
            silence_ch_status = Analyzer_.verifica_silencio(audio_data, config['instancias'][nome]['silence_offset'])
            
            for idx, channel in enumerate(silence_ch_status):
                if channel:
                    print(f'Silence in CH{idx}')
                    metrica[0] |= (1<<idx)
                else:
                    metrica[0] &= ~(1<<idx)

            sleep(10)
        except:
            pass

def Main():
    t = []
    metrica = []
    for idx, nome in enumerate(config['instancias'].keys()):
        metrica.append([0,])
        #print(type(metrica[idx]))
        t.append(Thread(target=realtime_monitor, args=(metrica[idx], nome), daemon=True))
        t[idx].start()

    wx.App.InitLocale = InitLocale
    app = wx.App()   #criação da interface gráfica
    TaskBarIcon(f"Radio Streaming Monitor") 
    app.MainLoop()

Main()