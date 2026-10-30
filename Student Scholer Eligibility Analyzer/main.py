import pandas as pd

# Scholarship amounts
FULL_SCHOLARSHIP = 50000
PARTIAL_SCHOLARSHIP = 25000

# CSV file name
FILE_NAME = "students.csv"


# STEP 1: Load student data
def load_students():

    try:
        df = pd.read_csv(FILE_NAME, dtype=str)

        required_columns = [
            "Name",
            "Marks (%)",
            "Income (per year)",
            "Attendance (%)"
        ]

        # Check CSV columns
        for col in required_columns:
            if col not in df.columns:
                print("Missing column:", col)
                return pd.DataFrame()

        valid_students = []

        # Check every student row
        for index, row in df.iterrows():

            name = row["Name"].strip()

            try:
                marks = float(row["Marks (%)"])
            except ValueError:
                print(
                    f"Invalid marks for {name}: "
                    f"'{row['Marks (%)']}'. Row skipped."
                )
                continue

            try:
                income = float(row["Income (per year)"])
            except ValueError:
                print(f"Invalid income for {name}. Row skipped.")
                continue

            try:
                attendance = float(row["Attendance (%)"])
            except ValueError:
                print(f"Invalid attendance for {name}. Row skipped.")
                continue

            # Validate values
            if not name or not (
                0 <= marks <= 100
                and income >= 0
                and 0 <= attendance <= 100
            ):
                print(f"Invalid data for {name}. Row skipped.")
                continue

            valid_students.append({
                "Name": name,
                "Marks (%)": marks,
                "Income (per year)": income,
                "Attendance (%)": attendance
            })

        return pd.DataFrame(valid_students)

    except FileNotFoundError:
        print("students.csv file not found!")
        return pd.DataFrame()

    except pd.errors.EmptyDataError:
        print("CSV file is empty!")
        return pd.DataFrame()


# STEP 2: Check scholarship eligibility
def check_eligibility(df):

    if df.empty:
        print("No valid student records found.")
        return df

    df = df.copy()

    # Eligibility condition
    eligible = (
        (df["Marks (%)"] >= 75)
        & (df["Income (per year)"] <= 500000)
        & (df["Attendance (%)"] >= 75)
    )

    df["Status"] = "Not Eligible"
    df["Scholarship"] = 0

    # Full scholarship condition
    full = (
        eligible
        & (df["Marks (%)"] >= 90)
        & (df["Income (per year)"] <= 300000)
    )

    # Partial scholarship condition
    partial = eligible & (~full)

    df.loc[full, "Status"] = "Eligible - Full"
    df.loc[full, "Scholarship"] = FULL_SCHOLARSHIP

    df.loc[partial, "Status"] = "Eligible - Partial"
    df.loc[partial, "Scholarship"] = PARTIAL_SCHOLARSHIP

    return df


# STEP 3: Display student results
def display_results(df):

    if df.empty:
        print("No results available.")
        return

    print("\n========== SCHOLARSHIP RESULTS ==========")

    for _, row in df.iterrows():

        if row["Status"] == "Eligible - Full":
            result = "Full"

        elif row["Status"] == "Eligible - Partial":
            result = "Partial"

        else:
            result = "Not Eligible"

        print(
            f"{row['Name']} | {result} | "
            f"Rs. {int(row['Scholarship'])}"
        )


# STEP 4: Display summary
def show_summary(df):

    if df.empty:
        print("No valid student records found.")
        return

    eligible = df[df["Status"] != "Not Eligible"]

    not_eligible = df[df["Status"] == "Not Eligible"]

    full = df[df["Status"] == "Eligible - Full"]

    partial = df[df["Status"] == "Eligible - Partial"]

    total_scholarship = df["Scholarship"].sum()

    if not eligible.empty:
        average_marks = eligible["Marks (%)"].mean()
    else:
        average_marks = 0

    print("\n========== SUMMARY ==========")

    print("Total Students:", len(df))
    print("Eligible:", len(eligible))
    print("Not Eligible:", len(not_eligible))
    print("Full Scholarship:", len(full))
    print("Partial Scholarship:", len(partial))

    print("Total Scholarship: Rs.", int(total_scholarship))

    print("Average Eligible Marks:", f"{average_marks:.2f}")


# STEP 5: Filter students by minimum marks
def filter_students(df):

    if df.empty:
        print("No valid student records found.")
        return

    try:
        minimum_marks = float(
            input("Enter minimum marks: ")
        )

        if not 0 <= minimum_marks <= 100:
            print("Enter marks between 0 and 100.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    filtered = df[df["Marks (%)"] >= minimum_marks]

    print("\n========== FILTERED STUDENTS ==========")

    if filtered.empty:
        print("No students found.")

    else:
        for _, row in filtered.iterrows():
            print(
                row["Name"],
                "| Marks:",
                row["Marks (%)"]
            )


# STEP 6: Main menu
def main():

    print("======================================")
    print(" STUDENT SCHOLARSHIP ELIGIBILITY ANALYZER")
    print("======================================")

    students = load_students()

    if students.empty:
        print("No valid data available. Program stopped.")
        return

    results = check_eligibility(students)

    while True:

        print("\n========== MAIN MENU ==========")
        print("1. Check Scholarship Eligibility")
        print("2. Show Scholarship Summary")
        print("3. Filter Students by Minimum Marks")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            display_results(results)

        elif choice == "2":
            show_summary(results)

        elif choice == "3":
            filter_students(results)

        elif choice == "4":
            print("Thank you for using Scholarship Analyzer!")
            break

        else:
            print("Invalid choice! Please select 1 to 4.")


# STEP 7: Run program
if __name__ == "__main__":
    main()