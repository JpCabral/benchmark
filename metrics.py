import os
import subprocess
from scapy.all import rdpcap
import numpy as np
import time

def packetloss_calc(arquivo, usuario):
    packets = rdpcap(arquivo)
    totalpackets = len(packets)
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
        time.sleep(15)
    return loss


def throughput_calc(janeladetempo,arquivo):
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