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
from LibZabbixSender import ZabbixSender
from LibTaskBar import TaskBarIcon

FileOperations_ = FileOperations()
config = FileOperations_.read_json_from_file('config.json')

status = {}
for key in config['instancias'].keys():
    status[key] = 0

def realtime_monitor(nome, status):
    Analyzer_ = Analyzer()
    Gravacao_ = Gravacao()
    ZabbixSender(metric_interval=config['zabbix']['send_metrics_interval'],
    hostname=config['zabbix']['hostname'],
    server=config['zabbix']['server_ip'],
    port=config['zabbix']['port'],
    key=config['instancias'][nome]['zabbix_key'],
    nome=nome,
    status=status
    )

    while True:
        filename = f'R:\\{nome}.wav'
        Gravacao_.gravar_trecho_de_streaming(config['instancias'][nome]['link'], filename)
        audio_data = FileOperations_.read_wav_file(filename)
        clipped_ch_status = Analyzer_.verificar_clipped(audio_data)
        if clipped_ch_status:
            print('Cliped')
        silence_ch_status = Analyzer_.verifica_silencio(audio_data, config['instancias'][nome]['silence_offset'])
        for idx, channel in enumerate(silence_ch_status):
            if channel:
                print(f'Silence in CH{idx}')          
        sleep(10)

def Main():
    t = []
    for idx, nome in enumerate(config['instancias'].keys()):
        t.append(Thread(target=realtime_monitor, args=(nome, status), daemon=True))
        t[idx].start()
    app = wx.App()   #criação da interface gráfica
    TaskBarIcon(f"Radio Streaming Monitor") 
    app.MainLoop()

Main()