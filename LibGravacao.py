from subprocess import run, PIPE, CREATE_NO_WINDOW, STDOUT
from LibFileOperations import FileOperations                                 # Suporte à operações com arquivos
 
class Gravacao():                                                               # Criação da classe que dá suporte a operações de gravação de áudio
    def __init__(self) -> None:
        self.FileOperations_ = FileOperations()                                 # Suporte à operações com arquivos

    def gravar_trecho_de_streaming(self, m3u8link, filename):
        """Salva um arquivo na pasta dos arquivos salvos configurada para a instancia. Retorna o nome do arquivo salvo"""
        output = run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-t', '10', '-y', '-i', m3u8link, filename], creationflags=CREATE_NO_WINDOW, timeout=10, stdout=PIPE, stderr=STDOUT, text=True)
        return output.returncode

if __name__ == '__main__':
    Gravacao_ = Gravacao()
    recording = Gravacao_.gravar_trecho_de_streaming("https://47809y.ha.azioncdn.net/primary/ita_fln.sdp/playlist.m3u8", 'teste.mp3')
  