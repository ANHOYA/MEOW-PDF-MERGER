import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox


def merge_pdfs(odd_pdf_path, even_pdf_path, output_pdf_path):
    try:
        odd_pdf = open(odd_pdf_path, 'rb')
        even_pdf = open(even_pdf_path, 'rb')

        odd_reader = PyPDF2.PdfReader(odd_pdf)
        even_reader = PyPDF2.PdfReader(even_pdf)

        pdf_writer = PyPDF2.PdfWriter()
        total_pages = len(odd_reader.pages)

        if len(even_reader.pages) != total_pages:
            messagebox.showerror("Error", "PDF 파일의 페이지 수가 일치하지 않습니다.")
            return

        for i in range(total_pages):
            pdf_writer.add_page(odd_reader.pages[i])
            even_page = even_reader.pages[total_pages - i - 1]
            pdf_writer.add_page(even_page)

        with open(output_pdf_path, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)

        odd_pdf.close()
        even_pdf.close()

        messagebox.showinfo("성공", f"PDF 파일이 성공적으로 병합되었습니다.\n저장 위치: {output_pdf_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def select_files():
    odd_pdf_path = filedialog.askopenfilename(title="홀수 페이지 PDF 선택", filetypes=[("PDF files", "*.pdf")])
    even_pdf_path = filedialog.askopenfilename(title="짝수 페이지 PDF 선택", filetypes=[("PDF files", "*.pdf")])

    if not odd_pdf_path or not even_pdf_path:
        messagebox.showerror("Error", "두 개의 PDF 파일을 선택해야 합니다.")
        return

    output_pdf_path = filedialog.asksaveasfilename(title="병합된 PDF 저장", defaultextension=".pdf",
                                                   filetypes=[("PDF files", "*.pdf")])

    if output_pdf_path:
        merge_pdfs(odd_pdf_path, even_pdf_path, output_pdf_path)


# Tkinter 기본 창 구성
root = tk.Tk()
root.title("PDF 병합 도구")

# 창 크기 조정
root.geometry("300x150")

# 안내 텍스트
label = tk.Label(root, text="PDF 파일을 병합하려면 버튼을 클릭하세요.")
label.pack(pady=20)

# 파일 선택 버튼
button = tk.Button(root, text="PDF 파일 선택", command=select_files)
button.pack(pady=10)

# Tkinter 창 실행
root.mainloop()
