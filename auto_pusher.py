import os
import subprocess

# Define your GitHub repository path and the branch name
repo_path = "/path/to/your/repository"  # Local path to your repo
branch_name = "main"  # Or the name of the branch you're working with

# Navigate to the repository directory
os.chdir(repo_path)

# Function to commit and push changes to GitHub
def commit_and_push_to_github():
    try:
        # Check for uncommitted changes
        status = subprocess.check_output(['git', 'status', '--porcelain']).decode('utf-8')
        
        if status:
            # Add all changes to staging
            subprocess.run(['git', 'add', '.'])
            
            # Commit changes with a user-provided commit message
            commit_message = input("Enter your commit message: ")
            subprocess.run(['git', 'commit', '-m', commit_message])
            
            # Push changes to the specified branch
            subprocess.run(['git', 'push', 'origin', branch_name])
            print(f"Changes successfully pushed to {branch_name} at GitHub.")
        else:
            print("No changes to commit.")
    except subprocess.CalledProcessError as e:
        print(f"Error during git operation: {e}")

# Call the function to commit and push
commit_and_push_to_github()
