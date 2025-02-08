class Task:
    def __init__(self, name, optimistic, most_likely, pessimistic):
        self.name = name
        self.optimistic = optimistic
        self.most_likely = most_likely
        self.pessimistic = pessimistic
        self.expected_time = self.calculate_expected_time()
        self.variance = self.calculate_variance()

    def calculate_expected_time(self):
        return (self.optimistic + 4 * self.most_likely + self.pessimistic) / 6

    def calculate_variance(self):
        return ((self.pessimistic - self.optimistic) / 6) ** 2

    def __str__(self):
        return f"Task: {self.name}, Optimistic: {self.optimistic}, Most Likely: {self.most_likely}, Pessimistic: {self.pessimistic}, Expected Time: {self.expected_time}, Variance: {self.variance}"

class PERTAnalysis:
    def __init__(self):
        self.tasks = []

    def add_task(self, name, optimistic, most_likely, pessimistic):
        task = Task(name, optimistic, most_likely, pessimistic)
        self.tasks.append(task)

    def show_results(self):
        total_expected_time = 0
        total_variance = 0
        print("PERT Analysis Results:\n")
        for task in self.tasks:
            print(task)
            total_expected_time += task.expected_time
            total_variance += task.variance
        total_std_dev = total_variance ** 0.5
        print(f"\nTotal Expected Time: {total_expected_time}")
        print(f"Total Variance: {total_variance}")
        print(f"Total Standard Deviation: {total_std_dev}")

# Example usage
if __name__ == "__main__":
    pert = PERTAnalysis()

    pert.add_task("Task 1", optimistic=2, most_likely=3, pessimistic=5)
    pert.add_task("Task 2", optimistic=1, most_likely=2, pessimistic=4)
    pert.add_task("Task 3", optimistic=4, most_likely=6, pessimistic=8)

    pert.show_results()
