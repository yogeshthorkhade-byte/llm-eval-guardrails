from pypdf import PdfReader


# --------------------------------
# Load PDF
# --------------------------------

def load_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""


    for page in reader.pages:

        extracted = page.extract_text()


        if extracted:

            text += extracted


    # Debug output
    print("\n========= PDF TEXT =========\n")

    print(text[:1000])

    print("\n============================\n")


    return text