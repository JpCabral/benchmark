import os
import subprocess

def generate_packets(arquivo_amostra, interface, loops):
    arquivo_amostra = subprocess.getoutput('pwd') + '/pcap_samples/' + arquivo_amostra
    os.system("tcpreplay -i "+interface+" -K --loop="+loops+" -x 0.67 "+arquivo_amostra+" &")
