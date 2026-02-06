
import os
import ats_logic
import generator

def test_logic():
    print("Testing ATS Logic...")
    data = {
        'full_name': 'John Doe',
        'email': 'john@example.com',
        'phone': '123-456-7890',
        'summary': 'Experienced Software Engineer with a track record of success.',
        'experience': [
            {'responsibilities': 'Developed a new feature using Python. Increased efficiency by 20%.'}
        ]
    }
    score, feedback = ats_logic.calculate_ats_score(data)
    print(f"Score: {score}")
    print(f"Feedback: {feedback}")
    assert score > 0
    print("Logic Test Passed!")

def test_generation():
    print("Testing Generation...")
    data = {
        'full_name': 'Test User',
        'email': 'test@test.com',
        'phone': '1234567890',
        'summary': 'This is a test summary for the resume.',
        'skills': 'Python, Java, C++',
        'experience': [
            {
                'company': 'Tech Corp',
                'location': 'New York, NY',
                'title': 'Senior Developer',
                'start_date': '2020',
                'end_date': 'Present',
                'responsibilities': 'Managed team.\n wrote code.'
            }
        ]
    }
    
    # DOCX
    out_docx = "test_resume.docx"
    generator.generate_resume(data, out_docx, 'docx')
    if os.path.exists(out_docx):
        print(f"DOCX Generated: {out_docx}")
    else:
        print("DOCX Generation Failed")

    # PDF
    out_pdf = "test_resume.pdf"
    generator.generate_resume(data, out_pdf, 'pdf')
    if os.path.exists(out_pdf):
        print(f"PDF Generated: {out_pdf}")
    else:
        print("PDF Generation Failed")

if __name__ == "__main__":
    test_logic()
    test_generation()
