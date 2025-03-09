import pandas as pd
import random
import csv

# Define realistic Indian names
indian_names = [
    "Aarav Sharma", "Aditi Patel", "Arjun Singh", "Ananya Gupta", "Aryan Kumar", 
    "Diya Reddy", "Ishaan Joshi", "Kavya Mehta", "Vihaan Verma", "Riya Malhotra",
    "Rohan Agarwal", "Neha Kapoor", "Vikram Choudhury", "Priya Desai", "Rahul Nair",
    "Shreya Iyer", "Aditya Khanna", "Meera Banerjee", "Karan Mehra", "Pooja Rao",
    "Dhruv Chauhan", "Tanvi Saxena", "Nikhil Menon", "Sanya Bhatia", "Varun Pillai",
    "Aisha Sharma", "Arnav Mukherjee", "Nisha Singhania", "Vivaan Chakraborty", "Sanjana Hegde",
    "Aryan Thakur", "Anushka Goyal", "Kabir Bajaj", "Zara Khan", "Reyansh Trivedi",
    "Saanvi Chawla", "Shaurya Malik", "Anika Suri", "Advait Tiwari", "Myra Ahuja",
    "Vedant Bose", "Ishita Sengupta", "Aarush Dutta", "Tara Rathore", "Krish Venkatesh",
    "Avni Chopra", "Virat Mathur", "Kiara Naidu", "Ayaan Lal", "Ira Bhattacharya",
    "Shivam Rajput", "Anvi Mishra", "Yuvan Yadav", "Navya Kulkarni", "Rudra Shetty",
    "Pari Mahajan", "Aaryan Mistry", "Saisha Goel", "Kabir Chhabra", "Kyra Kaur",
    "Veer Bhatnagar", "Shanaya Prasad", "Armaan Walia", "Aadhya Arora", "Rehan Gill",
    "Amaira Khurana", "Vivaan Parekh", "Anaya Kashyap", "Ayush Basu", "Aarohi Chandra",
    "Shaan Madan", "Aanya Bhandari", "Vihaan Tandon", "Siya Kohli", "Rishaan Ganguly",
    "Mira Bakshi", "Aarav Dhawan", "Disha Dalal", "Arjun Varma", "Samaira Sethi",
    "Advaith Nayar", "Trisha Oberoi", "Kabir Bhalla", "Zoya Grewal", "Vivaan Sood",
    "Anvi Wadhwa", "Aarush Khosla", "Myra Uppal", "Ishaan Luthra", "Anika Batra",
    "Dhruv Anand", "Siya Mallik", "Aaryan Bhardwaj", "Saanvi Chaudhary", "Veer Kashyap",
    "Aisha Dewan", "Aryan Sahni", "Ananya Bahl", "Reyansh Grover", "Tara Kalra"
]

# Define realistic tech skills grouped by category
tech_skills = {
    "Programming Languages": [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Ruby", "Go", "PHP", "Swift", "Kotlin", "Rust"
    ],
    "Web Development": [
        "React", "Angular", "Vue.js", "Node.js", "Express.js", "Django", "Flask", "Spring Boot", "ASP.NET", 
        "HTML5", "CSS3", "SASS", "Bootstrap", "Tailwind CSS", "jQuery", "Next.js", "GraphQL", "REST API"
    ],
    "Mobile Development": [
        "React Native", "Flutter", "Android SDK", "iOS Development", "Xamarin", "Kotlin", "Swift", "Jetpack Compose"
    ],
    "Databases": [
        "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Oracle", "SQL Server", "Redis", "Cassandra", "DynamoDB", "Firebase"
    ],
    "DevOps & Cloud": [
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "GitLab CI/CD", "Terraform", "Ansible", "Prometheus",
        "Grafana", "ELK Stack", "Linux", "Bash Scripting", "Nginx", "Apache"
    ],
    "Data Science & AI": [
        "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "Matplotlib", "Seaborn", "Keras", "NLTK", "OpenCV",
        "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "Data Analysis", "Big Data", "Hadoop", "Spark"
    ],
    "Other": [
        "Git", "Agile", "Scrum", "Jira", "Confluence", "RESTful API Design", "Microservices", "Unit Testing", 
        "Selenium", "Jest", "Cypress", "Blockchain", "Cybersecurity", "UI/UX Design", "Figma", "Adobe XD"
    ]
}

# Define realistic education backgrounds
education_backgrounds = [
    "B.Tech in Computer Science, IIT Delhi",
    "B.Tech in Information Technology, NIT Trichy",
    "B.E. in Computer Science, BITS Pilani",
    "B.Tech in Electronics, IIT Bombay",
    "MCA, Delhi University",
    "M.Tech in Software Engineering, IIT Kanpur",
    "B.Tech in Computer Science, VIT Vellore",
    "B.E. in Information Technology, PEC Chandigarh",
    "B.Tech in Computer Science, IIIT Hyderabad",
    "MSc in Computer Science, IISc Bangalore",
    "B.Tech in IT, Manipal Institute of Technology",
    "B.E. in Computer Engineering, Thapar University",
    "B.Tech in CSE, SRM University",
    "M.Tech in AI & ML, IIT Madras",
    "B.Tech in ECE, NIT Warangal",
    "B.Sc in Computer Science, St. Xavier's College",
    "BCA, Christ University",
    "B.Tech in CSE, LPU",
    "B.E. in Software Engineering, Coimbatore Institute of Technology",
    "M.Tech in Data Science, IIT Roorkee"
]

# Define realistic company names for internships
companies = [
    "Microsoft", "Google", "Amazon", "Flipkart", "Infosys", "TCS", "Wipro", "HCL", "Tech Mahindra", 
    "IBM", "Accenture", "Cognizant", "Capgemini", "Oracle", "SAP", "Zomato", "Swiggy", "Paytm", 
    "Ola", "Uber", "Myntra", "MakeMyTrip", "Razorpay", "BYJU'S", "Unacademy", "PhonePe", "Freshworks",
    "Zoho", "Reliance Jio", "Airtel", "Deloitte", "PwC", "EY", "KPMG"
]

# Define realistic job titles
job_titles = [
    "Software Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer", 
    "Mobile App Developer", "Data Scientist", "Machine Learning Engineer", "DevOps Engineer",
    "Cloud Architect", "Database Administrator", "UI/UX Designer", "Product Manager",
    "QA Engineer", "Automation Tester", "Systems Analyst", "Network Engineer",
    "Security Analyst", "Blockchain Developer", "Game Developer", "AR/VR Developer"
]

# Generate realistic email based on name
def generate_email(name):
    name_parts = name.lower().split()
    domain = random.choice(['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com'])
    
    email_formats = [
        f"{name_parts[0]}.{name_parts[1]}@{domain}",
        f"{name_parts[0]}{name_parts[1]}@{domain}",
        f"{name_parts[0]}{name_parts[1]}{random.randint(1, 999)}@{domain}",
        f"{name_parts[0][0]}{name_parts[1]}@{domain}",
        f"{name_parts[0]}.{name_parts[1][:1]}@{domain}"
    ]
    
    return random.choice(email_formats)

# Generate realistic phone number
def generate_phone():
    return f"+91 {random.randint(6, 9)}{random.randint(100, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}"[:14]

# Generate realistic skills for a candidate
def generate_skills():
    num_skill_categories = random.randint(1, 4)  # Each person knows 1-4 skill categories
    selected_categories = random.sample(list(tech_skills.keys()), num_skill_categories)
    
    all_skills = []
    for category in selected_categories:
        num_skills = random.randint(2, 5)  # 2-5 skills from each category
        category_skills = random.sample(tech_skills[category], min(num_skills, len(tech_skills[category])))
        all_skills.extend(category_skills)
    
    return ", ".join(all_skills)

# Generate realistic internship details
def generate_internship():
    company = random.choice(companies)
    duration = random.randint(1, 6)
    job_title = random.choice(job_titles)
    return f"{job_title} Intern at {company} for {duration} months"

# Generate dataset
def generate_dataset(num_candidates=100):
    data = []
    
    # Shuffle the names to get random selection
    shuffled_names = random.sample(indian_names, min(num_candidates, len(indian_names)))
    
    for i, name in enumerate(shuffled_names):
        email = generate_email(name)
        phone = generate_phone()
        education = random.choice(education_backgrounds)
        skills = generate_skills()
        internship = generate_internship()
        
        data.append({
            "Name": name,
            "Email": email,
            "Phone Number": phone,
            "Education": education,
            "Technical Skills": skills,
            "Internships": internship,
            "Current Job": random.choice(job_titles) if random.random() > 0.3 else "Seeking opportunities"
        })
    
    return pd.DataFrame(data)

# Generate and save the dataset
df = generate_dataset(100)
df.to_csv("realistic_resumes_dataset.csv", index=False)

print("✅ Realistic resume dataset generated successfully!") 