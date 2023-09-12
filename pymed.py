import sqlite3
import os

# Function to search for diseases in the database
def search_diseases(query):
    keywords = query.split()  # Split user input into individual keywords
    conn = sqlite3.connect('codes.db')
    cursor = conn.cursor()

    # Create a dictionary to store the count of occurrences for each result
    result_counts = {}

    # Use a loop to search for each keyword separately and combine the results
    for keyword in keywords:
        cursor.execute('''
            SELECT code, name1
            FROM diseases
            WHERE code LIKE ? OR name1 LIKE ?
        ''', ('%' + keyword + '%', '%' + keyword + '%'))
        results = cursor.fetchall()
        
        # Increment the count for each result in the dictionary
        for result in results:
            code, name1 = result
            if (code, name1) in result_counts:
                result_counts[(code, name1)] += 1
            else:
                result_counts[(code, name1)] = 1

    conn.close()
    
    # Filter the results to include only those with two or more similar terms
    filtered_results = [result for result, count in result_counts.items() if count >= 2]
    
    return filtered_results

# Function to display search results with numbered options
def display_results(results):
    if not results:
        print("No matching records found.")
    else:
        print("Search Results:")
        for index, result in enumerate(results, start=1):
            code, name1 = result
            print(f"{index}. Code: {code}, Name1: {name1}")

# Function to view full code description
def view_description(code):
    conn = sqlite3.connect('codes.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT *
        FROM diseases
        WHERE code = ?
    ''', (code,))

    result = cursor.fetchone()
    conn.close()

    if result:
        code, subcode, subcode2, name1, name2, name3, category = result
        print("\nFull Code Description:")
        print("Code:", code)
        print("Subcode:", subcode)
        print("Subcode2:", subcode2)
        print("Name1:", name1)
        print("Name2:", name2)
        print("Name3:", name3)
        print("Category:", category)
        input("\nPress Enter to continue...")
    else:
        print("Code not found.")

# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ASCII banner
banner = """
██████╗ ██╗   ██╗     ███╗   ███╗███████╗██████╗ 
██╔══██╗╚██╗ ██╔╝     ████╗ ████║██╔════╝██╔══██╗
██████╔╝ ╚████╔╝█████╗██╔████╔██║█████╗  ██║  ██║
██╔═══╝   ╚██╔╝ ╚════╝██║╚██╔╝██║██╔══╝  ██║  ██║
██║        ██║        ██║ ╚═╝ ██║███████╗██████╔╝
╚═╝        ╚═╝        ╚═╝     ╚═╝╚══════╝╚═════╝
    netx421@proton.me 2023                                                                                                   
"""


menu1 = """
_  _ ____ _  _ _  _ 
|\/| |___ |\ | |  | 
|  | |___ | \| |__| 
                                                                                                                   
"""
keyword1 = """
    _  _ ____ _ _ _  _ ____ ____ ___ 
1 - |-:_ |===  Y  |/\| [__] |--< |__>                                                                                              
"""

code1 = """
    ____ ____ ___  ____
2 - |___ [__] |__> |===                                                                                             
"""
exit1 = """
    ____ _ _ _ ___
3 - |=== _X_ |  |                                                                                               
"""


# Main menu loop
while True:
    clear_screen()
    print(banner)
    print(menu1)
    print("--------------------------------------------------")
    print(keyword1)
    print(code1)
    print(exit1)
    print("--------------------------------------------------")

    choice = input("Enter your choice: ")

    if choice == '1':
        keyword = input("Enter a keyword to search for: ")
        results = search_diseases(keyword)
        display_results(results)
        if results:
            selection = input("Enter the number of the code to view its full description (or press Enter to continue): ")
            if selection.isdigit():
                selection = int(selection)
                if 1 <= selection <= len(results):
                    code, _ = results[selection - 1]
                    view_description(code)
                else:
                    print("Invalid selection.")
    elif choice == '2':
        partial_code = input("Enter a partial code to search for: ")
        results = search_diseases(partial_code)
        display_results(results)
        if results:
            selection = input("Enter the number of the code to view its full description (or press Enter to continue): ")
            if selection.isdigit():
                selection = int(selection)
                if 1 <= selection <= len(results):
                    code, _ = results[selection - 1]
                    view_description(code)
                else:
                    print("Invalid selection.")
    elif choice == '3':
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please select a valid option (1, 2, or 3).")

