import subprocess
import os

def captura_pcap(arquivo, interface, janeladetempo):
    pwd = (subprocess.getoutput('pwd')) + '/'
    fullarquivo = pwd + arquivo

    try:
        os.system("dumpcap -i " + interface + " -a duration:" + str(janeladetempo) + " -w " + fullarquivo)
    except FileNotFoundError:
        os.system("touch " + arquivo)
