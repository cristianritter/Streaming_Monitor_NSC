from threading import Thread
from LibFileOperations import FileOperations
from LibGravacao import Gravacao
from LibAnalyzer import Analyzer
from LibSaveLogFile import SaveLogFile
from time import sleep
from LibZabbixSender import ZabbixSender

FileOperations_ = FileOperations()
config = FileOperations_.read_json_from_file('config.json')

def realtime_monitor(nome):
    Analyzer_ = Analyzer()
    Gravacao_ = Gravacao()
    ZabbixSender(metric_interval=config['instancias'][nome]['send_metrics_interval'],
    hostname=config['instancias'][nome]['hostname'],
    server=config['instancias'][nome]['server_ip'],
    port=config['instancias'][nome]['port']
    key=config['instancias'][nome]['key'],
    idx=,
    status=
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
    for nome in config['instancias'].keys():
        t.append(Thread(target=realtime_monitor(nome), daemon=True))

Main()