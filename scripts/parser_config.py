
def hfconfig_parser(config_file):

    batch_size = []
    back_end = []
    seq_len = []
    n_instance = []
    #config_file = open('../benchmarking_config/hf_config.txt')

    for line in config_file:
        x = list(line.split('='))
        if x[0] == "N_INSTS":
            x1 = x[1].split('(')
            n_instance = [int(t) for t in ((x[1].split('('))[1].split(')'))[0].split(' ')]
            #print("n_instance = ", n_instance)
        elif x[0] == "SEQ_LEN":
            l = list(x[1].split(','))
            seq_len = [int(sl) for sl in l]
            #print("sequence length = ", seq_len)
        elif x[0] == "BATCH_SIZE":
            l = list(x[1].split(','))
            batch_size = [int(bs) for bs in l]
            #print("batch_size = ", batch_size)
        elif x[0] == "BACKEND":
                back_end = list((x[1].split('"'))[1].split(','))
                #print("backend = ", back_end)
    return back_end, batch_size, seq_len, n_instance
 