from os import system
from subprocess import getoutput

def generate_packets(arquivo_amostra, interface, loops):
    arquivo_amostra = getoutput('pwd') + '/pcap_samples/' + arquivo_amostra
    system("tcpreplay -i "+interface+" -K --loop="+loops+" -x 0.67 "+arquivo_amostra+" &")
