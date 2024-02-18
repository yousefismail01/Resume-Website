# Name: Yousef Ismail
# Penn ID: 76072638
# Outside Resources: Stack Overflow

def read_resume_file(filename):
    """
    Read the contents of a file and return it as a list of lines.

    This function opens a file for reading, reads all lines in the file,
    and returns a list where each element is a line from the file.
    """

    # Open the file in read mode ('r') and bind it to the variable 'file'
    with open(filename, 'r') as file:
        # Read all lines from the file and store them in a list
        lines = file.readlines()

    # Return the list of lines read from the file
    return lines

def read_and_prepare_html_template(template_filename, resume_content):
    """
    Reads an HTML template file, removes the last 2 lines (</body> and </html>),
    adds custom resume content, and prepares the final HTML content.
    """
    with open(template_filename, 'r') as file:
        lines = file.readlines()
    
    # Remove the last 2 lines (assuming they are </body> and </html>)
    lines = lines[:-2]

    lines.append('<div id="page-wrap">')
    
    # Add the resume content
    lines.append(resume_content)
    
    # Add back the closing tags
    lines.append('</div>\n</body>\n</html>')
    
    return ''.join(lines)

def detect_name(lines):
    """
    Detects and returns the name from the first line of a list of lines, assuming the resume's name is on the first line.
    """
    if lines: # Check if the list of lines is not empty
        name = lines[0].strip() # Extract the first line and remove any leading/trailing whitespace
        if name and name[0].isupper():  # Validate that the name is not empty and starts with an uppercase letter
            return name # Return the validated name

    # If the list is empty, the name is empty, or the name does not start with an uppercase letter, return default message
    return 'Invalid Name...'

def detect_email(lines):
    """
    Detect and return the first valid email address found in a list of strings.
    """
    for line in lines:
        line = line.strip() # Remove leading and trailing whitespace
        if '@' in line: # Check if the line contains '@' symbol
            aT_index = line.index('@') # Get the index of '@' in the string

            # Ensure the character immediately after '@' is a lowercase letter
            if not line[aT_index + 1].islower():
                continue # Skip to the next line if the condition is not met

            # Check if the line contains any digit; if so, skip to the next line
            if any(char.isdigit() for char in line):
                continue

             # The email must end with either '.com' or '.edu'           
            if not(line.endswith('.com') or line.endswith('.edu')):
                continue

            # If all conditions are met, return the email address
            return line

    # If no valid email is found after checking all lines, return 'Invalid Email'    
    return 'Invalid Email'

def detect_courses(lines):
    """
    Extracts a list of courses from the given text lines.

    This function searches through each line for the keyword "Courses" and extracts
    the courses listed after it.
    """
    for line in lines:
        if "Courses" in line:
            # Find the index where "Courses" starts
            start_index = line.find("Courses") + len("Courses")

            # Iterate over the characters starting from the index right after "Courses"
            # to find the first alphabetical character, indicating the start of the course names.
            for i in range(start_index, len(line)):
                if line[i].isalpha():

                    # Extract the courses string from this point
                    courses_str = line[i:]
                    
                    # Split the courses string on commas to get the individual course names,
                    # then strip whitespace from each name for clean-up.
                    courses = [course.strip() for course in courses_str.split(',')]
                    return courses
                    
    # Return an empty list if no courses section is found in the input lines  
    return []

def detect_projects(lines):
    """
    Detects and extracts the projects listed in the resume text.

    This function scans the lines of text for a section starting with "Projects"
    and collects all the following non-empty lines until a line with "----------"
    is encountered, signifying the end of the section. 
    """
    projects = []  # Initialize an empty list to store project descriptions.
    in_projects_section = False  # Flag to track whether the current line is within the projects section.

    for line in lines:
        # Check if the current line marks the beginning of the Projects section.
        if "Projects" in line:
            in_projects_section = True  # Update flag to indicate we're in the Projects section.
            continue

        # If we're in the Projects section and encounter a separator line, it means the section has ended.
        if in_projects_section:
            if "----------" in line:
                break

            line = line.strip()
            if line: # Ignores any blank lines
                projects.append(line)
    
    return projects

def surround_block(tag, text):
    """
    Surrounds the given text with the given html tag and returns the string.
    """
    return f"<{tag}>{text}</{tag}>"

def create_email_link(email_address):
    """
    Creates an email link with the given email_address.
    To cut down on spammers harvesting the email address from the webpage,
    displays the email address with [aT] instead of @.

    Example: Given the email address: lbrandon@wharton.upenn.edu
    Generates the email link: <a href="mailto:lbrandon@wharton.upenn.edu">lbrandon[aT]wharton.upenn.edu</a>

    Note: If, for some reason the email address does not contain @,
    use the email address as is and don't replace anything.
    """
    if '@' in email_address:
        display_email = email_address.replace('@', '[aT]')
    else:
        display_email = email_address
    return f'<a href="mailto:{email_address}">{display_email}</a>'

def generate_html(txt_input_file, html_output_file, html_template_file='resume_template.html'):
    """
    Loads given txt_input_file,
    gets the name, email address, list of projects, and list of courses,
    then writes the info to the given html_output_file.

    # Hint(s):
    # call function(s) to load given txt_input_file
    # call function(s) to get name
    # call function(s) to get email address
    # call function(s) to get list of projects
    # call function(s) to get list of courses
    # call function(s) to write the name, email address, list of projects, and list of courses to the given html_output_file
    """

    # Read resume data from a text file
    lines = read_resume_file(txt_input_file)

    name = detect_name(lines)
    email_address = detect_email(lines)
    projects = detect_projects(lines)
    courses = detect_courses(lines)

    # Start building the HTML content for the resume with the name as a header
    resume_content = f'<h1>{name}</h1>\n'
    # Create a mailto link for the email address, using a function to remove '@' to reduce spam
    email_link = create_email_link(email_address)
    # Add the email link to the resume content
    resume_content += f'<p>Email: {email_link}</p>\n'

    # If there are projects listed in the resume, add them to the HTML content
    if projects:
        resume_content += '<h2>Projects</h2>\n<ul>\n'
        for project in projects:
            # Each project is listed as a bullet point
            resume_content += f'<li>{project}</li>\n'
        resume_content += '</ul>\n'

    # If there are courses listed in the resume, concatenate them into a single string
    if courses:
        # Join course names with a comma and space for readability
        courses_str = ', '.join(courses)  # Join all course names with a comma
        # Add the courses string to the resume content within a paragraph tag
        resume_content += f'<h2>Courses</h2>\n<p>{courses_str}</p>\n'

    # Read the template, insert the resume content, and prepare the final HTML
    final_html = read_and_prepare_html_template(html_template_file, resume_content)

    # Write the final HTML to the output file
    with open(html_output_file, 'w') as file:
        file.write(final_html)

def main():

    # DO NOT REMOVE OR UPDATE THIS CODE
    # generate resume.html file from provided sample resume.txt
    generate_html('resume.txt', 'resume.html')

    # DO NOT REMOVE OR UPDATE THIS CODE.
    # Uncomment each call to the generate_html function when you’re ready
    # to test how your program handles each additional test resume.txt file
    generate_html('TestResumes/resume_bad_name_lowercase/resume.txt', 'TestResumes/resume_bad_name_lowercase/resume.html')
    generate_html('TestResumes/resume_courses_w_whitespace/resume.txt', 'TestResumes/resume_courses_w_whitespace/resume.html')
    generate_html('TestResumes/resume_courses_weird_punc/resume.txt', 'TestResumes/resume_courses_weird_punc/resume.html')
    generate_html('TestResumes/resume_projects_w_whitespace/resume.txt', 'TestResumes/resume_projects_w_whitespace/resume.html')
    generate_html('TestResumes/resume_projects_with_blanks/resume.txt', 'TestResumes/resume_projects_with_blanks/resume.html')
    generate_html('TestResumes/resume_template_email_w_whitespace/resume.txt', 'TestResumes/resume_template_email_w_whitespace/resume.html')
    generate_html('TestResumes/resume_wrong_email/resume.txt', 'TestResumes/resume_wrong_email/resume.html')

    # If you want to test additional resume files, call the generate_html function with the given .txt file
    # and desired name of output .html file

if __name__ == '__main__':
    main()