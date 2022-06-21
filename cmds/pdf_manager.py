from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from PIL import Image 
from os import path


def merge_pdfs(pdfs: list, temp_path):
    pdf_merger = PdfMerger()
    pdf_output = f"{temp_path}/merged.pdf"
    for i in pdfs:
        pdf_merger.append(i)
    pdf_merger.write(pdf_output)
    pdf_merger.close()
    return pdf_output

def images_to_pdf(images: list, temp_path):
    if len(images) == 1:
        pdf_output = f"{temp_path}/{path.splitext(images[0])[0]}.pdf"
        pic = Image.open(images[0]).convert('RGB')
        pic.save(pdf_output)
        return pdf_output
    else:
        images_to_save = []
        pdf_output = f"{temp_path}/images_to_p.pdf"
        for i in images:
            pic = Image.open(i).convert('RGB')
            images_to_save.append(pic)
        images_to_save[0].save(pdf_output, save_all=True, append_images=images_to_save[1:])
        return pdf_output

def compress_pdf(pdf, temp_path):
    pdf_reader = PdfReader(pdf)
    pdf_writer = PdfWriter()

    pdf_output = f"{path.splitext(pdf)[0]}_compress.pdf"

    for page in pdf_reader.pages:
        page.compressContentStreams()
        pdf_writer.add_page(page)

    with open(pdf_output, 'wb') as file:
        pdf_writer.write(file)

    return pdf_output