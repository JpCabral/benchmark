from  operation_modes import *
import numpy as np
from packet_generator import generate_packets
from threading import Thread
from time import sleep

camada1_delay_list = []
camada1_throughput_list = []
camada1_packetloss_list = []
camada1_throughputs = []
camada1_delays = []
camada1_packetloss = []
packetlist = []
packetlistfinal = []
throughput_horas = []
packetloss_horas = []
delay_horas = []
arquivo = '5min_fila_wifi.pcapng'
janeladetempo =  1  # 5 * 60  # Segundos de captura do .pcapng
interface = 'wlan0'
usuario = 'pi'
tempo = 60
intervalo = 5
vez = 0
qtdhoras = 3
destino = subprocess.getoutput('pwd') + '/graphics/'
benchmark_executado = False

arranjotempocoleta = np.arange(start=0, stop=60 + 1, step=5)
arranjohoras = np.arange(start=1, stop=qtdhoras + 1, step=1)

try:
    # captura_pcap(arquivo, interface, 10 * 60 )
    print("\nInicializando retransmissão dos pacotes...\n")
    sensor = Thread(
        target=generate_packets(arquivo_amostra="15min_fila_wifi.pcapng", interface="wlan0", loops="19")).start()
    sleep(1)
    print("\nInicializando análise...\n")
    analise = Thread(target=benchmark_media_horas(qtdhoras, arquivo, interface, janeladetempo, camada1_delay_list,
                                                  camada1_packetloss_list, camada1_throughput_list, usuario,
                                                  arranjotempocoleta,
                                                  packetlist, delay_horas, throughput_horas, packetloss_horas,
                                                  packetlistfinal, arranjohoras, destino))

    sensor.join()
    analise.join()

    # benchmark_default(vez, tempo, interface, janeladetempo, arquivo, usuario)

except KeyboardInterrupt:
    print("Execução abortada pelo usuário")
except Exception as e:
    print(e)
