import PySimpleGUI as sg
from nasa_api_call import get_photos
from os_project_download_image_and_png_conversion import download_and_convert_to_png


sg.theme("DarkGrey3")

def window_1():

	# GUI as 2d list 

	layout = [[sg.Text("Enter Date to find image (in yyyy-mm-dd format): "), sg.InputText()],
	[sg.Ok(), sg.Cancel()]]

	# create special class window and implement it 

	window = sg.Window("Today in Mars", layout)

	# event loop to process events

	while True:
		event, values = window.read()
		if event in (sg.WIN_CLOSED, "Cancel"):
			window.close()
			break
		
		elif any(values.values()) is False:
			window.close()
			error_window()

		window.close()
		for i in values.values():
			window_2(i)
		
def error_window():

	layout = [[sg.Text("Please enter valid input")], 
	[sg.Ok()]]
	window = sg.Window("Today in Mars", layout)

	event, values = window.read()
	window.close()
	window_1()

def date_checker(given_date):

	if("-" not in given_date):
		return False
	else:
		checking = given_date.split("-")
		if(len(checking) != 3):
			return False
		else:
			if (len(checking[0]) != 4) or (len(checking[1]) != 2) or (len(checking[2]) != 2):
				return False
			else:
				if (int(checking[0]) > 2023 or int(checking[1]) > 12) or (int(checking[2]) > 31):
					return False
				else:
					return True

def window_2(given_date):

	camera_list = ["FHAZ", "NAVCAM", "MAST", "CHEMCAM", "MAHLI", "MARDI", "RHAZ"]
	camera_description = ["Front Hazard Avoidance Camera takes black-and-white images ensuring safe rover movement by assessing terrain hazards.", "Navigation Camera aids in rover navigation and obstacle avoidance with wide-angle views.", "Mast Cameras takes high-resolution color images revealing Mars' geological features and landscapes.", "Chemistry and Camera Complex analyzes Martian rocks' composition using laser-induced breakdown spectroscopy for discoveries.", "Mars Hand Lens Imager captures close-up images, aiding detailed examination of Martian rocks and soil.", "Mars Descent Imager captures descent images for studying Martian landing sites.", "Rear Hazard Avoidance Camera monitors terrain beneath rover for safe navigation."]
	if(date_checker(given_date)):
		photos_taken = get_photos(given_date)
		given_date_cameras_list = list(photos_taken[0].keys())

		layout = [[sg.Text("Curiosity Rover images")], 
		[sg.Text("Given Date:"), sg.Text(given_date)],
		[sg.Text("Select from listed cameras that have clicked pictures on this date")]]
		camera_number = 1
		for j in given_date_cameras_list:
			if j in camera_list:
				given_date_photos_list = (photos_taken[1][j])
				no_of_photos = len(given_date_photos_list)
				layout.append([sg.Text("Camera "), sg.Text(camera_number), sg.Text(": "), sg.Button(j), sg.Text("Total photos taken = "), sg.Text(no_of_photos)])
				k = camera_list.index(j)
				layout.append([sg.Text(camera_description[k])])
				camera_number += 1
			else:
				continue
		count = 0
		layout.append([sg.Button("Go back")])

		window = sg.Window("Today in Mars", layout)

		while True:
			event, values = window.read()
			if event == "Go back":
				window.close()
				window_1()
			elif event in camera_list:
				window.close()
				window_3(given_date, event, count)
			elif event == sg.WIN_CLOSED:
				window.close()
				break
	else:
		print("Sorry your date is in wrong format please start again")



def window_3(given_date, camera, count):

	photos_taken = get_photos(given_date)
	given_date_photos_list = (photos_taken[1][camera])

	layout = [
	[sg.Text("Here's the image captured by the selected camera:"), sg.Text(camera)],
	[sg.Text("\n")]]

	layout.append([sg.Button("Previous"), sg.Button("Next")])
	layout.append([sg.Button("Go back"), sg.Button("Cancel")])	
	layout.append([sg.Text("\n")])
	image_png_with_local_path = download_and_convert_to_png(given_date_photos_list[count])
	layout.append([sg.Image(image_png_with_local_path, expand_x=True, expand_y=True)])
	length = len(given_date_photos_list)

	window = sg.Window("Today in Mars", layout, size=(715,350))

	while True:
		event, value = window.read()
		if event in (sg.WIN_CLOSED, "Cancel"):
			window.close()
			break
		elif event == "Go back":
			window.close()
			window_2(given_date)
		elif event == "Next":
			window.close()
			if(count<(length-1)):
				count += 1
				print(f"Showing image {count+1} of {length}")
				window_3(given_date, camera, count)
			else:
				sg.popup("You have reached the end of today's photos.", title = "Today in Mars")
				window_3(given_date, camera, count)
		elif event == "Previous":
			window.close()
			if(count>0):
				count -= 1
				print(f"Showing image {count+1} of {length}")
				window_3(given_date, camera, count)
			else:
				sg.popup("You have reached the start of today's photos.", title = "Today in Mars")
				window_3(given_date, camera, count)

window_1()