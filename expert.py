import nltk
from nltk.tokenize import word_tokenize
from collections import defaultdict
from difflib import get_close_matches

nltk.download('punkt')

class CareerCounselingSystem:
    def __init__(self):
        self.knowledge_base = {
            "Technology": {"skills": ["Programming", "Problem-solving", "Coding", "AI", "Cybersecurity"], "careers": ["Software Developer", "Data Scientist", "Cybersecurity Analyst"]},
            "Healthcare": {"skills": ["Empathy", "Medical Knowledge", "Biology", "Chemistry"], "careers": ["Doctor", "Nurse", "Medical Researcher"]},
            "Business": {"skills": ["Leadership", "Finance", "Marketing", "Strategy"], "careers": ["Entrepreneur", "Financial Analyst", "Marketing Manager"]},
            "Creative Arts": {"skills": ["Creativity", "Design", "Writing", "Deejaying", "DJ", "Singing", "Dancing", "Drawing", "Choreography"], "careers": ["Graphic Designer", "Musician", "Content Creator"]},
        }
        self.unknown_skills = set()

    def process_input(self, text):
        return [word.strip().lower() for word in text.split(",")]

    def find_closest_match(self, skill):
        all_skills = [skill for field in self.knowledge_base.values() for skill in field["skills"]]
        matches = get_close_matches(skill, all_skills, n=1, cutoff=0.7)
        return matches[0] if matches else None

    def get_recommendations(self, interests, skills):
        matched_careers = defaultdict(int)
        
        for field, data in self.knowledge_base.items():
            field_matched = any(interest.lower() in field.lower() for interest in interests)

            for skill in skills:
                normalized_skill = skill.lower()
                if normalized_skill in [s.lower() for s in data["skills"]]:
                    for career in data["careers"]:
                        matched_careers[career] += 2 if field_matched else 1  # Higher weight if field also matched
                else:
                    closest_match = self.find_closest_match(normalized_skill)
                    if closest_match:
                        for career in data["careers"]:
                            matched_careers[career] += 1 if field_matched else 0.5
                    else:
                        self.unknown_skills.add(skill)

        sorted_careers = sorted(matched_careers.items(), key=lambda x: x[1], reverse=True)
        return [career for career, score in sorted_careers if score > 0]


    def display_unknown_skills(self):
        if self.unknown_skills:
            print("\nThe following skills were not found in our database:")
            for skill in self.unknown_skills:
                print(f"- {skill}")
            print("Consider refining your input or exploring related skills.")


def main():
    system = CareerCounselingSystem()
    print("Welcome to the AI Career Counseling System!")
    
    interests_input = input("Enter your interests (comma-separated): ")
    skills_input = input("Enter your skills (comma-separated): ")
    
    interests = system.process_input(interests_input)
    skills = system.process_input(skills_input)
    
    recommendations = system.get_recommendations(interests, skills)
    
    print("\nRecommended Careers:")
    for career in recommendations:
        print(f"- {career}")
    
    system.display_unknown_skills()


if __name__ == "__main__":
    main()
