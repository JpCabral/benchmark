import subprocess
import os

def captura_pcap(arquivo, interface, janeladetempo):
    pwd = (subprocess.getoutput('pwd')) + '/'
    fullarquivo = pwd + arquivo
    os.system("touch " + arquivo)
    os.system("dumpcap -i " + interface + " -a duration:" + str(janeladetempo) + " -w " + fullarquivo)
