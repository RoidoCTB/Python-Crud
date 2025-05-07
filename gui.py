import tkinter as tk
from tkinter import messagebox
import requests

# Set up your Flask API URL
API_URL = 'http://127.0.0.1:5000/api/students'

# Initialize the main window
root = tk.Tk()
root.title("Student Management")
root.geometry("600x450")

# Function to fetch students from the API
def fetch_students():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            students = response.json()
            listbox.delete(0, tk.END)
            for student in students:
                listbox.insert(tk.END, f"{student['id']} - {student['fname']} - {student['email']}")
        else:
            messagebox.showerror("Error", "Failed to fetch students.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Network Error", f"An error occurred: {e}")

# Function to view student details
def view_student():
    selected_student = listbox.curselection()
    if selected_student:
        student_id = listbox.get(selected_student[0]).split(" - ")[0]
        try:
            response = requests.get(f"{API_URL}/{student_id}")
            if response.status_code == 200:
                student = response.json()
                details = f"Name: {student['fname']}\nEmail: {student['email']}\nGender: {student['gender']}\nBirthdate: {student['bdate']}"
                messagebox.showinfo("Student Details", details)
            else:
                messagebox.showerror("Error", "Student not found!")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Selection Error", "Please select a student to view.")

# Function to delete student
def delete_student():
    selected_student = listbox.curselection()
    if selected_student:
        student_id = listbox.get(selected_student[0]).split(" - ")[0]
        confirmation = messagebox.askyesno("Delete", "Are you sure you want to delete this student?")
        if confirmation:
            try:
                response = requests.delete(f"{API_URL}/{student_id}")
                if response.status_code == 200:
                    fetch_students()
                    messagebox.showinfo("Success", "Student deleted successfully.")
                else:
                    messagebox.showerror("Error", "Failed to delete student.")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Network Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Selection Error", "Please select a student to delete.")

# Function to add student
def add_student():
    def save_student():
        fname = fname_entry.get()
        email = email_entry.get()
        gender = gender_var.get()
        bdate = bdate_entry.get()

        if not fname or not email or not gender or not bdate:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        student_data = {
            'fname': fname,
            'email': email,
            'gender': gender,
            'bdate': bdate
        }
        try:
            response = requests.post(API_URL, json=student_data)
            if response.status_code == 200:
                messagebox.showinfo("Success", "Student added successfully!")
                add_window.destroy()
                fetch_students()
            else:
                messagebox.showerror("Error", "Failed to add student.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"An error occurred: {e}")

    add_window = tk.Toplevel(root)
    add_window.title("Add Student")
    add_window.geometry("300x250")

    tk.Label(add_window, text="Name:").pack()
    fname_entry = tk.Entry(add_window)
    fname_entry.pack()

    tk.Label(add_window, text="Email:").pack()
    email_entry = tk.Entry(add_window)
    email_entry.pack()

    tk.Label(add_window, text="Gender:").pack()
    gender_var = tk.StringVar()
    tk.Radiobutton(add_window, text="Male", variable=gender_var, value="Male").pack()
    tk.Radiobutton(add_window, text="Female", variable=gender_var, value="Female").pack()

    tk.Label(add_window, text="Birthdate (YYYY-MM-DD):").pack()
    bdate_entry = tk.Entry(add_window)
    bdate_entry.pack()

    tk.Button(add_window, text="Save", command=save_student).pack()

# Function to edit student
def edit_student():
    selected_student = listbox.curselection()
    if selected_student:
        student_id = listbox.get(selected_student[0]).split(" - ")[0]
        try:
            response = requests.get(f"{API_URL}/{student_id}")
            if response.status_code == 200:
                student = response.json()

                edit_window = tk.Toplevel(root)
                edit_window.title("Edit Student")
                edit_window.geometry("300x250")

                tk.Label(edit_window, text="Name:").pack()
                fname_entry = tk.Entry(edit_window)
                fname_entry.insert(0, student['fname'])
                fname_entry.pack()

                tk.Label(edit_window, text="Email:").pack()
                email_entry = tk.Entry(edit_window)
                email_entry.insert(0, student['email'])
                email_entry.pack()

                tk.Label(edit_window, text="Gender:").pack()
                gender_var = tk.StringVar(value=student['gender'])
                tk.Radiobutton(edit_window, text="Male", variable=gender_var, value="Male").pack()
                tk.Radiobutton(edit_window, text="Female", variable=gender_var, value="Female").pack()

                tk.Label(edit_window, text="Birthdate (YYYY-MM-DD):").pack()
                bdate_entry = tk.Entry(edit_window)
                bdate_entry.insert(0, student['bdate'])
                bdate_entry.pack()

                def save_changes():
                    updated_data = {
                        'fname': fname_entry.get(),
                        'email': email_entry.get(),
                        'gender': gender_var.get(),
                        'bdate': bdate_entry.get()
                    }
                    try:
                        put_response = requests.put(f"{API_URL}/{student_id}", json=updated_data)
                        if put_response.status_code == 200:
                            messagebox.showinfo("Success", "Student updated successfully!")
                            edit_window.destroy()
                            fetch_students()
                        else:
                            messagebox.showerror("Error", "Failed to update student.")
                    except requests.exceptions.RequestException as e:
                        messagebox.showerror("Network Error", f"An error occurred: {e}")

                tk.Button(edit_window, text="Save Changes", command=save_changes).pack()
            else:
                messagebox.showerror("Error", "Failed to fetch student data.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Selection Error", "Please select a student to edit.")

# UI Setup
listbox = tk.Listbox(root, width=60, height=15)
listbox.pack(pady=10)

#btn_frame = tk.Frame(root)
#btn_frame.pack()

#view_btn = tk.Button(btn_frame, text="View Student", width=20, command=view_student)
#view_btn.grid(row=0, column=0, padx=5)

#delete_btn = tk.Button(btn_frame, text="Delete Student", width=20, command=delete_student)
#delete_btn.grid(row=0, column=1, padx=5)

#add_btn = tk.Button(btn_frame, text="Add Student", width=20, command=add_student)
#add_btn.grid(row=0, column=2, padx=5)

#edit_btn = tk.Button(btn_frame, text="Edit Student", width=20, command=edit_student)
#edit_btn.grid(row=1, column=1, pady=10)

# Updated Menu Setup
# Menu Setup
menu_bar = tk.Menu(root)
student_menu = tk.Menu(menu_bar, tearoff=0)

student_menu.add_command(label="Add Student", command=add_student)
student_menu.add_command(label="View Student", command=view_student) 
student_menu.add_command(label="Edit Student", command=edit_student)
student_menu.add_command(label="Delete Student", command=delete_student)
student_menu.add_separator()
student_menu.add_command(label="Exit", command=root.quit)

menu_bar.add_cascade(label="Manage Students", menu=student_menu)
root.config(menu=menu_bar)



# Initial fetch
fetch_students()

# Run the GUI loop
root.mainloop()










