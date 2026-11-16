from multiprocessing import Process, Lock, Semaphore, Manager, Value
import time
import random

CRATE_SIZE = 12
def picker(
    picker_id,
    crate,
    truck,
    tree_index,
    crate_count,
    tree_lock,
    crate_lock,
    loader_signal,
    picker_wait,
    done_pickers,
    total_pickers,
    TOTAL_FRUITS
):
    while True:
        with tree_lock: 

            if tree_index.value >= TOTAL_FRUITS + 1 :
                break
            fruit = tree_index.value
            tree_index.value += 1

            print(f"[Picker {picker_id}] picked fruit {fruit}")

        time.sleep(random.uniform(0.1, 0.4))  

        should_wait = False 
        with crate_lock:

            crate.append(fruit)
            crate_count.value += 1

            print(
                f"[Picker {picker_id}] placed fruit {fruit} "
                f"in crate slot {crate_count.value}/{CRATE_SIZE}"
            )
            if crate_count.value == CRATE_SIZE:

                print(f"[Picker {picker_id}] crate FULL -> calling loader")

                loader_signal.release() 
                
                should_wait = True
        if should_wait:
            picker_wait.acquire() 
    with done_pickers.get_lock(): 
        done_pickers.value += 1

        print(f"[Picker {picker_id}] tree is bare. Exiting.")
        if done_pickers.value == total_pickers:
            loader_signal.release() 

def loader(
    crate,
    truck,
    crate_count,
    crate_lock,
    loader_signal,
    picker_wait,
    done_pickers,
    total_pickers,
):

    while True:

        loader_signal.acquire()
        
        with crate_lock:
            if crate_count.value == CRATE_SIZE:

                print("\n[Loader] Loading FULL crate into truck...\n")

                truck.append(list(crate))

                crate[:] = []
                crate_count.value = 0

                print("[Loader] New empty crate supplied\n")

                active = total_pickers - done_pickers.value
                for _ in range(active):
                    picker_wait.release()
            if done_pickers.value == total_pickers:
                if crate_count.value > 0:
                    print("\n[Loader] Loading PARTIALLY filled crate into truck...\n")
                    truck.append(list(crate))
                    crate[:] = []
                    crate_count.value = 0

                print("[Loader] All work completed. Exiting.")
                break



def main(TOTAL_FRUITS):
    if TOTAL_FRUITS == 0:
        print("\n========== FINAL TRUCK ==========\n")
        print("No fruits to process.")
        print("Total crates loaded: 0")
        return

    manager = Manager() 

    crate = manager.list() 

    truck = manager.list()
    tree_index = Value('i', 1) 
    crate_count = Value('i', 0) 
    done_pickers = Value('i', 0)

    tree_lock = Lock() 
    crate_lock = Lock() 

    loader_signal = Semaphore(0)
    picker_wait = Semaphore(0)


    total_pickers = 3 

    loader_process = Process(
        target=loader,
        args=(
            crate,
            truck,
            crate_count,
            crate_lock,
            loader_signal,
            picker_wait,
            done_pickers,
            total_pickers
        ),
    )

    loader_process.start()
    pickers = []

    for i in range(total_pickers):

        p = Process(
            target=picker,
            args=(
                i + 1, 
                crate,
                truck,
                tree_index,
                crate_count,
                tree_lock,
                crate_lock,
                loader_signal,
                picker_wait,
                done_pickers,
                total_pickers,
                TOTAL_FRUITS
            ),
        )

        pickers.append(p)
        p.start()

    for p in pickers:
        p.join()

    loader_process.join() 
    print("\n========== FINAL TRUCK ==========\n")

    for i, c in enumerate(truck, start=1):
        print(f"Crate {i}: {c}")

    print(f"\nTotal crates loaded: {len(truck)}")
# if __name__ == "__main__":
#     try:
#         N = int(input("Enter the number of Fruits: "))
#         if N <0:
#             print("Number of fruits should be greater than 0!")
#             exit(0)
#     except ValueError:
#         print("Please Enter a valid Integer")

#     TOTAL_FRUITS = N
#     main(N)
if __name__ == "__main__":
    try:
        N = float(input("Enter the number of Fruits: "))

        # Check if the float is actually a whole number
        if N.is_integer():
            N = int(N)
        else:
            print("Please enter a whole number!")
            exit(0)

        if N < 0:
            print("Number of fruits should be greater than 0!")
            exit(0)

    except ValueError:
        print("Please Enter a valid number")

    TOTAL_FRUITS = N
    main(N)