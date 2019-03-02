#!/usr/bin/python

import pcapy
import os
import sys, traceback

from collections import Counter
from impacket import ImpactDecoder, ImpactPacket
from paylmodel import PaylModel

model_file = "payl.model"

def main(argv):
    try:
        if argv[1] == 'training':
            payl_train(argv[2])
        else:
            payl_detect(argv[2])
    except IndexError as e:
        traceback.print_exc(file=sys.stdout)
        print "Usage : python payl.py <training|testing> [filename]"

def payl_train(infile):
    cap = pcapy.open_offline(infile)
    models = {}

    while(1):
        (header, packet) = cap.next()
        if not header:
            break
        parse(models, header, packet)

    for key, value in models.items():
        value.save()


# def payl_detect(mode):
#     # load models



def parse(models, header, packet):
    length_groups = [500, 1500]
    decoder = ImpactDecoder.EthDecoder()
    ether = decoder.decode(packet)

    #print str(ether.get_ether_type()) + " " + str(ImpactPacket.IP.ethertype)

    if ether.get_ether_type() == ImpactPacket.IP.ethertype:
        iphdr = ether.child()
        transporthdr = iphdr.child()
        if transporthdr.get_data_as_string() != '' and isinstance(transporthdr, ImpactPacket.TCP):
            s_addr = iphdr.get_ip_src()
            d_addr = iphdr.get_ip_dst()
            s_port = transporthdr.get_th_sport()
            d_port = transporthdr.get_th_dport()
            d_length = transporthdr.get_size()
            payload = transporthdr.get_data_as_string()

            grams = get_byte_freq(payload, d_length)
            group_length = length_groups[len(length_groups)-1]
            for i in range(0, len(length_groups) - 1):
                if d_length <= length_groups[i]:
                    group_length = length_groups[i]

            group = str(d_port) + "-" + str(group_length)
            if group in models:
                models[group].add_grams(grams)
            else:
                models[group] = PaylModel(d_port, group_length)
                models[group].add_grams(grams)





def get_byte_freq(payload, length):
    c = Counter()
    arr_payload = []
    grams = dict.fromkeys(range(0, 256), 0)

    for ch in list(payload):
        arr_payload.append(ord(ch))

    c.update(arr_payload)
    for gram, value in c.items():
        #print str(gram) + "(" + str(value) + ")"
        value = value/float(length)
        grams[gram] = value

    return grams


if __name__ == '__main__':
	main(sys.argv)
