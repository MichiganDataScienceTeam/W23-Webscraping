import re
import requests
import json
from bs4 import BeautifulSoup, NavigableString

def extract_courses(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Error fetching the page")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Course code patterns
    course_code_pattern = r'(?:^|\. )(\b(?:Winter|Spring|Summer|Fall)\s*\d{4}\s*(?:LING|EECS|MATH|PHYSICS|SI)\s*\d{3}(?:-\d+)?\b|\b(?:LING|EECS|MATH|PHYSICS|SI)\s*\d{3}(?:-\d+)?\b)'
    course_code_regex = re.compile(course_code_pattern, re.IGNORECASE)

    # Keywords that are likely to be associated with courses
    keywords = ['course', 'class', 'lecture', 'seminar', 'workshop', 'tutorial']
    course_pattern = r'(?:^|\. )\b(?:{})\b(?=\s*\d)'.format('|'.join(keywords))
    course_regex = re.compile(course_pattern, re.IGNORECASE)

    unwanted_phrases = [
        "permission from instructor",
        "graduate standing",
        "Minimum grade",
        "prerequisite",
        "Prerequisite"
    ]

    courses = set()
    for text_node in soup.find_all(text=lambda t: isinstance(t, NavigableString) and (t.parent.name != 'script' and t.parent.name != 'style')):
        line = text_node.strip().replace('\n', ' ')
        if (course_code_regex.search(line) or course_regex.search(line)) and any(char.isdigit() for char in line):
            if not any(phrase in line for phrase in unwanted_phrases):
                cleaned_line = re.sub(r'\s+', ' ', line)
                courses.add(cleaned_line)

    return list(courses)


def save_courses_to_json(professor_name, courses, filename):
    try:
        with open(filename, 'r') as infile:
            data = json.load(infile)
    except FileNotFoundError:
        data = {}

    if professor_name in data:
        print(f"{professor_name} already exists in {filename}. Skipping overwrite.")
    else:
        data[professor_name] = courses
        with open(filename, 'w') as outfile:
            json.dump(data, outfile, indent=4)

if __name__ == "__main__":
    professor_urls = [
        ("Steven Abney", "http://www.vinartus.net/spa/teaching.html"),
        ("William 'Bill' Arthur", "https://web.eecs.umich.edu/~warthur/"),
        ("Nikola Banovic", "http://www.nikolabanovic.net/"),
        ("Valeria Bertacco", "https://web.eecs.umich.edu/~valeria/teaching/"),
        ("Mark Brehob", "https://web.eecs.umich.edu/~brehob/teaching.htm"),
        ("Joyce Y. Chai", "https://web.eecs.umich.edu/~chaijy/teach.html"),
        ("Mithun Chakraborty", "https://sites.google.com/umich.edu/mithunchakra/teaching"),
        ("Michal Derezinski","https://web.eecs.umich.edu/~derezin/")

        # Add more tuples with professor names and URLs as needed
    ]
    filename = "courses.json"
    for professor_name, url in professor_urls:
        courses = extract_courses(url)
        if courses:
            print(f"{len(courses)} courses found for {professor_name}!")
            # for course in courses:
            #     print(course)
            save_courses_to_json(professor_name, courses, filename)
        else:
            print(f"No courses found for {professor_name}")

