import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

class GanttTask:
    def __init__(self, name, start_date, duration):
        self.name = name
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.duration = timedelta(days=duration)
        self.end_date = self.start_date + self.duration

    def __str__(self):
        return f"{self.name}: {self.start_date.date()} to {self.end_date.date()}"

class GanttChart:
    def __init__(self):
        self.tasks = []

    def add_task(self, name, start_date, duration):
        task = GanttTask(name, start_date, duration)
        self.tasks.append(task)

    def plot_gantt_chart(self):
        fig, ax = plt.subplots(figsize=(10, 6))

        for i, task in enumerate(self.tasks):
            ax.barh(i, task.duration.days, left=mdates.date2num(task.start_date), height=0.6, label=task.name)

        ax.set_yticks(range(len(self.tasks)))
        ax.set_yticklabels([task.name for task in self.tasks])

        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))

        plt.title("Project Gantt Chart")
        plt.xlabel("Date")
        plt.ylabel("Tasks")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# Example
if __name__ == "__main__":
    gantt = GanttChart()

    gantt.add_task("Design Aircraft Wings", "2025-02-01", 20)
    gantt.add_task("Test Electronics", "2025-02-20", 15)
    gantt.add_task("Prepare Report", "2025-02-25", 10)

    gantt.plot_gantt_chart()
