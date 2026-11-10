# AI-Powered Resume Analyzer
# 1st year mini project. Python standard library only (tkinter).
#
# There is no internet and no extra package.
# The program reads the resume, finds skills and sections,
# compares them with the job text, then gives a score and tips.
#
# How to run:
#   python resume_analyzer.py

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# A skill name and the words that mean the same skill.
# Add a new skill here if you want the analyzer to look for it.
SKILLS = {
    "Python": ["python"],
    "Java": ["java"],
    "C++": ["c++", "cpp"],
    "SQL": ["sql", "mysql"],
    "Git": ["git", "github"],
    "HTML": ["html"],
    "CSS": ["css"],
    "JavaScript": ["javascript", "js"],
    "Excel": ["excel"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Machine Learning": ["machine learning"],
    "Power BI": ["power bi", "powerbi"],
    "Communication": ["communication"],
    "Problem Solving": ["problem solving", "problem-solving"],
    "Data Structures": ["data structures", "dsa"],
    "OOPs": ["oops", "object oriented", "object-oriented"],
    "Teamwork": ["teamwork", "team work", "team player"],
    "Linux": ["linux"],
    "React": ["react"],
}

# These job boxes are filled when the student picks a role.
# The analyzer still reads the text, so editing the box changes the score.
JOB_TEXTS = {
    "Python Developer Intern": (
        "Python Developer Intern\n\n"
        "We need a student who can write small Python programs.\n"
        "Required skills: Python, SQL, Git, OOPs, Data Structures, Pandas, Problem Solving.\n"
        "You will build tools, fix bugs, and work with a team."
    ),
    "Data Analyst Intern": (
        "Data Analyst Intern\n\n"
        "Look at student or sales data and explain it in simple charts.\n"
        "Required skills: Python, SQL, Excel, Pandas, Power BI, Communication, Problem Solving.\n"
        "Tell the story behind the numbers."
    ),
    "Web Developer Intern": (
        "Web Developer Intern\n\n"
        "Build simple web pages and a small project site.\n"
        "Required skills: HTML, CSS, JavaScript, Git, Python, React, Communication.\n"
        "Pages should be clear on a phone and on a laptop."
    ),
    "Custom Job Text": (
        "Type the job you want here.\n"
        "Include skill words such as Python, SQL, Excel, HTML, or Communication.\n"
        "The analyzer only scores skills it knows. Add more in the SKILLS dictionary."
    ),
}

ACTION_WORDS = [
    "built", "created", "developed", "designed", "made",
    "analyzed", "analysed", "improved", "led", "managed",
    "implemented", "automated", "fixed", "wrote",
]

SECTION_WORDS = {
    "Education": ["education", "bachelor", "b.tech", "btech", "b.e", "college", "university", "cgpa", "gpa", "12th", "10th"],
    "Skills": ["skills", "technical skills"],
    "Projects": ["project", "projects"],
    "Experience": ["experience", "intern", "internship", "worked"],
}


def has_phrase(text, phrase):
    """True when phrase appears as its own words, not inside a longer word.

    Example: "java" matches "java", but not "javascript".
    """
    padded = " " + text.lower() + " "
    phrase = phrase.lower()
    start = 0
    while True:
        index = padded.find(phrase, start)
        if index == -1:
            return False
        before = padded[index - 1]
        after = padded[index + len(phrase)]
        if (not before.isalnum()) and (not after.isalnum()):
            return True
        start = index + 1


def find_skills(text):
    found = []
    for skill, phrases in SKILLS.items():
        for phrase in phrases:
            if has_phrase(text, phrase):
                found.append(skill)
                break
    return found


def find_email(text):
    for word in text.replace("\n", " ").split():
        clean = word.strip(".,;:()[]<>")
        if "@" in clean and "." in clean.split("@")[-1]:
            return clean
    return ""


def find_phone(text):
    """Return the first 10-digit number. Spaces and dashes are allowed inside it."""
    number = ""
    for char in text:
        if char.isdigit():
            number += char
            if len(number) == 10:
                return number
        elif char not in " -+()":
            number = ""
    return ""


def words_of(text):
    return [word for word in text.split() if any(ch.isalpha() for ch in word)]


def analyze_resume(resume_text, job_text):
    """Compare one resume with one job. Returns a dictionary of results."""
    resume_text = resume_text.strip()
    job_text = job_text.strip()

    resume_skills = find_skills(resume_text)
    job_skills = find_skills(job_text)

    matched = []
    missing = []
    for skill in job_skills:
        if skill in resume_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    email = find_email(resume_text)
    phone = find_phone(resume_text)
    sections = {}
    for name, phrases in SECTION_WORDS.items():
        sections[name] = any(has_phrase(resume_text, phrase) for phrase in phrases)

    has_contact = email != "" or phone != ""
    has_work = sections["Projects"] or sections["Experience"]

    # 70 points come from the skill match. 30 points come from resume sections.
    if job_skills:
        skill_points = (len(matched) / len(job_skills)) * 70
    else:
        skill_points = 0

    section_points = 0
    if has_contact:
        section_points += 7.5
    if sections["Education"]:
        section_points += 7.5
    if sections["Skills"]:
        section_points += 7.5
    if has_work:
        section_points += 7.5

    score = int(round(skill_points + section_points))

    action_hits = []
    lowered = resume_text.lower()
    for word in ACTION_WORDS:
        if has_phrase(lowered, word):
            action_hits.append(word)

    has_number = any(ch.isdigit() for ch in resume_text)
    word_count = len(words_of(resume_text))

    good = []
    tips = []

    if not resume_text:
        return {
            "score": 0,
            "good": [],
            "tips": ["Paste your resume or load a .txt file first."],
            "matched": [],
            "missing": [],
            "extra": [],
            "email": "",
            "phone": "",
            "word_count": 0,
            "job_skills": job_skills,
        }

    if email:
        good.append("Email found: " + email)
    else:
        tips.append("Add an email address at the top of the resume.")

    if phone:
        good.append("Phone number found.")
    else:
        tips.append("Add a 10-digit phone number near your name.")

    if sections["Education"]:
        good.append("Education section found.")
    else:
        tips.append("Add an Education section with your course, college, and year.")

    if sections["Skills"]:
        good.append("Skills section found.")
    else:
        tips.append("Add a Skills line so the job skills are easy to see.")

    if has_work:
        good.append("Projects or experience found.")
    else:
        tips.append("Add at least one project. Write what you built and which tool you used.")

    if matched:
        good.append("Matched skills: " + ", ".join(matched) + ".")
    if missing:
        tips.append("For this job, try to show: " + ", ".join(missing) + ".")

    extra = []
    for skill in resume_skills:
        if skill not in job_skills:
            extra.append(skill)
    if extra:
        good.append("Other skills on the resume: " + ", ".join(extra) + ".")

    if len(action_hits) >= 2:
        good.append("Strong action words found, such as " + action_hits[0] + ".")
    else:
        tips.append("Start project lines with words like Built, Created, Analyzed, or Improved.")

    if has_number:
        good.append("The resume includes numbers (marks, dates, or results).")
    else:
        tips.append("Add a result with a number, such as CGPA 8.4 or saved 2 hours a week.")

    if word_count < 80:
        tips.append("The resume is very short (" + str(word_count) + " words). Add projects and skills.")
    elif word_count > 700:
        tips.append("The resume is long (" + str(word_count) + " words). Keep the best points for one page.")
    else:
        good.append("Length looks fine for a student resume (" + str(word_count) + " words).")

    if not job_skills:
        tips.insert(0, "The job text has none of the known skills. Type skills such as Python or SQL, or add words in SKILLS.")

    if not tips:
        tips.append("This resume covers the job text well. Ask a friend to read it once for spelling.")

    return {
        "score": score,
        "good": good,
        "tips": tips,
        "matched": matched,
        "missing": missing,
        "extra": extra,
        "email": email,
        "phone": phone,
        "word_count": word_count,
        "job_skills": job_skills,
    }


def format_report(result):
    lines = []
    lines.append("MATCH SCORE: " + str(result["score"]) + " / 100")
    lines.append("")
    lines.append("What looks good")
    if result["good"]:
        for item in result["good"]:
            lines.append("- " + item)
    else:
        lines.append("- Nothing yet. Add your resume text.")
    lines.append("")
    lines.append("What to improve")
    for item in result["tips"]:
        lines.append("- " + item)
    lines.append("")
    lines.append("Score split")
    lines.append("- Up to 70 points: skills in the job that also appear in the resume.")
    if result["job_skills"]:
        lines.append("- Job skills checked: " + ", ".join(result["job_skills"]) + ".")
        lines.append("- Matched " + str(len(result["matched"])) + " of " + str(len(result["job_skills"])) + ".")
    else:
        lines.append("- No known skills were found in the job text, so skill points are 0.")
    lines.append("- Up to 30 points: contact, education, skills section, and a project or experience.")
    return "\n".join(lines)


def read_text_file(path):
    # utf-8-sig handles files saved by Notepad with a hidden first character.
    file = open(path, "r", encoding="utf-8-sig")
    text = file.read()
    file.close()
    return text


def sample_path(name):
    folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(folder, name)


class ResumeApp:
    def __init__(self, root):
        self.root = root
        root.title("AI-Powered Resume Analyzer")
        root.geometry("980x700")
        root.minsize(860, 620)
        root.configure(bg="#f3f6fb")

        self.role_var = tk.StringVar(value="Python Developer Intern")

        header = tk.Frame(root, bg="#0f172a", padx=18, pady=14)
        header.pack(fill="x")
        tk.Label(
            header,
            text="AI-Powered Resume Analyzer",
            bg="#0f172a",
            fg="white",
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w")
        tk.Label(
            header,
            text="By Roshni  ·  Basic Python only. Paste a resume, pick a job, then press Analyze.",
            bg="#0f172a",
            fg="#cbd5e1",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))

        controls = tk.Frame(root, bg="#f3f6fb", padx=16, pady=10)
        controls.pack(fill="x")

        tk.Label(controls, text="Job role", bg="#f3f6fb", fg="#0f172a", font=("Segoe UI", 10, "bold")).pack(side="left")
        self.role_box = ttk.Combobox(
            controls,
            textvariable=self.role_var,
            values=list(JOB_TEXTS.keys()),
            state="readonly",
            width=28,
            font=("Segoe UI", 10),
        )
        self.role_box.pack(side="left", padx=(8, 16))
        self.role_box.bind("<<ComboboxSelected>>", self.on_role_change)

        self.make_button(controls, "Load Resume", self.load_resume).pack(side="left", padx=4)
        self.make_button(controls, "Load Job", self.load_job).pack(side="left", padx=4)
        self.make_button(controls, "Use Sample", self.load_sample).pack(side="left", padx=4)
        self.make_button(controls, "Clear", self.clear_all).pack(side="left", padx=4)

        panes = tk.Frame(root, bg="#f3f6fb", padx=16)
        panes.pack(fill="both", expand=True)

        left = tk.Frame(panes, bg="#f3f6fb")
        right = tk.Frame(panes, bg="#f3f6fb")
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        right.pack(side="left", fill="both", expand=True, padx=(8, 0))

        tk.Label(left, text="Your resume", bg="#f3f6fb", fg="#0f172a", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.resume_box = self.make_text(left)
        tk.Label(right, text="Job description", bg="#f3f6fb", fg="#0f172a", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.job_box = self.make_text(right)

        bottom = tk.Frame(root, bg="#ffffff", padx=16, pady=12, highlightbackground="#e2e8f0", highlightthickness=1)
        bottom.pack(fill="both", expand=True, padx=16, pady=12)

        score_row = tk.Frame(bottom, bg="#ffffff")
        score_row.pack(fill="x")
        self.score_label = tk.Label(
            score_row,
            text="Score: --",
            bg="#ffffff",
            fg="#2563eb",
            font=("Segoe UI", 18, "bold"),
        )
        self.score_label.pack(side="left")
        analyze_btn = tk.Button(
            score_row,
            text="Analyze Resume",
            command=self.analyze,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            padx=16,
            pady=6,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
        )
        analyze_btn.pack(side="right")

        self.report_box = tk.Text(
            bottom,
            height=12,
            wrap="word",
            bg="#f8fafc",
            fg="#0f172a",
            relief="flat",
            padx=10,
            pady=8,
            font=("Segoe UI", 10),
        )
        self.report_box.pack(fill="both", expand=True, pady=(8, 0))
        self.report_box.insert("1.0", "Load the sample or paste your own text, then press Analyze Resume.")
        self.report_box.configure(state="disabled")

        self.load_sample()

    def make_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg="#ffffff",
            fg="#0f172a",
            relief="solid",
            bd=1,
            padx=10,
            pady=4,
            font=("Segoe UI", 10),
            cursor="hand2",
        )

    def make_text(self, parent):
        box = tk.Text(
            parent,
            wrap="word",
            bg="#ffffff",
            fg="#0f172a",
            relief="solid",
            bd=1,
            padx=8,
            pady=8,
            font=("Consolas", 10),
            height=12,
        )
        box.pack(fill="both", expand=True, pady=(4, 0))
        return box

    def set_text(self, box, text):
        box.delete("1.0", "end")
        box.insert("1.0", text)

    def on_role_change(self, event=None):
        role = self.role_var.get()
        self.set_text(self.job_box, JOB_TEXTS[role])

    def load_resume(self):
        path = filedialog.askopenfilename(
            title="Open resume text file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if path:
            self.set_text(self.resume_box, read_text_file(path))

    def load_job(self):
        path = filedialog.askopenfilename(
            title="Open job text file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if path:
            self.role_var.set("Custom Job Text")
            self.set_text(self.job_box, read_text_file(path))

    def load_sample(self):
        self.role_var.set("Python Developer Intern")
        self.set_text(self.resume_box, read_text_file(sample_path("sample_resume.txt")))
        self.set_text(self.job_box, read_text_file(sample_path("sample_job.txt")))

    def clear_all(self):
        self.set_text(self.resume_box, "")
        self.role_var.set("Custom Job Text")
        self.set_text(self.job_box, JOB_TEXTS["Custom Job Text"])
        self.score_label.configure(text="Score: --", fg="#2563eb")
        self.show_report("Boxes cleared. Paste a resume and a job, then press Analyze Resume.")

    def show_report(self, text):
        self.report_box.configure(state="normal")
        self.report_box.delete("1.0", "end")
        self.report_box.insert("1.0", text)
        self.report_box.configure(state="disabled")

    def analyze(self):
        resume = self.resume_box.get("1.0", "end")
        job = self.job_box.get("1.0", "end")
        if resume.strip() == "":
            messagebox.showinfo("Add a resume", "Paste your resume or press Use Sample.")
            return
        result = analyze_resume(resume, job)
        score = result["score"]
        if score >= 75:
            color = "#15803d"
        elif score >= 50:
            color = "#c2410c"
        else:
            color = "#b91c1c"
        self.score_label.configure(text="Score: " + str(score) + " / 100", fg=color)
        self.show_report(format_report(result))


def main():
    root = tk.Tk()
    ResumeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
