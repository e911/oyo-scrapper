import os, sys, time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from operator import itemgetter

# os.environ['MOZ_HEADLESS'] = '1'
# binary = FirefoxBinary('/usr/bin/firefox', log_file=sys.stdout)

# two = sys.argv[1]
def clean_data(data):
	try:
		return data[0].text
	except IndexError:
		return 0


def parser_oyo(driver):
	# driver = webdriver.Firefox(firefox_binary=binary)
	# driver.get("https://www.oyorooms.com/oyos-in-kathmandu")

	time.sleep(5)

	# hotels = driver.find_elements_by_class_name("newHotelCard")
	# for hotel in hotels:
	#     price = hotel.find_elements_by_class_name("newHotelCard__pricing")
	#     print(price[0].text)
	hotels_data = []

	hotels_list = driver.find_elements_by_class_name("newHotelCard")
	for hotels in hotels_list:
		hotel_name = hotels.find_elements_by_class_name("newHotelCard__hotelName")
		hotel_location =  hotels.find_elements_by_class_name("newHotelCard__hotelAddress")

		hotel_price_detail = hotels.find_elements_by_class_name("newHotelCard__pricing")
		price = hotel_price_detail[0].text
		hotel_price =  int(price.split(" ")[1])


		hotel_not_discounted_amount = hotels.find_elements_by_class_name("newHotelCard__revisedPricing")
		hotel_discount_percentage = hotels.find_elements_by_class_name("newHotelCard__discount")
		hotel_rating = hotels.find_elements_by_class_name("hotelRating__value")
		hotel_rating_remarks = hotels.find_elements_by_class_name("hotelRating__subtext")

		# try:
		# 	disc_price = hotel_discounted_amount[0].text
		# except IndexError:
		# 	disc_price = 0

		# try:
		# 	disc_perc = hotel_discount_percentage[0].text
		# except IndexError:
		# 	disc_perc = 0

		# try:
		# 	rating = hotel_rating[0].text
		# except IndexError:
		# 	rating = 0

		# try:
		# 	remarks = hotel_rating_remarks[0].text
		# except IndexError:
		# 	remarks = None

		original_price = clean_data(hotel_not_discounted_amount)
		disc_perc = clean_data(hotel_discount_percentage)
		rating = clean_data(hotel_rating)
		remarks = clean_data(hotel_rating_remarks)

		data = {
			"Name": hotel_name[0].text,
			"Location": hotel_location[0].text,
			"Price after Disc": hotel_price,
			"Original Price": original_price,
			"Disc Percentage": disc_perc,
			"Rating": rating,
			"Remarks": remarks
			}
		print(data)
		hotels_data.append(data)
	# print(hotels_data)
	# del os.environ['MOZ_HEADLESS'] 
	return hotels_data

def write_data_to_csv(parsed_data, csv_columns, csv_file):
	try:
		with open(csv_file, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
			writer.writeheader()
			for data in parsed_data:
				writer.writerow(data)
	except IOError:
		print("I/O error") 



if __name__ == '__main__':
	url = "https://www.oyorooms.com/oyos-in-kathmandu"
	driver = webdriver.Chrome()
	driver.get(url)
	parsed_data = parser_oyo(driver)

	#get next pages data
	try:
		nextpageButton = driver.find_elements_by_class_name("btn-next")[0]
		while(nextpageButton != []):
			next_page = nextpageButton.click()
			next_page_data = parser_oyo(driver)
			parsed_data += next_page_data
			nextpageButton = driver.find_elements_by_class_name("btn-next")[0]
	except IndexError:
		pass

	driver.close()

	csv_columns = ['Name','Location','Price after Disc', 'Original Price', 'Disc Percentage', 'Rating', 'Remarks']
	csv_file = "Hotels List.csv"
	write_data_to_csv(parsed_data, csv_columns, csv_file)

	# try:
	# 	with open(csv_file, 'w') as csvfile:
	# 		writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
	# 		writer.writeheader()
	# 		for data in parsed_data:
	# 			writer.writerow(data)
	# except IOError:
	# 	print("I/O error") 

	data_sorted_by_price = sorted(parsed_data, key=itemgetter('Price after Disc'))
	sorted_csv_file = "Hotel List sorted by price.csv"
	write_data_to_csv(data_sorted_by_price, csv_columns, sorted_csv_file)

	# 	try:
	# 	with open(csv_file, 'w') as csvfile:
	# 		writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
	# 		writer.writeheader()
	# 		for data in data_sorted_by_price:
	# 			writer.writerow(data)
	# except IOError:
	# 	print("I/O error") 


