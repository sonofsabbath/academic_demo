import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import pandas as pd
from tkinter import messagebox, filedialog, ttk


def find_longest_job(js, times):
    """"Finds a job with longest execution time and deletes it from jobs and times lists.
    Returns longest job's index and updated lists."""
    ind = np.argmax(times)
    longest_job = js[ind]
    js = np.delete(js, ind)
    times = np.delete(times, ind)

    return longest_job, js, times


def find_possible_schedules(sch):
    """Finds all possible schedules, considering respective positions of already processed jobs"""
    possible = []
    n_tasks = len(sch)

    if n_tasks == 2:
        possible = [[sch[0], sch[1]], [sch[1], sch[0]]]
    else:
        moving = sch[-1]
        sch.remove(moving)

        for n in range(n_tasks):
            new_schedule = sch.copy()
            new_schedule.insert(n, moving)
            possible.append(new_schedule)

    return possible


def calculate_completion_times(sch, operations):
    """Calculates completion times for each operation with given schedule"""
    machs = operations.shape[0]
    machine_ready = np.zeros(machs)
    n_tasks = len(sch)
    operation_done = np.zeros((machs, n_tasks))

    for m in range(machs):
        for task in range(n_tasks):
            if operation_done[m-1, task] <= machine_ready[m] or m == 0:
                machine_ready[m] += operations[m, sch[task]]
            else:
                machine_ready[m] = operation_done[m - 1, task] + operations[m, sch[task]]
            operation_done[m, task] = machine_ready[m]

    return operation_done


def find_neighbor(sch, prev):
    """Finds new possible schedule in the neighborhood of the previous one"""
    found = 0
    failed = 1
    n = len(sch)
    neighbor = sch.copy()

    while not found:
        while failed:
            swap = np.random.randint(n, size=2)
            if swap[0] != swap[1]:
                failed = 0

        neighbor[swap[0]], neighbor[swap[1]] = neighbor[swap[1]], neighbor[swap[0]]
        if prev == []:
            found = 1
        elif neighbor not in prev:
            found = 1
        else:
            failed = 1

    return neighbor


def accept_worse_schedule(current, previous, t):
    """Decides whether to accept worse solution based on acceptance probability"""
    diff = current - previous
    p = np.random.uniform()
    ap = np.e ** (-diff / t)

    if p <= ap:
        return True
    else:
        return False
    

def sa(t_max, t_min, cr, iters, tasks):
    """Simulated annealing algorithm - searches for minimal makespan"""
    global progBar
    prog = 0
    n_machines, n_jobs = tasks.shape
    temp = t_max

    best_makespan = np.sum(tasks) * 1000
    best_schedule = None
    schedule = list(np.arange(n_jobs))
    makespan = calculate_completion_times(schedule, tasks)[-1, -1]

    while temp >= t_min:
        previous_schedules = []

        for ipt in range(iters):
            new_schedule = find_neighbor(schedule, previous_schedules)
            previous_schedules.append(new_schedule)
            new_makespan = calculate_completion_times(new_schedule, tasks)[-1, -1]

            if new_makespan < makespan or accept_worse_schedule(new_makespan, makespan, temp):
                schedule = new_schedule
                makespan = new_makespan

        if makespan < best_makespan:
            best_schedule = schedule
            best_makespan = makespan

        prog += 1
        progBar['value'] = (prog / 224) * 100
        root.update_idletasks()
        temp = temp * cr

    return best_schedule, best_makespan


def neh(tasks):
    global progBar
    """NEH algorithm for finding minimal makespan"""
    schedule = []
    n_jobs = tasks.shape[1]
    jobs = np.arange(n_jobs)
    job_times = tasks.sum(axis=0)

    for job in range(n_jobs):
        job_for_schedule, jobs, job_times = find_longest_job(jobs, job_times)
        schedule.append(job_for_schedule)

        if job >= 1:
            possible_schedules = find_possible_schedules(schedule)

            makespans = []
            for s in possible_schedules:
                completion_times = calculate_completion_times(s, tasks)
                makespans.append(completion_times[-1, -1])

            schedule = possible_schedules[int(np.argmin(makespans))]
            progBar['value'] = ((job + 1) / n_jobs) * 100
            root.update_idletasks()

    return schedule, np.min(makespans)


def ops_start_times(sch, ops, ops_done):
    ops_start = np.zeros(ops.shape)
    sch_job = 0

    for j in sch:
        for m in range(ops.shape[0]):
            ops_start[m, j] = ops_done[m, sch_job] - ops[m, j]
        sch_job += 1

    return ops_start


def select_file():
    global fileLbl
    global file_path
    root.filename = filedialog.askopenfilename(initialdir='/', title='Select .csv file',
                                               filetypes=(('csv files', '*.csv'),))

    fileLbl.grid_forget()
    fileLbl = tk.Label(frame1, text=root.filename)
    fileLbl.grid(row=0, column=0, columnspan=3)
    file_path = root.filename


def gantt_chart(ops_done, ops_start, ops):
    fig_width = max((ops_done[-1, -1] / 100) * 15, 5)
    fig_height = ops_done.shape[0]
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.set_title('Gantt chart')
    ax.set_xlabel('Time')
    ax.set_ylabel('Machines')

    ax.set_ylim(0, (ops_done.shape[0] + 1) * 10)
    yticks = [(x + 1) * 10 for x in range(ops_done.shape[0])]
    ax.set_yticks(yticks)
    ax.set_yticklabels([x for x in range(ops_done.shape[0])])
    
    for i in range(ops_done.shape[0]):
        for j in range(ops_done.shape[1]):
            ax.broken_barh([(ops_start[i, j], ops[i, j])], (yticks[i] - 3, 6), edgecolor='black')
            xtext = ops_start[i, j] + ops[i, j] / 2.25
            ytext = yticks[i] - 0.75
            plt.text(xtext, ytext, j + 1)

    plt.savefig('gantt.png', bbox_inches='tight')


def start_scheduling():
    global progBar

    if file_path is None:
        messagebox.showerror('File error', 'Please select a file')
        return

    frame1.destroy()
    frame2.destroy()
    acceptBtn.destroy()

    data = np.array(pd.read_csv(file_path, header=None, delimiter=';'))
    alg_choice = alg.get()

    if not alg_choice:
        setLbl = tk.Label(root, text='Scheduling in progress... (NEH)', padx=100)
        progBar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
        setLbl.pack()
        progBar.pack()
        root.update_idletasks()
        decision, result = neh(data)
    else:
        setLbl = tk.Label(root, text='Scheduling in progress... (Simulated annealing)', padx=100)
        progBar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
        setLbl.pack()
        progBar.pack()
        root.update_idletasks()
        decision, result = sa(90, 0.01, 0.96, 500, data)

    show_decision = []
    for i in decision:
        show_decision.append(i + 1)
    save_schedule = open('schedule.txt', 'w')
    save_schedule.write(str(show_decision))
    save_schedule.close()

    times = calculate_completion_times(decision, data)
    start_times = ops_start_times(decision, data, times)
    start_save = pd.DataFrame(start_times)
    h = []
    for i in range(len(decision)):
        h.append('Job ' + str(i + 1))
    start_save.index += 1
    start_save.to_excel('times.xlsx', index=True, index_label='Machines', header=h)

    gantt_chart(times, start_times, data)

    messagebox.showinfo('Finished', 'Scheduling finished!\nMakespan: ' + str(result) + '\nSchedule, time matrix'
                                                                                       ' and Gantt chart are saved in'
                                                                                       ' the app folder')
    root.destroy()


file_path = None
root = tk.Tk()
root.title('Scheduling app')

frame1 = tk.LabelFrame(root, padx=100)
frame1.pack()
fileLbl = tk.Label(frame1, text='File not selected')
fileBtn = tk.Button(frame1, text='Select file', command=select_file)

fileLbl.grid(row=0, column=0, columnspan=3)
fileBtn.grid(row=1, column=1, pady=5)

frame2 = tk.LabelFrame(root, padx=100)
frame2.pack()
alg = tk.IntVar()
alg.set(0)
algorithmLbl = tk.Label(frame2, text='Select the algorithm')
nehBtn = tk.Radiobutton(frame2, text='NEH', variable=alg, value=0)
saBtn = tk.Radiobutton(frame2, text='Simulated annealing', variable=alg, value=1)

algorithmLbl.grid(row=2, column=0, columnspan=3)
nehBtn.grid(row=3, column=1)
saBtn.grid(row=4, column=1)

acceptBtn = tk.Button(root, text='Schedule', command=start_scheduling)
acceptBtn.pack()

root.mainloop()
