import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
from Algorithms import Algorithms


# AI was used to learn some of the syntax for using Tkinter on Pycharm because of my unfamiliarity
# ex: side= , padx, key=lambda


class Helper:
    quantum_time = None

class ProcessData:
    def __init__(self, pid, burst, priority, arrival):
        self.pid = pid
        self.burst = burst
        self.priority = priority
        self.arrival = arrival


class SchedulingResult:
    def __init__(self, pid, arrival, burst, start, finish):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.start = start
        self.finish = finish
        self.waiting = start - arrival
        self.turnaround = finish - arrival
        self.rtime = start - arrival


# main
class CpuScheduler(Algorithms):
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduler (Tkinter)")
        self.root.geometry("900x600")

        self.processes = []

        self.create_widgets()

    # user interface
    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="Process Count:").pack(side=tk.LEFT)
        self.entry_count = tk.Entry(top_frame, width=5)
        self.entry_count.pack(side=tk.LEFT, padx=5)

        tk.Button(top_frame, text="Set", command=self.set_processes).pack(side=tk.LEFT)
        tk.Button(top_frame, text="Random", command=self.randomize).pack(side=tk.LEFT)

        # table
        columns = ("PID", "Burst", "Priority", "Arrival")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack()

        tk.Button(btn_frame, text="FCFS", command=self.run_fcfs).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="SJF", command=self.run_sjf).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Priority", command=self.run_priority).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Round Robin", command=self.run_rr).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="MLQ", command=self.run_mlq).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="SRTF", command=self.run_srtf).pack(side=tk.LEFT, padx=5)

        # results
        self.result_box = tk.Text(self.root, height=10)
        self.result_box.pack(fill=tk.BOTH, padx=10, pady=10)

    # process
    def set_processes(self):
        try:
            count = int(self.entry_count.get())
        except:
            messagebox.showerror("Error", "Invalid number")
            return

        self.tree.delete(*self.tree.get_children())
        self.processes.clear()

        # this is where I need to edit if I want to allow them to input their own stuff
        # I had to alter this from starter code because the interface wouldn't allow the user to input their own values
        for i in range(count):
            burst = simpledialog.askfloat("Input", f"Burst time for P{i + 1}:", parent=root)
            priority = simpledialog.askfloat("Input", f"Priority time for P{i + 1}:", parent=root)
            arrival = simpledialog.askfloat("Input", f"Arrival time for P{i + 1}:", parent=root)

            p = ProcessData(f"P{i + 1}", burst, priority, arrival)
            self.processes.append(p)
            self.tree.insert("", tk.END, values=(p.pid, p.burst, p.priority, p.arrival))

    # randomize button
    def randomize(self):
        for i, p in enumerate(self.processes):
            p.burst = random.randint(1, 20)
            p.priority = random.randint(1, 10)
            p.arrival = random.randint(0, 10)

            self.tree.item(self.tree.get_children()[i],
                           values=(p.pid, p.burst, p.priority, p.arrival))

    # algorithms

    # first come first serve
    def run_fcfs(self):
        processes = sorted(self.processes, key=lambda x: x.arrival)
        current = 0
        results = []

        for p in processes:
            start = max(current, p.arrival)
            finish = start + p.burst
            results.append(SchedulingResult(p.pid, p.arrival, p.burst, start, finish))
            current = finish

        self.display(results, "FCFS")

    # shortest job first
    def run_sjf(self):
        remaining = self.processes[:]
        current = 0
        results = []

        while remaining:
            available = [p for p in remaining if p.arrival <= current]

            if not available:
                current = min(p.arrival for p in remaining)
                continue

            p = min(available, key=lambda x: x.burst)
            start = max(current, p.arrival)
            finish = start + p.burst

            results.append(SchedulingResult(p.pid, p.arrival, p.burst, start, finish))

            current = finish
            remaining.remove(p)

        self.display(results, "SJF")

    # priority
    def run_priority(self):
        remaining = self.processes[:]
        current = 0
        results = []

        while remaining:
            available = [p for p in remaining if p.arrival <= current]

            if not available:
                current = min(p.arrival for p in remaining)
                continue

            p = max(available, key=lambda x: x.priority)
            start = max(current, p.arrival)
            finish = start + p.burst

            results.append(SchedulingResult(p.pid, p.arrival, p.burst, start, finish))

            current = finish
            remaining.remove(p)

        self.display(results, "Priority")

    # round robin
    def run_rr(self):
        quantum = simpledialog.askinteger("Quantum", "Enter time quantum:", initialvalue=4)
        if not quantum:
            return

        queue = self.processes[:]
        remaining = {p.pid: p.burst for p in queue}
        time = 0
        results = {}

        while queue:
            p = queue.pop(0)

            if p.pid not in results:
                results[p.pid] = {"start": time, "arrival": p.arrival, "burst": p.burst}

            exec_time = min(quantum, remaining[p.pid])
            time += exec_time
            remaining[p.pid] -= exec_time

            if remaining[p.pid] > 0:
                queue.append(p)
            else:
                results[p.pid]["finish"] = time

        final = []
        for pid, data in results.items():
            final.append(SchedulingResult(
                pid, data["arrival"], data["burst"],
                data["start"], data["finish"]
            ))

        self.display(final, f"Round Robin (q={quantum})")

    #multilevel queue scheduling - went back and forth between this and MLFQ
    def run_mlq(self):
        def multilevel_queue(processes):
            high_priority = [p for p in processes if p.priority > 5]
            low_priority = [p for p in processes if p.priority <= 5]

            time = 0
            completed = []

            for p in sorted(high_priority, key=lambda x: x.arrival):
                start = max(time, p.arrival)
                finish = start + p.burst
                completed.append(SchedulingResult(p.pid, p.arrival, p.burst, start, finish))
                time = finish

            for p in sorted(low_priority, key=lambda x: x.arrival):
                start = max(time, p.arrival)
                finish = start + p.burst
                completed.append(SchedulingResult(p.pid, p.arrival, p.burst, start, finish))
                time = finish

            return completed

        results = multilevel_queue(self.processes)
        self.display(results, "MLQ")

    # shortest remaining time left, preemptive version of sjf
    def run_srtf(self):
        processes = []
        start = 0
        finish = 0
        for p in self.processes:
            processes.append(SchedulingResult(p.pid, p.arrival, p.burst, start, finish))

        time = 0
        completed = 0
        n = len(processes)

        while completed < n:
            available = [p for p in processes if p.arrival <= time and p.burst > 0]
            if not available:
                time += 1
                continue

            current = min(available, key=lambda x: x.burst)

            if current.start is None:
                current.start = time

            current.burst -= 1
            time += 1

            if current.burst == 0:
                current.finish = time
                completed += 1

        results = []
        for p in processes:
            results.append(SchedulingResult(p.pid, p.arrival, p.burst, p.start, p.finish))

        self.display(results, "SRTF")

    # displays the results of each algorithm
    def display(self, results, name):
        self.result_box.delete(1.0, tk.END)
        self.result_box.insert(tk.END, f"Algorithm: {name}\n\n")

        total_wait = 0
        total_turn = 0
        total_burst = sum(p.burst for p in self.processes)
        total_time = max(r.finish for r in results)
        cutilization = (total_burst / total_time) * 100
        throughput = len(self.processes) / total_time

        for r in results:
            self.result_box.insert(tk.END,
                                   f"{r.pid}: Start={r.start}, Finish={r.finish}, "
                                   f"Wait={r.waiting}, Turn={r.turnaround}\n, CPU Utilization={cutilization}%\n, Throughput={throughput} processes/unit\n, Response Time={r.rtime}\n")
            total_wait += r.waiting
            total_turn += r.turnaround

        n = len(results)
        self.result_box.insert(tk.END, "\n--- Summary ---\n")
        self.result_box.insert(tk.END, f"Avg Waiting: {total_wait / n:.2f}\n")
        self.result_box.insert(tk.END, f"Avg Turnaround: {total_turn / n:.2f}\n")


# runs interface
if __name__ == "__main__":
    root = tk.Tk()
    app = CpuScheduler(root)
    root.mainloop()

