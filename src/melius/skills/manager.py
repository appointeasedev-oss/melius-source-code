import os
import requests

class SkillManager:
    def __init__(self, skills_dir="skills"):
        self.skills_dir = os.path.abspath(skills_dir)
        if not os.path.exists(self.skills_dir):
            os.makedirs(self.skills_dir)

    def download_skill(self, skill_url, skill_name):
        """Downloads a skill file from a URL."""
        response = requests.get(skill_url)
        if response.status_code == 200:
            file_path = os.path.join(self.skills_dir, f"{skill_name}.py")
            with open(file_path, 'wb') as f:
                f.write(response.content)
            return f"Skill {skill_name} downloaded successfully."
        return f"Failed to download skill from {skill_url}"

    def list_skills(self):
        return [f for f in os.listdir(self.skills_dir) if f.endswith('.py')]
