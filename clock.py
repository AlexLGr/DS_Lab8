from multiprocessing import Process, Pipe, Manager
from time import sleep


# send time vector to the pipe
def send_vector(pipe, pid, counter):
    counter[pid] += 1
    pipe.send(counter)


# receive time vector and update
def receive_vector(pipe, pid, counter):
    time = pipe.recv()
    for pid in range(len(counter)):
        counter[pid] = max(time[pid], counter[pid])


# some local event
def event_simulator(pid, counter):
    counter[pid] += 1


# process a
def process_a(pipe):
    pid = 0
    counter = [0, 0, 0]

    send_vector(pipe, pid, counter)
    send_vector(pipe, pid, counter)
    event_simulator(pid, counter)
    sleep(1)
    receive_vector(pipe, pid, counter)
    event_simulator(pid, counter)
    event_simulator(pid, counter)
    receive_vector(pipe, pid, counter)

    results[pid] = counter


# process b
def process_b(pipe_a, pipe_c):
    pid = 1
    counter = [0, 0, 0]

    sleep(1)
    receive_vector(pipe_a, pid, counter)
    receive_vector(pipe_a, pid, counter)
    send_vector(pipe_a, pid, counter)
    receive_vector(pipe_c, pid, counter)
    event_simulator(pid, counter)
    send_vector(pipe_a, pid, counter)
    send_vector(pipe_c, pid, counter)
    send_vector(pipe_c, pid, counter)

    results[pid] = counter


# process c
def process_c(pipe):
    pid = 2
    counter = [0, 0, 0]

    send_vector(pipe, pid, counter)
    sleep(7)
    receive_vector(pipe, pid, counter)
    event_simulator(pid, counter)
    receive_vector(pipe, pid, counter)

    results[pid] = counter


if __name__ == '__main__':
    pipe_ab, pipe_ba = Pipe()
    pipe_bc, pipe_cb = Pipe()

    manager = Manager()
    results = manager.list([[], [], []])

    A = Process(target=process_a, args=(pipe_ab,))
    B = Process(target=process_b, args=(pipe_ba, pipe_bc))
    C = Process(target=process_c, args=(pipe_cb,))

    A.start()
    B.start()
    C.start()

    A.join()
    B.join()
    C.join()

    print(f'Process a {results[0]}')
    print(f'Process b {results[1]}')
    print(f'Process c {results[2]}')
