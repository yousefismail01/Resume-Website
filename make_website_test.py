import unittest

from make_website import *

class MakeWebsite_Test(unittest.TestCase):

    def test_surround_block(self):
        # test text with surrounding h1 tags
        self.assertEqual("<h1>Eagles</h1>", surround_block('h1', 'Eagles'))

        # test text with surrounding h2 tags
        self.assertEqual("<h2>Red Sox</h2>", surround_block('h2', 'Red Sox'))

        # test text with surrounding p tags
        self.assertEqual('<p>Lorem ipsum dolor sit amet, consectetur ' +
                         'adipiscing elit. Sed ac felis sit amet ante porta ' +
                         'hendrerit at at urna.</p>',
                         surround_block('p', 'Lorem ipsum dolor sit amet, consectetur ' +
                                        'adipiscing elit. Sed ac felis sit amet ante porta ' +
                                        'hendrerit at at urna.'))

    def test_create_email_link(self):

        # test email with @ sign
        self.assertEqual(
            '<a href="mailto:lbrandon@wharton.upenn.edu">lbrandon[aT]wharton.upenn.edu</a>',
            create_email_link('lbrandon@wharton.upenn.edu')
        )

        # test email with @ sign
        self.assertEqual(
            '<a href="mailto:krakowsky@outlook.com">krakowsky[aT]outlook.com</a>',
            create_email_link('krakowsky@outlook.com')
        )

        # test email without @ sign
        self.assertEqual(
            '<a href="mailto:lbrandon.at.seas.upenn.edu">lbrandon.at.seas.upenn.edu</a>',
            create_email_link('lbrandon.at.seas.upenn.edu')
        )
        
class TestDetectName(unittest.TestCase):
    def test_empty_list(self):
        # Test with an empty list.
        self.assertEqual(detect_name([]), 'Invalid Name...')

    def test_correct_name(self):
        # Test with a correctly formatted name.
        self.assertEqual(detect_name(['John Doe']), 'John Doe')

    def test_name_with_whitespace(self):
        # Test with a name that includes leading and trailing whitespace.
        self.assertEqual(detect_name(['  John Doe  ']), 'John Doe')

class TestDetectEmail(unittest.TestCase):
    def test_valid_email(self):
        # Test a valid email address
        lines = ["example@example.com"]
        self.assertEqual(detect_email(lines), "example@example.com")

    def test_invalid_email_no_at_symbol(self):
        # Test an invalid email address without '@' symbol
        lines = ["example.com"]
        self.assertEqual(detect_email(lines), "Invalid Email")

    def test_invalid_email_digit_present(self):
        # Test an invalid email address with digit
        lines = ["example1@example.com"]
        self.assertEqual(detect_email(lines), "Invalid Email")

class TestDetectCourses(unittest.TestCase):
    def test_detect_courses_single_course(self):
        # Test that a single course is detected correctly.
        lines = ["Courses: Introduction to Python"]
        expected = ["Introduction to Python"]
        self.assertEqual(detect_courses(lines), expected)

    def test_detect_courses_no_courses(self):
        # Test that an empty list is returned when no courses are present.
        lines = ["No relevant data here"]
        self.assertEqual(detect_courses(lines), [])

class TestDetectProjects(unittest.TestCase):
    def test_detect_projects_standard_case(self):
        # Test that the function extracts projects correctly from a well-formatted list."""
        lines = [
            "Some intro",
            "Projects",
            "Project 1: A project.",
            "Project 2: Another project.",
            "----------",
            "Some text"
        ]
        expected = ["Project 1: A project.", "Project 2: Another project."]
        self.assertEqual(detect_projects(lines), expected)

    def test_no_projects_section(self):
        # Test that the function returns an empty list if there's no Projects section."""
        lines = ["Some intro", "Some text"]
        expected = []
        self.assertEqual(detect_projects(lines), expected)

class TestSurroundBlock(unittest.TestCase):
    # Test with a standard HTML tag and text
    def test_standard_tag(self):
        self.assertEqual(surround_block('p', 'Hello World'), '<p>Hello World</p>', "Should surround text with <p> tags")
    

if __name__ == '__main__':
    unittest.main()