
import pymupdf

def extract_pdf(pdf_path):

    pdf = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(pdf):

        text = page.get_text()

        if text.strip():
            pages.append({
                "page": page_number + 1,
                "text": text
            })

    pdf.close()

    return pages


if __name__ == "__main__":

    print("PDF Extraction Program Started!")

    file_path = input("Enter PDF path: ")

    pages = extract_pdf(file_path)

    print("\nPDF extraction completed!")
    print("Total pages:", len(pages))

    for page in pages[:2]:
        print("\nPage:", page["page"])
        print(page["text"][:500])
