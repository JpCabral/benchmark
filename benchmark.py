import subprocess
import os
from scapy.all import rdpcap
import matplotlib.pyplot as plt
import numpy as np
import time
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
janeladetempo = 1  # 5 * 60  # Segundos de captura do .pcapng
interface = 'enp0s31f6'
usuario = 'jpcabral'
tempo = 60
intervalo = 5
vez = 0
qtdhoras = 3
destino = subprocess.getoutput('pwd') + '/'
benchmark_executado = False


def captura_pcap(arquivo, interface, janeladetempo):
    pwd = (subprocess.getoutput('pwd')) + '/'
    fullarquivo = pwd + arquivo
    os.system("touch " + arquivo)
    os.system("dumpcap -i " + interface + " -a duration:" + str(janeladetempo) + " -w " + fullarquivo)


def packetloss_calc(arquivo, usuario):
    packets = rdpcap(arquivo)
    totalpackets = len(packets)
    import subprocess
    retransmitidos = 0
    pwd = (subprocess.getoutput('pwd')) + '/'
    arquivo = pwd + arquivo

    retransmitidos_lista = subprocess.getoutput(
        "runuser -l " + usuario + " -c 'tshark -r " + arquivo + " -T fields -e tcp.analysis.retransmission'")
    try:
        for caso in retransmitidos_lista:
            if '1' in caso:
                retransmitidos += 1
        if retransmitidos == 0:
            return 0
        loss = retransmitidos / totalpackets * 100
    except IndexError:
        print('Sem pacotes para analisar... \naguardando 15 segundos...')
        sleep(15)
    return loss


def throughput_calc(janeladetempo):
    totalbytes = 0
    packets = rdpcap(arquivo)
    for packet in packets:
        totalbytes += int(len(packet))
    totalbits = totalbytes / 8
    throughput = (totalbits / janeladetempo)
    resultado = throughput
    return resultado  # bits per second (bps)]


def delay_calc(arquivo, usuario):
    delays = 0.0
    pwd = (subprocess.getoutput('pwd')) + '/'
    arquivo = pwd + arquivo

    lista_de_delays = subprocess.getoutput(
        "runuser -l " + usuario + " -c 'tshark -r " + arquivo + " -T fields -e frame.time_delta_displayed'")
    lista_de_delays = lista_de_delays.splitlines()

    for delay in lista_de_delays:
        try:
            if isinstance(float(delay), float):
                delays += float(delay)
        except ValueError:
            continue
    try:
        return delays / len(lista_de_delays) * 1000  # Delay médio em milissegundos
    except ZeroDivisionError:
        # 0 Pacotes foram capturados, portanto retorna-se 0.0
        return 0.0


def grafico_througput(throughputlist, destino, time, arranjohoras):
    # Data for plotting
    # x = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    # x = np.arange(start=1, stop=10 + 1, step=1)
    x = arranjohoras
    y = throughputlist

    fig, ax = plt.subplots()
    ax.plot(x, y)

    # ax.set(xlabel='time (min)', ylabel='throughput (bps)', title='Average Throughput')
    ax.set(xlabel='time (hours)', ylabel='throughput (bps)', title='Average Throughput')
    ax.grid()

    fig.savefig(destino + "[" + str(time) + "]" + " - Throughput.png")


def grafico_packetloss(packetlosslist, destino, time, arranjohoras):
    # Data for plotting
    # x = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    x = arranjohoras
    y = packetlosslist

    fig, ax = plt.subplots()
    ax.plot(x, y)

    # ax.set(xlabel='time (min)', ylabel='loss(%)', title='Average Packet Loss')
    ax.set(xlabel='time (hours)', ylabel='loss(%)', title='Average Packet Loss')
    ax.grid()

    fig.savefig(destino + "[" + str(time) + "]" + " - Packet_loss.png")


def grafico_delay(delaylist, destino, time, arranjohoras):
    # Data for plotting
    # x = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    x = arranjohoras
    y = delaylist

    fig, ax = plt.subplots()
    ax.plot(x, y)

    # ax.set(xlabel='time (min)', ylabel='delay(ms)', title='Average Delay')
    ax.set(xlabel='time (hours)', ylabel='delay(ms)', title='Average Delay')

    ax.grid()

    fig.savefig(destino + "[" + str(time) + "]" + " - Delay.png")


def grafico_packet_vs_time(packetlist, destino, time, arranjohoras):
    # Data for plotting
    x = arranjohoras
    # x = np.arange(start=1, stop=10 + 1, step=1)
    y = packetlist

    fig, ax = plt.subplots()
    ax.plot(x, y)

    # ax.set(xlabel='time (min)', ylabel='delay(ms)', title='Average Delay')
    # ax.set(xlabel='time (hours)', ylabel='delay(ms)', title='Average Delay')
    ax.set(xlabel='time (min)', ylabel='packets', title='Average Packets')

    ax.grid()

    fig.savefig(destino + "[" + str(time) + "]" + " - Packet_vs_Time.png")


def grafico_margem_throughput(qtdhoras, throughput_central_list, throughput_maior_list, throughput_menor_list):
    # Data for plotting
    x = np.arange(start=1, stop=qtdhoras + 1, step=1)
    y = throughput_central_list

    plt.errorbar(x, y, xerr=throughput_menor_list, yerr=throughput_maior_list, fmt='--o')

    # # First illustrate basic pyplot interface, using defaults where possible.
    # plt.figure()
    # plt.errorbar(x, y, xerr=0.2, yerr=0.4)
    # plt.title("Simplest errorbars, 0.2 in x, 0.4 in y")
    #
    # # Now switch to a more OO interface to exercise more features.
    # fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True)
    # ax = axs[0, 0]
    # ax.errorbar(x, y, yerr=yerr, fmt='o')
    # ax.set_title('Vert. symmetric')
    #
    # # With 4 subplots, reduce the number of axis ticks to avoid crowding.
    # ax.locator_params(nbins=4)
    #
    # ax = axs[0, 1]
    # ax.errorbar(x, y, xerr=xerr, fmt='o')
    # ax.set_title('Hor. symmetric')
    #
    # ax = axs[1, 0]
    # # ax.errorbar(x, y, yerr=[yerr, 2 * yerr], xerr=[xerr, 2 * xerr], fmt='--o')
    # ax.errorbar(x, y, yerr=yerr, xerr=xerr, fmt='--o')
    # ax.set_title('H, V asymmetric')
    #
    # ax = axs[1, 1]
    # ax.set_yscale('log')
    # # ax.any()
    # # Here we have to be careful to keep all y values positive:
    # # ylower = np.maximum(1e-2, y - yerr)
    # # yerr_lower = y - ylower
    # #
    # # ax.errorbar(x, y, yerr=[yerr_lower, 2 * yerr], xerr=xerr,
    # #             fmt='o', ecolor='g', capthick=2)
    # ax.set_title('Mixed sym., log y')
    #
    # fig.suptitle('Variable errorbars')

    plt.savefig(subprocess.getoutput('pwd') + '/' + "margem_de_erro_throughput.png")
    # plt.errorbar(x,y,
    #              xerr=xerr,
    #              yerr=yerr,
    #              label='Average Throughput'
    #            fmt='-',
    #             color='g',


def margem_de_erro(qtdhoras):
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


def benchmark_default(vez, tempo, interface, janeladetempo, arquivo, usuario):
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


def benchmark_media_horas(arranjotempocoleta, interface, janeladetempo, arquivo, usuario, qtdhoras, arranjohoras):
    for i in range(1, qtdhoras + 1):
        print("###################################### Etapa: " + str(i) + " ######################################")
        for etapa in arranjotempocoleta:
            print("\nIteração ", etapa, "/", arranjotempocoleta[len(arranjotempocoleta) - 1])
            captura_pcap(arquivo, interface, janeladetempo)

            camada1_delay_list.append(delay_calc(arquivo, usuario))
            camada1_packetloss_list.append(packetloss_calc(arquivo, usuario))
            camada1_throughput_list.append(throughput_calc(janeladetempo))
            packetlist.append(len(rdpcap(arquivo)))

        total = 0

        for delay in camada1_delay_list:
            total += delay
        total = total / len(arranjotempocoleta)
        delay_horas.append(total)
        print("Tamanho camada1_delay_list:", len(camada1_delay_list))
        print("Tamanho delay_horas:", len(delay_horas))
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

    grafico_delay(delay_horas, destino, time.strftime("%H:%M", time.localtime()), arranjohoras)
    grafico_packetloss(packetloss_horas, destino, time.strftime("%H:%M", time.localtime()), arranjohoras)
    grafico_througput(throughput_horas, destino, time.strftime("%H:%M", time.localtime()), arranjohoras)
    grafico_packet_vs_time(packetlistfinal, destino, time.strftime("%H:%M", time.localtime()), arranjohoras)
    benchmark_executado = True


def ler_sensor_ultrassonico(horasleitura):
    import time
    import paho.mqtt.client as mqtt
    import sys
    import argparse
    import RPi.GPIO as GPIO  # Import GPIO library
    import time  # Import time library
    import serial

    timeout = horasleitura * 60 * 60  # Horas em segundos
    timeout_start = time.time()
    tempo = 0

    MQTT_PORT = 1883
    TOPICO = '/softway/iot'
    MQTT_TIMEOUT = 60

    GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering

    TRIG = 23  # Associate pin 23 to TRIG
    ECHO = 24  # Associate pin 24 to ECHO

    ID_LINE = 1
    MQTT_ADDRESS = '10.17.0.2'

    GPIO.setup(TRIG, GPIO.OUT)  # Set pin as GPIO out
    GPIO.setup(ECHO, GPIO.IN)  # Set pin as GPIO in

    def send_message(msg, MQTT_ADDRESS):  # Send MQTT Message
        client = mqtt.Client()
        client.connect(MQTT_ADDRESS, MQTT_PORT, MQTT_TIMEOUT)
        result, mid = client.publish(TOPICO, msg)
        print('Mensagem enviada ao canal: %d, [MQTT_ADDRESS: %s]' % (mid, MQTT_ADDRESS))

    while time.time() < timeout_start + timeout:

        GPIO.output(TRIG, False)  # Set TRIG as LOW
        time.sleep(2)  # Delay of 2 seconds

        GPIO.output(TRIG, True)  # Set TRIG as HIGH
        time.sleep(0.00001)  # Delay of 0.00001 seconds
        GPIO.output(TRIG, False)  # Set TRIG as LOW

        while GPIO.input(ECHO) == 0:  # Check whether the ECHO is LOW
            pulse_start = time.time()  # Saves the last known time of LOW pulse

        while GPIO.input(ECHO) == 1:  # Check whether the ECHO is HIGH
            pulse_end = time.time()  # Saves the last known time of HIGH pulse

        pulse_duration = pulse_end - pulse_start  # Get pulse duration to a variable

        distance = pulse_duration * 17150  # Multiply pulse duration by 17150 to get distance
        distance = round(distance, 2)  # Round to two decimal points

        if distance > 5:
            mensagem = "{\"id\":" + str(ID_LINE) + "}"
            print("++ MSG-SEND:", mensagem, "\n")

            send_message(mensagem, MQTT_ADDRESS)  # Send message via MQTT protocol



arranjotempocoleta = np.arange(start=0, stop=60 + 1, step=5)
arranjohoras = np.arange(start=1, stop=qtdhoras + 1, step=1)

try:
    benchmark_media_horas(arranjotempocoleta, interface, janeladetempo, arquivo, usuario, qtdhoras, arranjohoras)
    # benchmark_default(vez, tempo, interface, janeladetempo, arquivo, usuario)

except KeyboardInterrupt:
    print("Execução abortada pelo usuário")