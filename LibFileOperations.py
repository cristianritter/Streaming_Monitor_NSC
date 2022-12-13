from datetime import datetime, timedelta
import os
import json
from subprocess import check_output
import soundfile as sf

class FileOperations:
    def __init__(self) -> None:
        pass
    
    def verificar_diretorios(self, *args):
        """Verifica a existência dos diretórios informados como uma tupla nos argumentos. Caso os dirtórios não existam eles serão criados."""
        print(f"Verificando a existência de diretórios necessários: \n {args}")
        for dir in args:
            if not os.path.exists(dir):
                os.makedirs(dir)
        
    def verificar_file_exists(self, dir, *args):
        """Verifica a existência do arquivo informado no argumento. Retorna true or false."""
        return os.path.isfile(dir)
        
    def adiciona_linha_log(self, texto, dir, time_offset=0):
        ("""Adiciona as informações do texto ao arquivo incluindo informações de data e hora, também imprime a informação no terminal"""
        """Recebe como argumentos o texto a er adicionado e o diretorio onde os arquivos da instancia sao salvos""")
        log_folder = os.path.join(dir, "logs")
        if (not os.path.exists(log_folder)):                        # Se não existir o diretório é criado
            os.makedirs(log_folder)
        dataFormatada = (datetime.now()+timedelta(seconds=time_offset)).strftime('%d/%m/%Y %H:%M:%S')
        mes_ano = (datetime.now()+timedelta(seconds=time_offset)).strftime('_%Y%m')
        try:
            filename = 'log'+mes_ano+'.txt'
            logfilepath = os.path.join(log_folder, filename)
            f = open(logfilepath, 'a')
            info = f'{dataFormatada} {texto} \n'
            f.write(info)
            f.close()
            print(info)
        except Exception as err:
            erro = f'{dataFormatada} adiciona_linha_log: {err}' 
            print(erro)

    def save_json_to_file(self, filename, dict_data):
        """     Salva o conteúdo de um dicionário para arquivo no formato Json"""
        try:
            """Salva dados em arquivo"""
            data_to_write = json.dumps(dict_data, indent = 4) 
            with open(filename, 'w') as infile:
                infile.write(data_to_write)
            return 1
        except Exception as Err:
            print(Err, 'salvando aquivo')
            return 0            

    def read_json_from_file(self, filename):
        """     Carrega o conteúdo de um arquivo no formato Json para um dicionário"""
        try:
            """Le dados do arquivo"""
            with open(filename, 'r', encoding='utf-8') as infile:
                data = json.load(infile)
            return data
        except Exception as Err:
            print(Err, 'carregando aquivo')
            return 0

    def read_wav_file(self, file):
        """Carrega os dados de um arquivo de audio e retorna como um array wave"""
        data , fs = sf.read(file)
        return data
           
    def use_ffmpeg_to_convert(self, input_file, args, output_file, inst_configs):
        """Utiliza ffmpeg para executar a conversão de arquivos"""
        log = check_output(f'ffmpeg -y -hide_banner -loglevel error -i {input_file} {args} {output_file}')            # Chama o commando e aguarda o retorno bloqueando a execução
        if (log != b''):
            self.adiciona_linha_log(f'Retorno da chamada do ffmpeg: {log}', inst_configs['files_folder'])
        try:
            #os.remove(input_file)                                                   # Remove o arquivo wav
            pass    
        except Exception as err:
            self.adiciona_linha_log(f'use_ffmpeg_to_convert, remove file error: {err}', inst_configs['files_folder'])
            
    """ def verificar_arquivos_de_terceiros(self):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))                   # This is your Project Root
        print("Carregando arquivos de terceiros...")
        try:
            SOX_DIR = os.path.join(ROOT_DIR, 'sox-14-4-1')                      # Verificação dos arquivos de programa de terceiros utilizados pelo código
            os.add_dll_directory(r'{}'.format(SOX_DIR))
        except Exception as Err:                                                # Inicia uma exceção fatal caso os arquivos não sejam encontrados
            self.adiciona_linha_log(f'Verifica_arquivos_de_terceiros - {Err}')
            exit()
    """



if __name__ == '__main__':
    FileOperations_ = FileOperations()
  

