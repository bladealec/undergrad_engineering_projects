import random

def assign_team(difficulty_level, team_members):
    """
    Assign team members to a project based on the difficulty level.

    Parameters:
        difficulty_level (int): The difficulty level of the project (1-10).
        team_members (list): List of team members.

    Returns:
        tuple: Two lists -
            - Team members for research.
            - Team members for presentation (chosen from research team).
    """
    if not (1 <= difficulty_level <= 10):
        raise ValueError("Difficulty level must be between 1 and 10.")

    # Determine team sizes based on difficulty level
    research_team_size = max(2, min(5, difficulty_level))  # Research team size scales with difficulty
    presentation_team_size = max(1, min(3, difficulty_level // 3))  # Presentation team size scales with difficulty

    # Select team members
    research_team = random.sample(team_members, research_team_size)
    presentation_team = random.sample(research_team, presentation_team_size)

    return research_team, presentation_team

# List of available team members
team_members = ["Alec", "David", "Steven", "Mia", "Karla", "Lucas", "Thomas"]

# Get user input for difficulty level
difficulty_level = int(input("Enter the difficulty level of the project (1-10): "))

# Assign team members based on the difficulty level
try:
    research_team, presentation_team = assign_team(difficulty_level, team_members)
    print(f"Research team ({len(research_team)} members): {', '.join(research_team)}")
    print(f"Presentation team ({len(presentation_team)} members from research team): {', '.join(presentation_team)}")
except ValueError as e:
    print(e)
