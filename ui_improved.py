import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox

# PDF 경로를 저장할 변수
odd_pdf_path = None
even_pdf_path = None


def merge_pdfs():
    if not odd_pdf_path or not even_pdf_path:
        messagebox.showerror("Error", "두 개의 PDF 파일을 모두 선택해야 합니다.")
        return

    output_pdf_path = filedialog.asksaveasfilename(title="병합된 PDF 저장", defaultextension=".pdf",
                                                   filetypes=[("PDF files", "*.pdf")])

    if output_pdf_path:
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


def select_odd_file():
    global odd_pdf_path
    odd_pdf_path = filedialog.askopenfilename(title="홀수 페이지 PDF 선택", filetypes=[("PDF files", "*.pdf")])
    if odd_pdf_path:
        odd_label.config(text=f"홀수 페이지: {odd_pdf_path}")


def select_even_file():
    global even_pdf_path
    even_pdf_path = filedialog.askopenfilename(title="짝수 페이지 PDF 선택", filetypes=[("PDF files", "*.pdf")])
    if even_pdf_path:
        even_label.config(text=f"짝수 페이지: {even_pdf_path}")


# Tkinter 기본 창 구성
root = tk.Tk()
root.title("MEOW PDF MERGER")
root.geometry("500x300")  # 창 크기 조정 가능
root.resizable(True, True)  # 창 크기 조절 가능

# 안내 텍스트
label = tk.Label(root, text="PDF 파일을 선택하고 병합하세요.")
label.pack(pady=10)

# 홀수 페이지 선택 버튼과 라벨
odd_button = tk.Button(root, text="홀수 페이지 PDF 선택", command=select_odd_file)
odd_button.pack(pady=5)

odd_label = tk.Label(root, text="홀수 페이지: 선택되지 않음", wraplength=400, justify="left")
odd_label.pack(pady=5)

# 짝수 페이지 선택 버튼과 라벨
even_button = tk.Button(root, text="짝수 페이지 PDF 선택", command=select_even_file)
even_button.pack(pady=5)

even_label = tk.Label(root, text="짝수 페이지: 선택되지 않음", wraplength=400, justify="left")
even_label.pack(pady=5)

# 병합 버튼
merge_button = tk.Button(root, text="PDF 병합", command=merge_pdfs)
merge_button.pack(pady=20)

# Tkinter 창 실행
root.mainloop()
