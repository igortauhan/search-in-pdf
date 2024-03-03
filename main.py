import argparse
from service.system_commands import list_files, convert_pdf_to_text, search_text, delete_file


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="Directory where the PDF files are stored")
    parser.add_argument("text", help="Text to be searched")

    arguments = parser.parse_args()

    return arguments


def find_all_pdfs(directory):
    all_files = list_files(directory)
    pdf_files = []

    for file in all_files:
        if file.__contains__(".pdf"):
            pdf_files.append(file)

    return pdf_files


def convert(directory, pdf_files):
    txt_files = []

    for file in pdf_files:
        convert_pdf_to_text(directory, file)
        txt_files.append(f'{file.split(".")[0]}.txt')

    return txt_files


def search(directory, txt_files, text):
    for file in txt_files:
        result = search_text(directory, file, text)

        if result == "":
            print("Texto não encontrado em nenhum dos arquivos")
            return

        print(f'Arquivo: {file.split(".")[0]}\nEncontrado no(s) trecho(s):\n{result}')


def delete_txt_files(directory, txt_files):
    for file in txt_files:
        delete_file(directory, file)


def main():
    args = get_args()

    directory = args.directory
    text = args.text

    # 1 Get all pdf files
    pdf_files = find_all_pdfs(directory)

    # 2 Use the "pdftotext" lib to convert all pdfs in txts
    txt_files = convert(directory, pdf_files)

    # 3 Use cat and grep commands to search the text
    search(directory, txt_files, text)

    # 4 Delete all txt files generated by 2 step
    delete_txt_files(directory, txt_files)


if __name__ == "__main__":
    main()