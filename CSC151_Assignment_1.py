from tkinter import *
import tkinter.messagebox
import pandas
import csv
from tkinter import ttk
from tempfile import NamedTemporaryFile
import shutil


def get_initials():
	name = Full_name.get()
	id_num = ID_number.get()
	course_year = Course_Level.get()
	ab = False

	with open('records.txt' , 'r') as read_csv_file:
		reader = csv.reader(read_csv_file, delimiter = ',')
		for row in reader:
			if name == row[0] and id_num == row[1]:
				ab = True

	if ab is True:
		tkinter.messagebox.showerror("Account already exists!", "You have registered an existing account")
		
		entry_name.delete(0, END)
		entry_course.delete(0, END)
		entry_id_num.delete(0, END)

	else:
		registrant = [name, id_num, course_year]
		with open(r"records.txt" , 'a', newline = '') as csv_file:
			csv_writer = csv.writer(csv_file, delimiter = ',')

			#csv_writer.writeheader()
			csv_writer.writerow(registrant)

		tkinter.messagebox.showinfo("Registration Success!", "You have registered successfully")

		window_reg.destroy()


def del_info():
	d_name = del_name.get()
	d_num = del_ID_num.get()
	d_cl = del_course_level.get()
	line = list()
	with open("records.txt" ,'r') as csv_file:	
		csv_reader = csv.reader(csv_file, delimiter = ',')
		for row in csv_reader:
			line.append(row)
			for field in row:
				if field == d_name:
					line.remove(row)
	with open('records.txt' , 'w', newline = '') as new_csv_file:
		writer = csv.writer(new_csv_file, delimiter = ',')
		writer.writerows(line)

	del_entry_name.delete(0, END)
	del_entry_id_num.delete(0, END)
	del_entry_course.delete(0, END)

	tkinter.messagebox.showinfo("Delete!", "You have deleted the value in the record")

	window_del.destroy()


def updater():
	ad = False
	upd_name = up_up_name.get()
	upd_id = up_ID_num.get()
	upd_course_level = up_course_level.get()

	filename = 'records.txt'
	tempfile = NamedTemporaryFile(mode = 'a', newline = '', delete = False)

	with open(filename,'r') as read_csv_file:
		reader_file = csv.reader(read_csv_file)
		for red in reader_file:
			if upd_name == red[0] or upd_id == red[1]:
				ad = True

	if ad is True:
		tkinter.messagebox.showerror("Error!", "Account already exists")

		up_entry_name.delete(0, END)
		up_entry_id_num.delete(0, END)
		up_entry_course.delete(0, END)	

	else:
		with open(filename, 'r') as csv_file, tempfile:
			reader = csv.reader(csv_file)
			writer = csv.writer(tempfile)
			for row in reader:
				print(row)
				print(row[1])
				if to_id == row[1]:
					row[0], row[1], row[2] = upd_name, upd_id, upd_course_level
				res = [row[0], row[1], row[2]]
				# 	row['Name'], row['ID'], row['Course'] = upp_name, upp_id, upp_course_level
				# rese = {'Name' : row['Name'], 'ID' : row['ID'], 'Course' : row['Course']}
				writer.writerow(res)

		tkinter.messagebox.showinfo("Success!", "You have updated the students record")

		shutil.move(tempfile.name, filename)

	window_update.destroy()

	
def shower():
	with open('records.txt' , 'r') as csv_file:
		reader = csv.reader(csv_file)
		data = [row for row in reader]

	print(list(enumerate(data, start = 1)))
	for i, (name, id_number, course_level) in enumerate(data, start = 1):
		listBox.insert("", "end", values = (i, name, id_number, course_level))

	csv_file.close()


def showAll():
	global listBox
	show_all = Toplevel(window)
	label = Label(show_all, text = "CRUD App Table" , font = ("Arial, 30")).grid(row = 0, columnspan = 4)
	cols = ('' , 'Name', 'ID Number', 'Course/Level')
	listBox = ttk.Treeview(show_all, column = cols, show = 'headings')

	for col in cols:
		listBox.heading(col, text = col)
	listBox.grid(row = 1, column = 0, columnspan = 2)

	shower()

	show = Button(show_all, text = "Show list", width = 15, state = DISABLED, command = shower).grid(row = 4, column = 0)
	searches = Button(show_all, text = "Search", width = 15, command = search).grid(row = 4, column = 1)
	deletes = Button(show_all, text = "Delete", width = 15, command = delete).grid(row = 5, column = 0)
	close = Button(show_all, text = "Close", width = 15, command = show_all.destroy).grid(row = 5, column = 1)


def searcher():
	var = StringVar()
	searched = search_id_num.get()
	new_search_win = Toplevel(window)
	new_search_win.geometry("400x200")

	file = csv.reader(open('records.txt', 'r'), delimiter = ',')
	sett = False
	global result
	for row in file:
		if searched == row[1]:
			result = row
			sett = True

	if sett is False:
		tkinter.messagebox.showinfo("Error!", "No record...")
		new_search_win.destroy()
	else:	
		string_result = 'Name: '+ str(result[0]) + 'ID_number: ' + str(result[1]) + 'Course: ' + str(result[2])
		var.set(string_result)
	# print('Name:',result[0],'ID_number:',result[1],'Course:',result[2])

	lbl = Label(new_search_win, text = "Searched", width = 20, relief = "solid", font = ("arial", 19, "bold"))
	lbl.place(x = 45, y = 53)

	sea_lbl_name = Label(new_search_win, textvariable = var, width = 36, font = ("arial", 10, "bold"))
	sea_lbl_name.place(x = 43, y = 120)

	sea_b_close = Button(new_search_win, text = "Close", width = 12, bg = 'brown', fg = 'white', command = new_search_win.destroy)
	sea_b_close.place(x = 150, y = 150)

	window_search.destroy()
	

def search():
	global search_id_num
	global window_search
	search_id_num = StringVar()

	window_search = Toplevel(window)
	window_search.title("Search via ID Number")
	window_search.geometry("400x500")

	lbl = Label(window_search, text = "Search", width = 20, relief = "solid", font = ("arial", 19, "bold"))
	lbl.place(x = 45, y = 53)

	se_lbl_name = Label(window_search, text = "ID Number:", width = 12, font = ("arial", 10, "bold"))
	se_lbl_name.place(x = 43, y = 120)
	se_entry_name = Entry(window_search, textvar = search_id_num)
	se_entry_name.place(x = 220, y = 120)

	se_b_submit = Button(window_search, text = "Search", width = 12, bg = 'brown', fg = 'white', command = searcher)
	se_b_submit.place(x = 100, y = 230)

	se_b_cancel = Button(window_search, text = "Cancel", width = 12, bg = 'brown', fg = 'white', command = window_search.destroy)
	se_b_cancel.place(x = 220, y = 230)


def update():
	global window_update
	global up_ID_num
	global up_course_level
	global up_entry_name
	global up_entry_id_num
	global up_entry_course
	global up_up_name

	up_up_name = StringVar()
	up_ID_num = StringVar()
	up_course_level = StringVar()

	window_update = Toplevel(window)
	window_update.title("Update")
	window_update.geometry("400x500")

	lbl = Label(window_update, text = "Update user", width = 20, relief = "solid", font = ("arial", 19, "bold"))
	lbl.place(x = 45, y = 53)

	up_lbl_name = Label(window_update, text = "Full Name:", width = 12, font = ("arial", 10, "bold"))
	up_lbl_name.place(x = 43, y = 120)
	up_entry_name = Entry(window_update, textvar = up_up_name)
	up_entry_name.place(x = 220, y = 120)

	up_lbl_id_num = Label(window_update, text = "Identification Number:", width = 18,  font = ("arial", 10, "bold"))
	up_lbl_id_num.place(x = 55, y = 150)
	up_entry_id_num = Entry(window_update, textvar = up_ID_num)
	up_entry_id_num.place(x = 220, y = 150)


	up_lbl_course = Label(window_update, text = "Course and Year:", width = 15, font = ("arial", 10, "bold"))
	up_lbl_course.place(x = 52, y = 180)
	up_entry_course = Entry(window_update, textvar = up_course_level)
	up_entry_course.place(x = 220, y = 180)

	up_b_submit = Button(window_update, text = "Update", width = 12, bg = 'brown', fg = 'white', command = updater)
	up_b_submit.place(x = 100, y = 230)

	up_b_cancel = Button(window_update, text = "Cancel", width = 12, bg = 'brown', fg = 'white', command = window_update.destroy)
	up_b_cancel.place(x = 220, y = 230)

	to_window_update.destroy()

def to_confirm():
	global to_id	
	to_id = to_up_id.get()
	with open('records.txt' , 'r') as csv_file:
		ad = False
		reader = csv.reader(csv_file, delimiter = ',')

		for row in reader:
			if to_id == row[1]:
				ad = True
	if ad is False:
		tkinter.messagebox.showerror("Error!", "No record")
		to_window_update.destroy()
	else:
		update()

	to_window_update.destroy()


def to_update():
	global to_window_update
	global to_up_id
	
	to_up_id = StringVar()
	
	to_window_update = Toplevel(window)
	to_window_update.title("Update")
	to_window_update.geometry("400x500")

	lbl = Label(to_window_update, text = "Update user", width = 20, relief = "solid", font = ("arial", 19, "bold"))
	lbl.place(x = 45, y = 53)

	to_lbl_name = Label(to_window_update, text = "ID Number:", width = 12, font = ("arial", 10, "bold"))
	to_lbl_name.place(x = 43, y = 120)
	to_entry_name = Entry(to_window_update, textvar = to_up_id)
	to_entry_name.place(x = 220, y = 120)

	to_b_submit = Button(to_window_update, text = "Update", width = 12, bg = 'brown', fg = 'white', command = to_confirm)
	to_b_submit.place(x = 100, y = 230)

	to_b_cancel = Button(to_window_update, text = "Cancel", width = 12, bg = 'brown', fg = 'white', command = to_window_update.destroy)
	to_b_cancel.place(x = 220, y = 230)



def delete():
	global window_del
	global del_name
	global del_ID_num
	global del_course_level
	global del_entry_name
	global del_entry_id_num
	global del_entry_course

	del_name = StringVar()
	del_ID_num = StringVar()
	del_course_level = StringVar()

	window_del = Toplevel(window)
	window_del.title("Delete")
	window_del.geometry("400x500")

	lbl = Label(window_del, text = "Delete", width = 20, relief = "solid", font = ("arial", 19, "bold"))
	lbl.place(x = 45, y = 53)

	del_lbl_name = Label(window_del, text = "Full Name:", width = 12, font = ("arial", 10, "bold"))
	del_lbl_name.place(x = 43, y = 120)
	del_entry_name = Entry(window_del, textvar = del_name)
	del_entry_name.place(x = 220, y = 120)

	del_lbl_id_num = Label(window_del, text = "Identification Number:", width = 18,  font = ("arial", 10, "bold"))
	del_lbl_id_num.place(x = 55, y = 150)
	del_entry_id_num = Entry(window_del, textvar = del_ID_num)
	del_entry_id_num.place(x = 220, y = 150)


	del_lbl_course = Label(window_del, text = "Course and Year:", width = 15, font = ("arial", 10, "bold"))
	del_lbl_course.place(x = 52, y = 180)
	del_entry_course = Entry(window_del, textvar = del_course_level)
	del_entry_course.place(x = 220, y = 180)

	del_b_submit = Button(window_del, text = "Delete", width = 12, bg = 'brown', fg = 'white', command = del_info)
	del_b_submit.place(x = 100, y = 230)

	del_b_cancel = Button(window_del, text = "Cancel", width = 12, bg = 'brown', fg = 'white', command = window_del.destroy)
	del_b_cancel.place(x = 220, y = 230)


def register():
	global entry_name
	global entry_course
	global entry_id_num
	global window_reg
	global Full_name
	global ID_number
	global Course_Level

	Full_name = StringVar()
	ID_number = StringVar()
	Course_Level = StringVar()

	window_reg = Toplevel(window)
	window_reg.title("Registration")
	window_reg.geometry("400x500")


	lbl = Label(window_reg, text = "Registration Form", width = 20, relief = "solid", font = ("arial", 19, "bold"))
	lbl.place(x = 45, y = 53)

	lbl_name = Label(window_reg, text = "Full Name:", width = 12, font = ("arial", 10, "bold"))
	lbl_name.place(x = 43, y = 120)
	entry_name = Entry(window_reg, textvar = Full_name)
	entry_name.place(x = 220, y = 120)

	lbl_id_num = Label(window_reg, text = "Identification Number:", width = 18,  font = ("arial", 10, "bold"))
	lbl_id_num.place(x = 55, y = 150)
	entry_id_num = Entry(window_reg, textvar = ID_number)
	entry_id_num.place(x = 220, y = 150)


	lbl_course = Label(window_reg, text = "Course and Year:", width = 15, font = ("arial", 10, "bold"))
	lbl_course.place(x = 52, y = 180)
	entry_course = Entry(window_reg, textvar = Course_Level)
	entry_course.place(x = 220, y = 180)

	b_submit = Button(window_reg, text = "Submit", width = 12, bg = 'brown', fg = 'white', command = get_initials)
	b_submit.place(x = 100, y = 230)

	b_cancel = Button(window_reg, text = "Cancel", width = 12, bg = 'brown', fg = 'white', command = window_reg.destroy)
	b_cancel.place(x = 220, y = 230)

def main():
	global window
	window = Tk()
	window.title("CRUD Application")
	window.geometry("400x500")

	lbl = Label(window, text = "This is a CRUD app", width = 20, relief = "solid", font = ("arial", 19, "bold"))
	lbl.place(x = 45, y = 53)

	b_regis = Button(window, text = "Register", width = 12, bg = 'brown', fg = 'white', command = register)
	b_regis.place(x = 145, y = 115)

	b_print = Button(window, text = "Show", width = 12, bg = 'brown', fg = 'white', command = showAll)
	b_print.place(x = 145, y = 155)

	b_search = Button(window, text = "Search", width = 12, bg = 'brown', fg = 'white', command = search)
	b_search.place(x = 145, y = 195)

	b_delete = Button(window, text = "Delete", width = 12, bg = 'brown', fg = 'white', command = delete)
	b_delete.place(x = 145, y = 235)

	b_update = Button(window, text = "Update", width = 12, bg = 'brown', fg = 'white', command = to_update)
	b_update.place(x = 145, y = 235)

	b_exit = Button(window, text = "Exit", width = 12, bg = 'brown', fg = 'white', command = window.destroy)
	b_exit.place(x = 145, y = 275)


	window.mainloop()


main()