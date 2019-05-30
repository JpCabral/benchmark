import graphics
from metrics import *
from sniffer import *
from threading import Thread
from time import strftime, localtime
def margem_de_erro(qtdhoras, tempo, intervalo, arquivo, interface, janeladetempo, camada1_delay_list,
                   camada1_packetloss_list, camada1_throughput_list, usuario, camada1_delays,
                   camada1_packetloss, camada1_throughputs):
    vez = 0
    for i in range(1, qtdhoras + 1):
        while vez != tempo + intervalo:
            print("\nColeta ", i, "/", qtdhoras, "- Iteração ", vez, "/", tempo, )
            captura_pcap(arquivo, interface, janeladetempo)

            # Limpa as listas para não haver repetições
            camada1_delay_list.clear()
            camada1_packetloss_list.clear()
            camada1_throughput_list.clear()

            # Dados coletados e automaticamente inseridos nas 13 posições da camada1_metrica_list
            camada1_delay_list.append(delay_calc(arquivo, usuario))
            camada1_packetloss_list.append(packetloss_calc(arquivo, usuario))
            camada1_throughput_list.append(throughput_calc(janeladetempo))

            # print ("camada1_delay_list: ",camada1_delay_list)

            # Vez iterada
            vez += intervalo
        print("camada1_throughput_list: ", camada1_throughput_list)
        camada1_delays.append(camada1_delay_list)
        camada1_packetloss.append(camada1_packetloss_list)
        camada1_throughputs.append(camada1_throughput_list)

        vez = 0  # Retorna vez para 0 para não parar o while

    throughput_central = 0.0
    throughput_maior = 0.0
    throughput_menor = 0.0
    camada2_throughputs_centrais = []
    camada2_throughputs_maiores = []
    camada2_throughputs_menores = []

    print("camada1_throughputs tem tamanho: ", len(camada1_throughputs), "\n\ncamada1_throughputs tem tipo:",
          type(camada1_throughputs))

    for medias_hora in camada1_throughputs:
        print("Tipo de medias_hora:", type(medias_hora), "\n medias_hora tem tipo:", type(medias_hora))

        for media in medias_hora:
            throughput_central += media

        throughput_central = throughput_central / len(medias_hora)
        camada2_throughputs_centrais.append(throughput_central)
        throughput_central = 0

        throughput_maior = max(medias_hora)
        camada2_throughputs_maiores.append(throughput_maior)
        throughput_menor = min(medias_hora)
        camada2_throughputs_menores.append(throughput_menor)

    print("Throughput médio das 10 execuções: ", throughput_central)
    print("Menor Throughput analisado: ", throughput_menor)
    print("Maior Throughput analisado: ", throughput_maior)
    print("Margem de erro para +: ", throughput_central - throughput_maior)
    print("Margem de erro para -: ", throughput_central - throughput_menor)
    print("##########################################\nTamanho da camada2_throughputs_maiores:",
          len(camada2_throughputs_maiores), "\ncamada2_throughputs_maiores: ", camada2_throughputs_maiores,
          "\nTamanho da camada2_throughputs_menores: ", len(camada2_throughputs_menores),
          "\n camada2_throughputs_menores: ", camada2_throughputs_menores,
          "\nTamanho da camada2_throughputs_centrais: ", len(camada2_throughputs_centrais),
          "\ncamada2_throughputs_centrais: ", camada2_throughputs_centrais)
    # grafico_margem_throughput(qtdhoras=10, throughput_central_list=camada2_throughputs_centrais, throughput_maior_list=camada2_throughputs_maiores, throughput_menor_list=camada2_throughputs_menores)


def benchmark_default(vez, tempo, intervalo, arquivo, interface, janeladetempo, camada1_delay_list,
                      camada1_packetloss_list, camada1_throughput_list, usuario, delay_horas,throughput_horas,
                      packetloss_horas):
    threadSensor = Thread(target=ler_sensor_ultrassonico(), args=())
    threadSensor.start()
    while vez != tempo + intervalo:
        print("\nIteração ", vez, "/", tempo, )
        captura_pcap(arquivo, interface, janeladetempo)
        # print ('Throughput: '+str(throughput_calc(janeladetempo))+'bps')
        # print ('Packet Loss: %.2f'%packetloss_calc(arquivo, usuario)+'%')
        # print ('Delay médio: ' + str(delay_calc(arquivo, usuario)) + 'ms')
        camada1_delay_list.append(delay_calc(arquivo, usuario))
        camada1_packetloss_list.append(packetloss_calc(arquivo, usuario))
        camada1_throughput_list.append(throughput_calc(janeladetempo))
        vez += intervalo

    # grafico_delay(camada1_delay_list, destino)
    # grafico_packetloss(camada1_packetloss_list, destino)
    # grafico_througput(camada1_throughput_list, destino)
    total = 0

    for delay in camada1_delay_list:
        total += delay
    total = total / 10
    delay_horas.append(total)
    total = 0

    for throughput in camada1_throughput_list:
        total += throughput
    total = total / 10
    throughput_horas.append(total)
    total = 0

    for packetloss in camada1_packetloss_list:
        total += packetloss
    total = total / 10
    packetloss_horas.append(total)

    # print ('packetloss_10horas: ',packetloss_10horas)
    # print ('throughput_10horas: ',throughput_10horas)
    # print ('delay_10horas: ',delay_10horas)

    camada1_throughput_list.clear()
    camada1_delay_list.clear()
    camada1_packetloss_list.clear()

def benchmark_media_horas(qtdhoras, arquivo, interface, janeladetempo, camada1_delay_list,
                   camada1_packetloss_list, camada1_throughput_list, usuario, arranjotempocoleta,
                   packetlist, delay_horas, throughput_horas, packetloss_horas, packetlistfinal, arranjohoras,destino):

                                for i in range(1, qtdhoras + 1):
                                    print("###################################### Etapa: " + str(i) + " ######################################")
                                    for etapa in arranjotempocoleta:
                                        print("\nIteração ", etapa, "/", arranjotempocoleta[len(arranjotempocoleta) - 1])
                                        captura_pcap(arquivo, interface, janeladetempo)

                                        camada1_delay_list.append(delay_calc(arquivo, usuario))
                                        camada1_packetloss_list.append(packetloss_calc(arquivo, usuario))
                                        camada1_throughput_list.append(throughput_calc(janeladetempo, arquivo))
                                        packetlist.append(len(rdpcap(arquivo)))

                                    total = 0

                                    for delay in camada1_delay_list:
                                        total += delay
                                    total = total / len(arranjotempocoleta)
                                    delay_horas.append(total)
                                    total = 0

                                    for throughput in camada1_throughput_list:
                                        total += throughput
                                    total = total / len(arranjotempocoleta)
                                    throughput_horas.append(total)
                                    total = 0

                                    for packetloss in camada1_packetloss_list:
                                        total += packetloss
                                    total = total / len(arranjotempocoleta)
                                    packetloss_horas.append(total)
                                    total = 0

                                    for packets in packetlist:
                                        total += packets / len(arranjotempocoleta)
                                    packetlistfinal.append(total)

                                    camada1_throughput_list.clear()
                                    camada1_delay_list.clear()
                                    camada1_packetloss_list.clear()
                                    packetlist.clear()

                                print("\n Gerando gráficos ...")
                                grafico_delay(delay_horas, destino, strftime("%H:%M", localtime()), arranjohoras)
                                grafico_packetloss(packetloss_horas, destino, strftime("%H:%M", localtime()), arranjohoras)
                                grafico_througput(throughput_horas, destino, strftime("%H:%M", localtime()), arranjohoras)
                                grafico_packet_vs_time(packetlistfinal, destino, strftime("%H:%M", localtime()), arranjohoras)
