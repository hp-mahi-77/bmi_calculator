import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import io
import datetime

# --- Functions ---
def calculate_bmi():
    try:
        feet = int(entry_feet.get())
        inches = int(entry_inches.get())
        weight = float(entry_weight.get())
        total_inches = feet * 12 + inches
        height_m = total_inches * 0.0254

        bmi = weight / (height_m ** 2)
        label_result.config(text=f"Your BMI is: {bmi:.2f}", font=("Arial", 12, "bold"))

        category, tip = get_bmi_category_and_tip(bmi)
        label_category.config(text=f"Category: {category}", font=("Arial", 12, "bold"))
        label_tips.config(text=f"Health Tip: {tip}", font=("Arial", 11, "italic"), wraplength=450, fg='darkblue')

        plot_bmi_chart(bmi)
        frame_chart.pack(pady=10)
        save_data(feet, inches, weight, bmi, category, tip)

    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numeric values for height and weight.")


def get_bmi_category_and_tip(bmi):
    if bmi < 18.5:
        return "Underweight", "Include nutrient-rich foods and eat more frequently."
    elif 18.5 <= bmi < 25:
        return "Normal", "Keep up the good work with a balanced diet and regular exercise."
    elif 25 <= bmi < 30:
        return "Overweight", "Consider portion control and increase physical activity."
    else:
        return "Obese", "Consult a healthcare provider and adopt a healthier lifestyle."


def plot_bmi_chart(bmi):
    categories = ['Underweight', 'Normal', 'Overweight', 'Obese']
    limits = [18.5, 25, 30, 40]
    colors = ['skyblue', 'green', 'orange', 'red']

    fig, ax = plt.subplots(figsize=(9, 2.5))
    fig.tight_layout()

    start = 10
    for i, limit in enumerate(limits):
        ax.barh(0, limit - start, left=start, color=colors[i], height=0.5)
        ax.text(start + (limit - start)/2, 0.1, categories[i], ha='center', fontsize=10, weight='bold')
        start = limit

    ax.axvline(bmi, color='black', linewidth=2, label=f'Your BMI: {bmi:.1f}')
    ax.set_yticks([])
    ax.set_xlim(10, 40)
    ax.set_xlabel("BMI Range")
    ax.set_title("BMI Classification Chart")
    ax.legend(loc='upper right')

    for widget in frame_chart.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=frame_chart)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Save chart to buffer for export
    global chart_buffer
    chart_buffer = io.BytesIO()
    fig.savefig(chart_buffer, format='png')
    chart_buffer.seek(0)


def save_data(feet, inches, weight, bmi, category, tip):
    with open("bmi_report.txt", "w") as file:
        file.write(f"BMI Report ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
        file.write(f"Height: {feet} feet {inches} inches\n")
        file.write(f"Weight: {weight} kg\n")
        file.write(f"BMI: {bmi:.2f}\n")
        file.write(f"Category: {category}\n")
        file.write(f"Tip: {tip}\n")

    if chart_buffer:
        with open("bmi_chart.png", "wb") as f:
            f.write(chart_buffer.getvalue())
        messagebox.showinfo("Export", "Report and chart saved successfully!")

# --- GUI ---
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("700x720")
root.resizable(False, False)

# Background image
bg_image = Image.open("C:Users/admin/Downloads/redd-francisco-8LWo8v0mKik-unsplash.jpg")  # ensure this file is present
bg_image = bg_image.resize((700, 720), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

frame_input = tk.Frame(root, bg="#f0f0f0", bd=2)
frame_input.pack(pady=20)

label_title = tk.Label(frame_input, text="BMI Calculator", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
label_title.grid(row=0, columnspan=2, pady=10)

label_feet = tk.Label(frame_input, text="Height (feet):", bg="#f0f0f0")
label_feet.grid(row=1, column=0, sticky='e', padx=5, pady=5)
entry_feet = tk.Entry(frame_input)
entry_feet.grid(row=1, column=1, padx=5)

label_inches = tk.Label(frame_input, text="Height (inches):", bg="#f0f0f0")
label_inches.grid(row=2, column=0, sticky='e', padx=5, pady=5)
entry_inches = tk.Entry(frame_input)
entry_inches.grid(row=2, column=1, padx=5)

label_weight = tk.Label(frame_input, text="Weight (kg):", bg="#f0f0f0")
label_weight.grid(row=3, column=0, sticky='e', padx=5, pady=5)
entry_weight = tk.Entry(frame_input)
entry_weight.grid(row=3, column=1, padx=5)

btn_calculate = tk.Button(frame_input, text="Calculate BMI", command=calculate_bmi, bg="#007ACC", fg="white", font=("Arial", 11, "bold"))
btn_calculate.grid(row=4, columnspan=2, pady=10)

label_result = tk.Label(root, text="", bg="#e0f7fa")
label_result.pack()

label_category = tk.Label(root, text="", bg="#e0f7fa")
label_category.pack()

label_tips = tk.Label(root, text="", bg="#f9fbe7", wraplength=450, font=("Arial", 11))
label_tips.pack(pady=5)

frame_chart = tk.Frame(root, bg="#ffffff")
frame_chart.pack_forget()  # Hide initially

chart_buffer = None
root.mainloop()
