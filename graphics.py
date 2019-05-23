import matplotlib.pyplot as plt
from numpy import arange
import subprocess
from os import system

def grafico_througput(throughputlist, destino, time, arranjohoras):
    x = arranjohoras
    y = throughputlist

    fig, ax = plt.subplots()
    ax.plot(x, y)

    # ax.set(xlabel='time (min)', ylabel='throughput (bps)', title='Average Throughput')
    ax.set(xlabel='time (hours)', ylabel='throughput (bps)', title='Average Throughput')
    ax.grid()
    try:
        fig.savefig(destino + "[" + str(time) + "]" + " - Throughput.png")
    except FileNotFoundError:
        system('mkdir '+destino)
        fig.savefig(destino + "[" + str(time) + "]" + " - Throughput.png")


def grafico_packetloss(packetlosslist, destino, time, arranjohoras):
    x = arranjohoras
    y = packetlosslist

    fig, ax = plt.subplots()
    ax.plot(x, y)

    ax.set(xlabel='time (hours)', ylabel='loss(%)', title='Average Packet Loss')
    ax.grid()
    try:
        fig.savefig(destino + "[" + str(time) + "]" + " - Packet_loss.png")
    except FileNotFoundError:
        system('mkdir '+destino)
        fig.savefig(destino + "[" + str(time) + "]" + " - Packet_loss.png")

def grafico_delay(delaylist, destino, time, arranjohoras):
    x = arranjohoras
    y = delaylist

    fig, ax = plt.subplots()
    ax.plot(x, y)

    ax.set(xlabel='time (hours)', ylabel='delay(ms)', title='Average Delay')

    ax.grid()
    try:
        fig.savefig(destino + "[" + str(time) + "]" + " - Delay.png")
    except FileNotFoundError:
        system('mkdir '+destino)
        fig.savefig(destino + "[" + str(time) + "]" + " - Delay.png")

def grafico_packet_vs_time(packetlist, destino, time, arranjohoras):
    x = arranjohoras
    y = packetlist

    fig, ax = plt.subplots()
    ax.plot(x, y)

    ax.set(xlabel='time (hours)', ylabel='packets', title='Average Packets')

    ax.grid()
    try:
        fig.savefig(destino + "[" + str(time) + "]" + " - Packet_vs_Time.png")
    except FileNotFoundError:
        system('mkdir '+destino)
        fig.savefig(destino + "[" + str(time) + "]" + " - Packet_vs_Time.png")

def grafico_margem_throughput(qtdhoras, throughput_central_list, throughput_maior_list, throughput_menor_list):

    x = arange(start=1, stop=qtdhoras + 1, step=1)
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


# 
# oot@raspberrypi:/home/pi/benchmark# iperf3 -c 10.16.0.237 -F 5min_fila_wifi.pcapng
# Connecting to host 10.16.0.237, port 5201
# [  4] local 10.16.0.122 port 54386 connected to 10.16.0.237 port 5201
# [ ID] Interval           Transfer     Bandwidth       Retr  Cwnd
# [  4]   0.00-0.00   sec  29.7 KBytes   204 Mbits/sec    0   18.4 KBytes
# - - - - - - - - - - - - - - - - - - - - - - - - -
# [ ID] Interval           Transfer     Bandwidth       Retr
# [  4]   0.00-0.00   sec  29.7 KBytes   204 Mbits/sec    0             sender
#         Sent 29.7 KByte /  587 KByte (5%) of 5min_fila_wifi.pcapng
# [  4]   0.00-0.00   sec  21.2 KBytes   145 Mbits/sec                  receiver
