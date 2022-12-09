from subprocess import check_output
import numpy as np

class Analyzer():
    def __init__(self) -> None:
        pass
      
    def verificar_clipped(self, data):
        """Retorna True se for detectado audio clipado"""
        try:
            max = 0
            contagem = 0
            for sample in data:
                for channel in sample:
                    valor = abs(channel)
                    if valor > max:
                        max = valor
                    if valor == 32768:
                        contagem += 1
            if contagem > 0:
                return True
            else:
                return False
        except Exception as err:
            print (err)

    def verifica_silencio(self, data, silence_offset):
        audio_results = [False, False, False]
        for idx, value in enumerate(self.get_data_RMS(data)):
            if value <= silence_offset:
                audio_results[idx] = True
        return audio_results

    def get_data_RMS(self, data):
        ("""Retorna o valor rms dos dados informados como uma lista. """
        """ Os indices da lista referem se aos canais individualmente.""")
        calculated_rms = []
        for channel in range(len(data[0])):    # roda 2x em audios stereo
            channel_data = []                
            for sample in data:
                channel_data.append(sample[channel])
            calculated_rms.append(np.sqrt(np.mean(np.array(channel_data)**2)))  
        return calculated_rms 

    
if __name__ == '__main__':
    Analyzer_ = Analyzer()
    fp1 = Analyzer_.calc_fp('pinknoise.wav')
    fp2 = Analyzer_.calc_fp('whitenoise.wav')
    print(Analyzer_.compair_fp(fp1, fp2))
