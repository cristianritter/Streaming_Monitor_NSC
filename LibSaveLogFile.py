from datetime import datetime, timedelta
import os

class SaveLogFile:
    def __init__(self) -> None:
        configuration = LibParseConfig.ConfPacket()
        configs = configuration.load_config('FILES')
        saved_files_folder = os.path.join(configs['FILES']['saved_files_folder'])
        if (not os.path.exists(self.log_folder)):                        # Se não existir o diretório é criado
            os.makedirs(self.log_folder)

    def adiciona_linha_log(self, texto, time_offset=0):
            dataFormatada = (datetime.now()+timedelta(seconds=time_offset)).strftime('%d/%m/%Y %H:%M:%S')
            mes_ano = (datetime.now()+timedelta(seconds=time_offset)).strftime('_%Y%m')
            try:
                filename = 'log'+mes_ano+'.txt'
                logfilepath = os.path.join(self.log_folder, filename)
                f = open(logfilepath, 'a')
                f.write(dataFormatada + " " + str(texto) +"\n")
                f.close()
            except Exception as err:
                print(dataFormatada, "LibSaveLogFile: ERRO ao adicionar linha log: ", err)
                self.adiciona_linha_log(str(err))

if __name__ == '__main__':
    SaveLogFile_ = SaveLogFile()
    SaveLogFile_.adiciona_linha_log('Teste de texto')