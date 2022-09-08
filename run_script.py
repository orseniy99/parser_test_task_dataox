from db_collector import get_db_now
from csv_collector import get_csv_now
import time

if __name__ == '__main__':
    start_time = time.time()
    while True:
        try:
            answer = input("HOW DO YOU WANT TO SAVE DATA? [TYPE ONE: CSV / DB / BOTH ]: ")
        except ValueError:
            print("TRY AGAIN")
            continue
        if answer == "DB" or "CSV" or "BOTH":
            if answer == "DB":
                get_db_now()
                print("db data insert complete")
                break
            elif answer == "CSV":
                get_csv_now()
                print("csv file complete")
                break
            elif answer == "BOTH":
                get_csv_now()
                print("csv file complete")
                get_db_now()
                print("db data insert complete")
                break
            else:
                print("ERROR. NO SUCH ANSWER. TRY ONE OF THIS: CSV | DB | BOTH")
        else:
            print("NO SUCH ANSWER. TRY ONE OF THIS: CSV | DB | BOTH")
            continue

    end_time = time.time()
    runtime = end_time - start_time
    print(f'Program runtime is {round(runtime)} sec')