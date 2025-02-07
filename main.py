# Author: Matthew Witkowski
# Date: 3/1/2025
# CS341 Project 1


import sqlite3
import matplotlib.pyplot as plt
# sys used for input.txt file to compare to output
import sys

def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    # selects all general stats from database and displays
    print("General Statistics:")
    sqlite = """
    SELECT
        (SELECT COUNT(*) FROM RedCameras), 
        (SELECT COUNT(*) FROM SpeedCameras),
        (SELECT COUNT(*) FROM RedViolations),
        (SELECT COUNT(*) FROM SpeedViolations),
        (SELECT MIN(Violation_Date) FROM RedViolations),
        (SELECT MAX(Violation_Date) FROM SpeedViolations),
        (SELECT SUM(Num_Violations) FROM RedViolations),
        (SELECT SUM(Num_Violations) FROM SpeedViolations)
    """
    dbCursor.execute(sqlite)
    row = dbCursor.fetchone()
    print("  Number of Red Light Cameras:", f"{row[0]:,}")
    print("  Number of Speed Cameras:", f"{row[1]:,}")
    print("  Number of Red Light Camera Violation Entries:", f"{row[2]:,}")
    print("  Number of Speed Camera Violation Entries:", f"{row[3]:,}")
    print(f"  Range of Dates in the Database: {row[4]} - {row[5]}")
    print("  Total Number of Red Light Camera Violations:", f"{row[6]:,}")
    print("  Total Number of Speed Camera Violations:", f"{row[7]:,}")
##################################################################  


# function that sends the user to the respective func 
# some might say that fun1 should be more descriptive, but I find this to be much more organized 
# comments above the function will describe what the function does
# and everything is already listed with the program
def withinrange(inp,dbConn):    
    if inp == 1:
        fun1(dbConn)
    elif inp == 2:
        fun2(dbConn)
    elif inp == 3:
        fun3(dbConn)
    elif inp == 4:
        fun4(dbConn)
    elif inp == 5:
        fun5(dbConn)
    elif inp == 6:
        fun6(dbConn)
    elif inp == 7:
        fun7(dbConn)
    elif inp == 8:
        fun8(dbConn)
    elif inp == 9:
        fun9(dbConn) 

# Find an intersection by name
def fun1(dbConn):
    print()
    inp = input("Enter the name of the intersection to find (wildcards _ and % allowed): ")
    dbCursor = dbConn.cursor()
    # this is how most of my sql queries will look
    # i will select the columns that will be displayed, setting an alias, and then filtering by input when needed
    # then I order the output to follow what is needed

    # this one is simple, as it selects the intersection information, filters by the input whilst allowing wildcards
    # and then orders by the intersection name
    sqlite = """
    SELECT i.Intersection_ID, i.Intersection
    FROM Intersections as i
    WHERE i.Intersection LIKE ? 
    ORDER BY i.Intersection ASC;
    """
    dbCursor.execute(sqlite, (inp,))
    rows = dbCursor.fetchall()
    # checks that rows returned something, prints all the intersections that match the input
    if rows:
        for x in rows:
            print(f"{x[0]} : {x[1]}")
    else:
        print("No intersections matching that name were found.")
    print()

# Find all cameras at an intersection
def fun2(dbConn):
    print()
    inp = input("Enter the name of the intersection (no wildcards allowed):")
    dbCursor = dbConn.cursor()
    # this one selects the cameraID and address for red cameras, and then joins it with intersections to get all the outputs that share the same cameraID
    # then it filters by the input, and orders by the cameraID
    redsql = """
    SELECT rc.Camera_ID, rc.Address
    FROM RedCameras AS rc
    JOIN Intersections AS i ON rc.Intersection_ID = i.Intersection_ID
    WHERE i.Intersection = ?
    ORDER BY rc.Camera_ID ASC    

    """
    # this one is the same as the last one but for speedcamera. I do two seperate queries for less complexity as the outputs are seperated 
    speedsql = """
    SELECT sc.Camera_ID, sc.Address
    FROM SpeedCameras AS sc
    JOIN Intersections AS i ON sc.Intersection_ID = i.Intersection_ID
    WHERE i.Intersection = ?
    ORDER BY sc.Camera_ID ASC    
    """

    dbCursor.execute(redsql, (inp,))
    redrows = dbCursor.fetchall()
    
    dbCursor.execute(speedsql, (inp,))
    speedrows = dbCursor.fetchall()

    print()
    # checks if rows ouputted, then displays cameraID and address for each camera at the intersection for both red cam and speed cam
    if redrows:
        print("Red Light Cameras:")
        for x in redrows:
            print(f"   {x[0]} : {x[1]}") 
        print()
    else:
        print("No red light cameras found at that intersection.")
        print()    
    if speedrows:
        print("Speed Cameras:")
        for x in speedrows:
            print(f"   {x[0]} : {x[1]}")
        print()
    else:
        print("No speed cameras found at that intersection.")
        print()    
        

# Percentage of violations for a specific date
def fun3(dbConn):
    print()
    inp = input("Enter the date that you would like to look at (format should be YYYY-MM-DD): ")
    dbCursor = dbConn.cursor()
    # this one is very simple just sums the amount of violations for both red violations and speed violations
    # filtering by input date
    redsql= """
    SELECT SUM(Num_Violations)
    FROM RedViolations
    WHERE Violation_Date = ?
    """
    speedsql = """
    SELECT SUM(Num_Violations)
    FROM SpeedViolations 
    WHERE Violation_Date = ? 
    """
    dbCursor.execute(redsql, (inp,))
    redrow = dbCursor.fetchone()
    
    dbCursor.execute(speedsql, (inp,))
    speedrow = dbCursor.fetchone()

    # checks if redrow and speedrow are empty tuples, before adding them together
    if redrow[0] == None and speedrow[0] == None:
        print("No violations on record for that date.")
        print()
        return
    # sets trv = total red violations tsv = total speed violations, dealing with None values with or statement
    # calculates percentage for each violation type, sp = speed percentage, rp = red percentage
    trv = redrow[0] or 0
    tsv = speedrow[0] or 0
    total = tsv+trv
    sp = (tsv/total)*100
    rp = (trv/total)*100
    print(f"Number of Red Light Violations: {trv:,} ({rp:.3f}%)")
    print(f"Number of Speed Violations: {tsv:,} ({sp:.3f}%)")
    print(f"Total Number of Violations: {total:,}")

# Number of cameras at each intersection
def fun4(dbConn):
    dbCursor = dbConn.cursor()
    # selects intersection name, id, and counts the amount of cameras at each intersection
    # the selects the count of the total amount of red light cameras
    #  joins red cameras with intersection based off which cameras they share
    # then groups by intersection id, orders by the amount of cameras at each intersection
    redsql = """
    SELECT i.Intersection, i.Intersection_ID, COUNT(rc.Camera_ID) AS rcnum,
    (SELECT COUNT(*) FROM RedCameras) AS rctotal
    FROM Intersections AS i
    JOIN RedCameras AS rc ON i.Intersection_ID = rc.Intersection_ID
    GROUP BY i.Intersection_ID
    ORDER BY rcnum DESC;
    """
    # same as redsql but for speed cameras
    speedsql = """
    SELECT i.Intersection, i.Intersection_ID, COUNT(sc.Camera_ID) AS scnum,
    (SELECT COUNT(*) FROM SpeedCameras) AS sctotal
    FROM Intersections AS i
    JOIN SpeedCameras AS sc ON i.Intersection_ID = sc.Intersection_ID
    GROUP BY i.Intersection_ID
    ORDER BY scnum DESC;
    """

    dbCursor.execute(redsql)
    redrows = dbCursor.fetchall()
    dbCursor.execute(speedsql)
    speedrows = dbCursor.fetchall()

    print()
    print("Number of Red Light Cameras at Each Intersection")
    # first calculates percentage of red cameras at each intersection, then orders by largest
    if redrows:
        for x in redrows:
            percent = ((x[2]*100)/x[3])
            print(f" {x[0]} ({x[1]}) : {x[2]} ({percent:.3f}%)")
    print()
    print()
    # first calculates percentage of red cameras at each intersection, then orders by largest
    print("Number of Speed Cameras at Each Intersection")             
    if speedrows:
        for x in speedrows:
            percent = ((x[2]*100)/x[3])
            print(f" {x[0]} ({x[1]}) : {x[2]} ({percent:.3f}%)")
    print()

# Number of violations at each intersection, given a year
def fun5(dbConn):
    print()
    inp = input("Enter the year that you would like to analyze: ")
    dbCursor = dbConn.cursor()
    # sums all violations in the year for red violations
    tredsql ="""
    SELECT SUM(rv.Num_Violations)
    FROM RedViolations AS rv
    WHERE strftime('%Y', rv.Violation_Date) = ?;
    """
    # does the same for speed violation
    # we seperate these two from the main query as we need to find total violations for each type without any filtering
    tspeedsql = """
    SELECT SUM(sv.Num_Violations)
    FROM SpeedViolations AS sv
    WHERE strftime('%Y', sv.Violation_Date) = ?;
    """
    # now finds the amount of red violations for specific intersection and orders by greatest amount of violations
    redsql ="""
    SELECT i.Intersection, i.Intersection_ID, SUM(rv.Num_Violations) AS tv
    FROM RedViolations AS rv
    JOIN RedCameras AS rc ON rv.Camera_ID = rc.Camera_ID
    JOIN Intersections AS i ON i.Intersection_ID = rc.Intersection_ID
    WHERE strftime('%Y', rv.Violation_Date) = ?
    GROUP BY i.Intersection_ID, i.Intersection
    ORDER BY tv DESC, i.Intersection_ID DESC;
    """
    # same thing for speed violations
    speedsql = """
    SELECT i.Intersection, i.Intersection_ID, SUM(sv.Num_Violations) AS tv
    FROM SpeedViolations AS sv
    JOIN SpeedCameras AS sc ON sv.Camera_ID = sc.Camera_ID
    JOIN Intersections AS i ON i.Intersection_ID = sc.Intersection_ID
    WHERE strftime('%Y', sv.Violation_Date) = ?
    GROUP BY i.Intersection_ID, i.Intersection
    ORDER BY tv DESC, i.Intersection_ID DESC;
    """
    # we first execute the total query 
    dbCursor.execute(tredsql, (inp,))
    tred = dbCursor.fetchone()
    dbCursor.execute(tspeedsql, (inp,))
    tspeed = dbCursor.fetchone()
    # we then execute the main queries that get use the specific intersections and their data
    dbCursor.execute(redsql, (inp,))
    redrows = dbCursor.fetchall()
    dbCursor.execute(speedsql, (inp,))
    speedrows = dbCursor.fetchall()
    # we then print the data with relevant info like intersection name and total red light violations for that intersection, with calculations for the percentage with our two queries
    # this is also a good time to mention that I like to use x for my for loops as it is standarized across all my functions and easier to read
    print(f"\nNumber of Red Light Violations at Each Intersection for {inp}")
    if redrows:
        for x in redrows:
            if tred[0]:
                percent = ((x[2]*100)/tred[0])
            else:
                percent = 0
            print(f"  {x[0]} ({x[1]}) : {x[2]:,} ({percent:.3f}%)")
        print(f"Total Red Light Violations in {inp} : {tred[0]:,}")

    else:
        print("No red light violations on record for that year.")
    print()
    # same thing for speedd violations
    print(f"Number of Speed Violations at Each Intersection for {inp}")             
    if speedrows:
        for x in speedrows:
            if tspeed[0]:
                percent = ((x[2]*100)/tspeed[0])
            else: 
                percent = 0
            print(f"  {x[0]} ({x[1]}) : {x[2]:,} ({percent:.3f}%)")
        print(f"Total Speed Violations in {inp} : {tspeed[0]:,}")
    else:
        print("No speed violations on record for that year.")
    print()

# Number of violations by year, given a camera ID
def fun6(dbConn):
    print()
    inp = input("Enter a camera ID: ")
    dbCursor = dbConn.cursor()
    # so this query is a little different than the rest
    # since we need to find number of violations every year for a specific camera,
    # we use a subquery to combine both red and speed violations into one table
    # then we select by year, and sum the total number of violations
    # group by year and order by year
    sqlite = """
    SELECT strftime('%Y', v.Violation_Date) AS y, SUM(v.Num_Violations) AS tv
    FROM ( 
        SELECT rv.Violation_Date, rv.Num_Violations, rv.Camera_ID
        FROM RedViolations AS rv
        JOIN RedCameras AS rc ON rv.Camera_ID = rc.Camera_ID
        WHERE rc.Camera_ID = ?
        UNION ALL
        SELECT sv.Violation_Date, sv.Num_Violations, sv.Camera_ID
        FROM SpeedViolations AS sv
        JOIN SpeedCameras AS sc ON sv.Camera_ID = sc.Camera_ID
        WHERE sc.Camera_ID = ?
    ) AS v
    GROUP by y
    ORDER BY y ASC;
    """
    # inputs two inputs as we need to filter by cameraID twice
    dbCursor.execute(sqlite, (inp,inp))
    rows = dbCursor.fetchall()
    
    # this checks that thte rows are not empty, so that we dont output any additional text if it is
    if not rows:
        print("No cameras matching that ID were found in the database.")
        print()
        return
    
    # this prints the year and the total amount of violations for that year 
    print(f"Yearly Violations for Camera {inp}")
    for x in rows:
        print(f"{x[0]} : {x[1]:,}")
    print()
    # here is our first plot! this is pretty simple we just set the plot size, plot the x and y for all the rows, and set some labels
    plotinp = input("Plot? (y/n)")
    print()
    if plotinp == 'y':
        plt.figure(figsize=(7,5))
        plt.plot([x[0] for x in rows], [y[1] for y in rows])
        plt.title(f"Yearly Violations for Camera {inp}")
        plt.xlabel("Year")
        plt.ylabel("Number of Violations")
        plt.show()
    else:
        return

# Number of violations by month, given a camera ID and year
def fun7(dbConn):
    print()
    inpid = input("Enter a camera ID: ")
    dbCursor = dbConn.cursor()
    # i have 2 queries here for error handling. this first queries only job is to check if camera id is valid from user input
    camsql = """
    SELECT Camera_ID FROM (
        SELECT rc.Camera_ID
        FROM RedCameras AS rc
        UNION
        SELECT sc.Camera_ID
        FROM SpeedCameras AS sc
        ) AS c
        WHERE c.Camera_ID = ?
    """
    # this is the check to see if valid and then returns if not
    dbCursor.execute(camsql, (inpid,))
    row = dbCursor.fetchone()
    if not row:
        print("No cameras matching that ID were found in the database.")
        print()
        return
    
    # now we prompt for a year and then filter by that year and by camera id, so the previous check was needed
    # we then select the month for each violation date, and sum the total number of violations for that month
    # we do the same thing we did in func6, with the subquery and grouping by month instead of year
    inpyear = input("Enter a year: ")
    sqlite = """
    SELECT v.m, SUM(v.Num_Violations) AS tv
    FROM ( 
        SELECT strftime('%m', rv.Violation_Date) AS m, rv.Num_Violations, rv.Camera_ID
        FROM RedViolations AS rv
        JOIN RedCameras AS rc ON rv.Camera_ID = rc.Camera_ID
        WHERE rc.Camera_ID = ? AND strftime('%Y', rv.Violation_Date) = ?
        UNION ALL
        SELECT strftime('%m', sv.Violation_Date) AS m, sv.Num_Violations, sv.Camera_ID
        FROM SpeedViolations AS sv
        JOIN SpeedCameras AS sc ON sv.Camera_ID = sc.Camera_ID
        WHERE sc.Camera_ID = ? AND strftime('%Y', sv.Violation_Date) = ?
    ) AS v
    GROUP by m
    ORDER BY m ASC;
    """
    dbCursor.execute(sqlite, (inpid, inpyear,inpid,inpyear))
    rows = dbCursor.fetchall()
    # we then print the month and the total amount of violations for that month
    print(f"Monthly Violations for Camera {inpid} in {inpyear}")
    for x in rows:
        print(f"{x[0]}/{inpyear} : {x[1]:,}")
    print()
    # another plot, same thing as the last really
    plotinp = input("Plot? (y/n)")
    print()
    if plotinp == 'y':
        plt.figure(figsize=(7,5))
        plt.plot([x[0] for x in rows], [y[1] for y in rows])
        plt.title(f"Monthly Violations for Camera {inpid} ({inpyear})")
        plt.xlabel("Month")
        plt.ylabel("Number of Violations")
        plt.show()
    else:
        return

# Compare the number of red light and speed violations, given a year
def fun8(dbConn):
    print()
    inpyear = input("Enter a year: ")
    dbCursor = dbConn.cursor()
    # this has some new things in the queries. so first we select yy-mm-dd to display in our output, but then we select the important part
    # we find the violation date, and we set it by the date in relation to the year with %j, so 02/01 would be 32
    # we then cast it to set it to an integer so we dont have to convert all the times we use it, also since its a tuple its harder to convert
    # we then sum the total number of violations for that day, and group by day, and order by day
    redsql = """
    SELECT strftime('%Y-%m-%d', rv.Violation_Date) AS d, CAST(strftime('%j', rv.Violation_Date) AS INTEGER) AS days, SUM(rv.Num_Violations) AS tv
    FROM RedViolations AS rv
    JOIN RedCameras AS rc ON rv.Camera_ID = rc.Camera_ID
    WHERE strftime('%Y', rv.Violation_Date) = ?
    GROUP BY d
    ORDER BY d ASC;
    """
    # same exact thing but for speed violations
    speedsql = """
    SELECT strftime('%Y-%m-%d', sv.Violation_Date) AS d, CAST(strftime('%j', sv.Violation_Date) AS INTEGER) AS days, SUM(sv.Num_Violations) AS tv
    FROM SpeedViolations AS sv
    JOIN SpeedCameras AS sc ON sv.Camera_ID = sc.Camera_ID
    WHERE strftime('%Y', sv.Violation_Date) = ?
    GROUP BY d
    ORDER BY d ASC;
    """
    dbCursor.execute(redsql, (inpyear,))
    redrows = dbCursor.fetchall()
    dbCursor.execute(speedsql, (inpyear,))
    speedrows = dbCursor.fetchall()

    # creates a dict for both red and speed violations
    # for each row in redrows, set the day in terms of year to the key,
    # and total number of violations for the day as the value
    rd = {row[1]: row[2] for row in redrows}
    sd = {row[1]: row[2] for row in speedrows}
    
    # this creates a list for all the days in the year
    days =list(range(1, 366))

    # sets the x axis for plotting
    xred = days
    xspeed = days

    # adds the amount of violations recorded in that day to the y
    # if no violations exist for that day, set to 0
    yred = [rd.get(day, 0) for day in days]
    yspeed = [sd.get(day, 0) for day in days]   

    # here we just print the first 5 and last 5 of each total violation in terms of days for the whole year with slicing
    print("Red Light Violations:")
    for x in redrows[:5]:
        print(f"{x[0]} {x[2]}")
    for x in redrows[-5:]:
        print(f"{x[0]} {x[2]}")
    
    print("Speed Violations:")
    for x in speedrows[:5]:
        print(f"{x[0]} {x[2]}")
    for x in speedrows[-5:]:
        print(f"{x[0]} {x[2]}")
    print()
    
    # this plot uses the the xred,yred xspeed,yspeed we did before in order to show 0 for the data for days that are not in the database
    # this is for examples like 2014, where there is no data available, but we still need to show in the plot
    plotinp = input("Plot? (y/n)")
    print()
    if plotinp == 'y':
        plt.figure(figsize=(7,5))
        plt.plot(xred,yred,color='red')
        plt.plot(xspeed, yspeed,color='orange')
        plt.title(f"Violation Each Day of {inpyear}")
        plt.legend(["Red Light", "Speed"])
        plt.xlabel("Day")
        plt.ylabel("Number of Violations")
        plt.show()
    else:
        return

# Find cameras located on a street
def fun9(dbConn):
    print()
    inp = input("Enter a street name: ")
    # cleans the input for wildcards
    cleaninp = f"%{inp}%"
    dbCursor = dbConn.cursor()
    # this one is back to simply, query selects all the points it needs for 
    # the plot, for red cameras, filters by address, orders by cameraID
    redsql = """
    SELECT rc.Camera_ID, rc.Address, rc.Latitude, rc.Longitude
    from RedCameras AS rc
    WHERE rc.Address LIKE ?
    ORDER BY rc.Camera_ID ASC
    """
    # same thing as redsql as always ;)
    speedsql = """
    SELECT sc.Camera_ID, sc.Address, sc.Latitude, sc.Longitude
    from SpeedCameras AS sc
    WHERE sc.Address LIKE ?
    ORDER BY sc.Camera_ID ASC
    """
    dbCursor.execute(redsql, (cleaninp,))
    redrows = dbCursor.fetchall()
    dbCursor.execute(speedsql, (cleaninp,))
    speedrows = dbCursor.fetchall()

    # checks that rows are not empty
    if not redrows and not speedrows:
        print("There are no cameras located on that street.")
        print()
        return

    print()
    print(f"List of Cameras Located on Street: {inp}")
    # prints the info we selected from the query 
    print("  Red Light Cameras:")
    for x in redrows:
        print(f"     {x[0]} : {x[1]} ({x[2]}, {x[3]})")
    print("  Speed Cameras:")
    for x in speedrows:
        print(f"     {x[0]} : {x[1]} ({x[2]}, {x[3]})")
    print()

    # so this is unique to the program
    # first we overlay the image of chicago map
    # then we plot the lat and long for each camera on the map, with different colors
    # and setting a dot for each camera location
    # we then annotate the cameraID for each camera, which overlays the cameraID for each one
    # it looks pretty ugly and you cant even read it most of the time but hey thats what they wanted
    plotinp = input("Plot? (y/n)")
    print()
    if plotinp == 'y':
        image = plt.imread("chicago.png")
        xydims = [-87.9277, -87.5569, 41.7012, 42.0868] # area covered by the map
        plt.imshow(image, extent=xydims)
        
        plt.plot([x[3] for x in redrows], [y[2] for y in redrows], color='red',marker='o',linestyle='-')  
        plt.plot([x[3] for x in speedrows], [y[2] for y in speedrows], color='orange',marker='o',linestyle='-')  

        for x in redrows:
            plt.annotate(x[0], (x[3], x[2]))
        for x in speedrows:
            plt.annotate(x[0], (x[3], x[2]))
        
        plt.title(f"Cameras on Street: {inp}")
        plt.xlim([-87.9277, -87.5569])
        plt.ylim([41.7012, 42.0868])
        plt.show()


#
# main
#

# this is for testing 
if len(sys.argv) > 1:
    sys.stdin = open(sys.argv[1], 'r')

dbConn = sqlite3.connect('chicago-traffic-cameras.db')

print("Project 1: Chicago Traffic Camera Analysis")
print("CS 341, Spring 2025")
print()
print("This application allows you to analyze various")
print("aspects of the Chicago traffic camera database.")
print()
print_stats(dbConn)
print()

# while loop so user is always prompted with this after completing a function
while True:
    print("Select a menu option:")
    print("  1. Find an intersection by name")
    print("  2. Find all cameras at an intersection")
    print("  3. Percentage of violations for a specific date")
    print("  4. Number of cameras at each intersection")
    print("  5. Number of violations at each intersection, given a year")
    print("  6. Number of violations by year, given a camera ID")
    print("  7. Number of violations by month, given a camera ID and year")
    print("  8. Compare the number of red light and speed violations, given a year")
    print("  9. Find cameras located on a street")
    print("or x to exit the program.")
    
    inp = input("Your choice --> ")

    # so we first chek that the user wants to leave
    # we then check if the user inputted a number within the range
    # inside a try except statement so that if the user inputs a string, it wont crash
    # if user inputs integer that is not within range, 
    # it reprints everything and asks for them to try again
    if inp == 'x':
        break
    try: 
        inp = int(inp)
        if 0 < inp < 10:
            withinrange(inp,dbConn)
        else:
            print("Error, unknown command, try again...")
    except ValueError:
        print("Error, unknown command, try again...")
print("Exiting program.")

# and thats the program!

#
# done
#
