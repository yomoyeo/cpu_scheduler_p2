import tkinter as tk
from tkinter import messagebox, simpledialog



class Helper:
    quantum_time = None

class Algorithms:

    @staticmethod
    def run_fcfs(root, process_count_input):
        try:
            process_count = int(process_count_input)
            if process_count <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Invalid number of processes")
            return

        if not messagebox.askyesno("FCFS", "First Come First Serve Scheduling"):
            return

        burst_times = []
        waiting_times = [0] * process_count

        # Input burst times
        for i in range(process_count):
            val = simpledialog.askfloat("Input", f"Burst time for P{i+1}:", parent=root)
            if val is None or val < 0:
                messagebox.showerror("Error", "Invalid burst time")
                return
            burst_times.append(val)

        # Calculate waiting times
        for i in range(1, process_count):
            waiting_times[i] = waiting_times[i - 1] + burst_times[i - 1]
            messagebox.showinfo("Job Queue",
                                f"Waiting time for P{i+1} = {waiting_times[i]}")

        avg = sum(waiting_times) / process_count
        messagebox.showinfo("Average Waiting Time",
                            f"Average waiting time = {avg:.2f} sec(s)")

    # -----------------------------
    @staticmethod
    def run_sjf(root, process_count_input):
        try:
            process_count = int(process_count_input)
            if process_count <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Invalid number of processes")
            return

        if not messagebox.askyesno("SJF", "Shortest Job First Scheduling"):
            return

        burst = []
        waiting = [0] * process_count

        for i in range(process_count):
            val = simpledialog.askfloat("Input", f"Burst time for P{i+1}:", parent=root)
            if val is None or val < 0:
                messagebox.showerror("Error", "Invalid burst time")
                return
            burst.append(val)

        sorted_burst = sorted(burst)

        used = [False] * process_count

        for i in range(process_count):
            for j in range(process_count):
                if burst[j] == sorted_burst[i] and not used[j]:
                    if i == 0:
                        waiting[i] = 0
                    else:
                        waiting[i] = waiting[i - 1] + sorted_burst[i - 1]

                    messagebox.showinfo("Waiting Time",
                                        f"Waiting time for P{j+1} = {waiting[i]}")

                    used[j] = True
                    break

        avg = sum(waiting) / process_count
        messagebox.showinfo("Average Waiting Time",
                            f"Average waiting time = {avg:.2f} sec(s)")

    # -----------------------------
    @staticmethod
    def run_priority(root, process_count_input):
        try:
            process_count = int(process_count_input)
            if process_count <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Invalid number of processes")
            return

        if not messagebox.askyesno("Priority", "Priority Scheduling"):
            return

        burst = []
        priority = []
        waiting = [0] * process_count

        for i in range(process_count):
            b = simpledialog.askfloat("Input", f"Burst time for P{i+1}:", parent=root)
            if b is None or b < 0:
                messagebox.showerror("Error", "Invalid burst time")
                return
            burst.append(b)

        for i in range(process_count):
            p = simpledialog.askinteger("Input", f"Priority for P{i+1}:", parent=root)
            if p is None or p < 0:
                messagebox.showerror("Error", "Invalid priority")
                return
            priority.append(p)

        sorted_priority = sorted(priority)

        used = [False] * process_count
        last_index = 0

        for i in range(process_count):
            for j in range(process_count):
                if priority[j] == sorted_priority[i] and not used[j]:
                    if i == 0:
                        waiting[i] = 0
                    else:
                        waiting[i] = waiting[i - 1] + burst[last_index]

                    messagebox.showinfo("Waiting Time",
                                        f"Waiting time for P{j+1} = {waiting[i]}")

                    used[j] = True
                    last_index = j
                    break

        avg = sum(waiting) / process_count
        messagebox.showinfo("Average Waiting Time",
                            f"Average waiting time = {avg:.2f} sec(s)")

    # -----------------------------
    @staticmethod
    def run_round_robin(root, process_count_input):
        try:
            process_count = int(process_count_input)
            if process_count <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Invalid number of processes")
            return

        if not messagebox.askyesno("Round Robin", "Round Robin Scheduling"):
            return

        arrival = []
        burst = []
        remaining = []

        for i in range(process_count):
            a = simpledialog.askfloat("Input", f"Arrival time for P{i+1}:", parent=root)
            b = simpledialog.askfloat("Input", f"Burst time for P{i+1}:", parent=root)

            if a is None or b is None or a < 0 or b < 0:
                messagebox.showerror("Error", "Invalid input")
                return

            arrival.append(a)
            burst.append(b)
            remaining.append(b)

        quantum = simpledialog.askfloat("Input", "Time Quantum:", parent=root)
        Helper.quantum_time = quantum
        if quantum is None or quantum <= 0:
            messagebox.showerror("Error", "Invalid quantum time")
            return

        time = 0
        wait = 0
        turnaround = 0
        remaining_processes = process_count

        i = 0
        while remaining_processes > 0:
            if remaining[i] > 0:
                if remaining[i] <= quantum:
                    time += remaining[i]
                    remaining[i] = 0
                    remaining_processes -= 1

                    tat = time - arrival[i]
                    wt = tat - burst[i]

                    messagebox.showinfo("Turnaround",
                                        f"P{i+1} Turnaround = {tat}")
                    messagebox.showinfo("Waiting",
                                        f"P{i+1} Waiting = {wt}")

                    turnaround += tat
                    wait += wt
                else:
                    remaining[i] -= quantum
                    time += quantum

            i = (i + 1) % process_count

        messagebox.showinfo("Average",
                            f"Average Wait = {wait/process_count:.2f}")
        messagebox.showinfo("Average",
                            f"Average Turnaround = {turnaround/process_count:.2f}")


# -----------------------------
# Simple UI to test
# -----------------------------
def main():
    root = tk.Tk()
    root.title("CPU Scheduler Algorithms")
    root.geometry("300x250")

    tk.Label(root, text="Process Count:").pack(pady=5)
    entry = tk.Entry(root)
    entry.pack()

    tk.Button(root, text="FCFS",
              command=lambda: Algorithms.run_fcfs(root, entry.get())).pack(pady=5)

    tk.Button(root, text="SJF",
              command=lambda: Algorithms.run_sjf(root, entry.get())).pack(pady=5)

    tk.Button(root, text="Priority",
              command=lambda: Algorithms.run_priority(root, entry.get())).pack(pady=5)

    tk.Button(root, text="Round Robin",
              command=lambda: Algorithms.run_round_robin(root, entry.get())).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()