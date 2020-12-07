# Justin Suttles
#  Student ID: #001317337

import csv
import datetime
import sys

from PackageTable import PackageTable
from DistanceGraph import DistanceGraph
from Truck import Truck


def look_up_package_info(key):
    # Displays package information corresponding the key parameter.
    # Time Complexity: O(1)
    # Space Complexity: O(1)

    package = packages.search(key)

    print('Package ID: %d' % key)
    print('Address: %s' % package[0])
    print('City: %s' % package[1])
    print('State: %s' % package[2])
    print('Zip: %s' % package[3])
    print('Delivery Deadline: %s' % package[4])
    print('Mass(KILO): %s' % package[5])
    print('Special Notes: %s' % package[6])


def display_package_info(key):
    # Displays package information corresponding the key parameter and delivery status.
    # Time Complexity: O(1)
    # Space Complexity: O(1)

    package = packages.search(key)

    look_up_package_info(key)
    print('In route: %s' % package[8])
    print('Delivered: %s' % package[9])


def all_packages_info():
    # Prints information for all packages. Calls look_up_package_info function.
    # Time Complexity: O(N)
    # Space Complexity: O(1)

    for i in range(1, packages.size + 1):
        display_package_info(i)
        print()


def menu():
    # Displays the menu in command line interface.
    # Time Complexity: O(1)
    # Space Complexity: O(1)

    print()
    print('\t1 - Look Up Package Information')
    print('\t2 - Display Information and Status For All Packages')
    print('\t3 - Search Packages By Time')
    print('\t4 - Exit Program')
    print()


def load_truck_1():
    # This function loads the first truck for the first trip of the day. The function adds the packages to truck in the
    # following order:
    # - Parsing through the Special notes and adds packages that must be delivered it together
    # - Adds package that do not have a deadline of 'EOD'
    # - Adds packages that have the same address as packages listed above
    # - Removes packages that must be delivered on truck 2 and addresses that match
    # - Removes packages that will are delayed on flight and addresses that match
    # - Removes packages that have wrong addresses
    # Time Complexity: O(N^2)
    # Space Complexity: O(N)
    temp_list = []
    for i in range(1, packages.size + 1):
        j = packages.search(i)
        if "Must be delivered" in j[6]:
            temp_list.append(i)
            format_line = j[6].replace(',', '')
            for s in format_line.split():
                if s.isdigit():
                    temp_list.append(int(s))
    temp_list1 = list(set(temp_list))

    for i in range(1, packages.size + 1):
        j = packages.search(i)
        if j[4] != 'EOD' and j[6] == '':
            temp_list.append(int(i))
    temp_list1 = list(set(temp_list))

    for i in temp_list1:
        j = packages.search(i)
        temp_address = j[0]
        for x in range(1, packages.size + 1):
            y = packages.search(x)
            temp_address2 = y[0]
            if temp_address == temp_address2:
                temp_list.append(int(x))
    temp_list1 = list(set(temp_list))

    copy_list = temp_list1[:]

    for i in copy_list:
        j = packages.search(i)
        temp_address = j[0]
        for x in range(1, packages.size + 1):
            y = packages.search(x)
            temp_address2 = y[0]
            special_notes = y[6]
            if ("truck 2" in special_notes) and temp_address == temp_address2 and i in temp_list1:
                temp_list1.remove(i)
            if ("Delayed" in special_notes) and temp_address == temp_address2 and i in temp_list1:
                temp_list1.remove(i)

    copy_list = temp_list1[:]

    for i in copy_list:
        j = packages.search(i)
        if "Wrong address" in j[6]:
            temp_list1.remove(i)

    return temp_list1


def load_truck_2():
    # This function loads the second truck for the first trip of the day. The function adds the packages to truck in the
    # following order:
    # - Adds package that do not have a deadline of 'EOD'
    # - Adds packages that were delayed on flight
    # - Parses through the rest of the available packages and add packages and packages with matching addresses and
    #   stops when maximum package count is reached.
    # - Do not add packages with Wrong address
    # Time Complexity: O(N^3)
    # Space Complexity: O(N)
    package_count = 0
    temp_list = []
    for i in range(1, packages.size + 1):
        j = packages.search(i)
        if j[4] != "EOD" and i in available_packages:
            temp_list.append(int(i))
            package_count += 1
        if "Delayed" in j[6] and i in available_packages and i not in temp_list:
            temp_list.append(int(i))
            package_count += 1

    for i in range(1, packages.size + 1):
        j = packages.search(i)
        if package_count >= truck.MAX_PACKAGES:
            break
        elif "Wrong" in j[6]:
            continue
        elif i in available_packages and i not in temp_list:
            temp_list.append(int(i))
            package_count += 1
            for i in temp_list:
                j = packages.search(i)
                temp_address = j[0]
                for x in range(1, packages.size + 1):
                    if x in available_packages and x not in temp_list:
                        y = packages.search(x)
                        temp_address2 = y[0]
                        if temp_address == temp_address2 and package_count < truck.MAX_PACKAGES:
                            temp_list.append(int(x))
                            package_count += 1

    return temp_list


def rest_of_packages():
    # This function loads the rest of the available packages.
    # Time Complexity: O(N)
    # Space Complexity: O(N)
    temp_list = []
    for i in range(1, packages.size + 1):
        if i in available_packages:
            temp_list.append(int(i))

    return temp_list


def deliver(depart_time, load_list):
    # This function delivers the packages in the load_list parameter. Location_time is set to the depart_time parameter.
    # The While loop will iterate until the load_list  is empty. The For loop will iterate through the load_list to
    # determine the package with the closet distance. Once the package with the closet package is found, a delivered
    # time is calculated, location_time is set to the calculated delivered time, and closet distance is added to the
    # total distance. The delivered time is added to the package's values, and the anchor address is set to the
    # package's address ID. The package is removed from the available list and load list. Once the While loop finishes,
    # a return distance, and return time is calculated with from the last closet package and the Hub. The total distance
    # and return time is returned.
    # Time Complexity: O(N^2)
    # Space Complexity: O(1)
    anchor_address = 0
    trip_distance = 0
    location_time = depart_time
    while len(load_list) > 0:
        closet_distance = 5000
        for i in load_list:
            j = packages.search(i)
            address_ID = int(j[10])
            j[8] = depart_time
            if address_ID >= anchor_address:
                if graph.distance_list[address_ID][anchor_address] < closet_distance:
                    closet_ID = i
                    closet_distance = graph.distance_list[address_ID][anchor_address]
            elif anchor_address > address_ID:
                if graph.distance_list[anchor_address][address_ID] < closet_distance:
                    closet_ID = i
                    closet_distance = graph.distance_list[anchor_address][address_ID]

        delivered_time = location_time + datetime.timedelta(minutes=(closet_distance / (truck.AVG_SPEED / 60)))
        location_time = delivered_time
        print("%d has been delivered at %s" % (closet_ID, delivered_time))
        trip_distance += closet_distance
        package = packages.search(closet_ID)
        package[9] = delivered_time
        anchor_address = int(package[10])
        available_packages.remove(closet_ID)
        load_list.remove(closet_ID)

    return_distance = graph.distance_list[anchor_address][0]
    trip_distance += return_distance
    return_time = location_time + datetime.timedelta(minutes=(return_distance / (truck.AVG_SPEED / 60)))

    return trip_distance, return_time


def address_id():
    # This functions matches the address from the DistanceGraph class and the PackageTable class. Once a match is found,
    # the address ID from the DistanceGraph is added to the PackageTable values.
    # Time Complexity: O(N)
    # Space Complexity: O(1)
    for i in range(1, packages.size + 1):
        j = packages.search(i)
        package_address = j[0]
        add_ID = graph.search_address(package_address)
        packages.insert_addressID(i, add_ID)


def package_status():
    # This function return a list of all the packages, associated info, and status based on the time values entered by
    # the user.
    # Time Complexity: O(N)
    # Space Complexity: O(1)
    print()
    first_time = input("Enter beginning time for search(use military time and 08:00 format): ")
    second_time = input("Enter ending time for search(use military time and 08:00 format): ")

    first_time_split = first_time.split(':')
    first_hour = int(first_time_split[0])
    first_minute = int(first_time_split[1])
    first_time_format = datetime.datetime(2020, 9, 5, first_hour, first_minute)

    second_time_split = second_time.split(':')
    second_hour = int(second_time_split[0])
    second_minute = int(second_time_split[1])
    second_time_format = datetime.datetime(2020, 9, 5, second_hour, second_minute)

    for i in range(1, packages.size + 1):
        look_up_package_info(i)
        j = packages.search(i)
        if j[9] <= second_time_format:
            print('Package Status: Delivered at %s' % j[9])
        elif first_time_format <= j[8] <= second_time_format:
            print('Package Status: In route at %s' % j[8])
        else:
            print('Package Status: at Hub')
        print()


if __name__ == '__main__':

    # Create a DistanceGraph instance
    graph = DistanceGraph()

    # Create a Truck instance
    truck = Truck()

    # Create a PackageTable instance
    packages = PackageTable()
    available_packages = []

    total_distance = 0
    d = datetime.datetime(2020, 9, 5, 8, 0)

    # Read in distance data from CSV file
    # Time Complexity: O(N)
    # Space Complexity: O(1)
    with open('WGUPS_Distance_Table.csv') as file:
        readCSV = csv.reader(file, delimiter=',')
        for row in readCSV:
            address_ID = row[0]
            address_name = row[1].replace('North', 'N').replace('West', 'W').replace('East', 'E').replace('South', 'S')
            distances = row[2:]
            distances = list(map(float, distances))
            graph.insert_al(address_ID, address_name)
            graph.insert_dl(distances)

    # Read in package data from CSV file
    # Time Complexity: O(N^2)
    # Space Complexity: O(N)
    headerlines = 0
    with open('WGUPS_Package_File.csv') as file:
        read = csv.reader(file, delimiter=',')

        for row in read:
            if headerlines < 8:
                headerlines += 1
                continue
            key = int(row[0])
            values = []
            address_string = row[1].replace('North', 'N').replace('West', 'W').replace('East', 'E').replace('South',
                                                                                                            'S')
            values.append(address_string)
            for i in range(2, 8):
                values.append(row[i])
            initial_status = ['at Hub']
            values.append(initial_status)  # Initial status Hub
            values.append(None)  # Placeholder for date/time of in route
            values.append(None)  # Placeholder for date/time for delivered
            packages.insert(key, values)
            available_packages.append(key)

    # Calls the address_id function to add the address ID to the package values
    address_id()

    print("Western Governors University Parcel Service Routing Program")
    print()

    # Truck 1/First trip
    load_list = load_truck_1()
    print("Truck 1 Departure: %s" % d)
    print("Truck 1 Delivered the Following Packages:")
    trip_distance, return_time = deliver(d, load_list)
    print("Truck 1 Trip Distance: %f" % trip_distance)
    print("Truck 1 Return Time: %s" % return_time)
    print()
    total_distance += trip_distance

    # Truck 2/First trip
    load_list2 = load_truck_2()
    d = datetime.datetime(2020, 9, 5, 9, 5)
    print("Truck 2 Departure: %s" % d)
    print("Truck 2 Delivered the Following Packages:")
    trip_distance2, return_time2 = deliver(d, load_list2)
    print("Truck 2 Trip Distance: %f" % trip_distance2)
    print("Truck 2 Return Time: %s" % return_time2)
    print()
    total_distance += trip_distance2

    # Update the address for package 9
    i = packages.search(9)
    i[0] = "410 S State St"
    i[1] = "Salt Lake City"
    i[2] = "UT"
    i[3] = "84111"
    # Update address ID again
    address_id()

    # Truck 2/Second trip
    rest_of_list = rest_of_packages()
    print("Truck 2 Departure: %s" % return_time2)
    print("Truck 2 Delivered the Following Packages:")
    trip_distance3, return_time3 = deliver(return_time2, rest_of_list)
    print("Truck 2 Trip Distance: %f" % trip_distance3)
    print("Truck 2 Return Time: %s" % return_time3)
    print()
    total_distance += trip_distance3
    print()

    # Check to see if all packages have been delivered
    if not len(available_packages):
        print("All packages have been delivered.")
        print()
    else:
        print("All packages have not been delivered.")
        print()

    # Display the total distance traveled by all trucks and all trips
    print("Total Distance By All Trucks: %f" % total_distance)

    user_input = -1
    # Time Complexity: O(N)
    # Space Complexity: O(1)
    while user_input != 4:
        menu()
        user_input = int(input('Enter option: '))
        if user_input < 1 or user_input > 4:
            print('Please select a valid option')
        elif user_input == 1:
            package_id = int(input('Enter a package ID: '))
            print()
            display_package_info(package_id)
        elif user_input == 2:
            print()
            all_packages_info()
        elif user_input == 3:
            package_status()
        elif user_input == 4:
            sys.exit()
