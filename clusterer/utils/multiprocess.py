import multiprocessing


def _SpawnProcess(func,args,num_processes):
    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(target=func, args=args)
        p.start()
        processes.append(p)

    return processes


def SpawnProcesses(funcs,args,num_processes,join=True):
    if type(funcs) is list:
        assert type(args) is list,'Expected args to be list'
        assert type(num_processes) is list,'Expected num_processes to be list'
        processes = []
        for func,arg,num_process in zip(funcs,args,num_processes):
            process = _SpawnProcess(func,arg,num_process)
            processes += process

    else:
        #print(args)
        processes = _SpawnProcess(funcs,args,num_processes)

    if not join:
        return processes

    for process in processes:
        process.join()