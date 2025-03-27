import requests
import threading
import time

# Test qilinadigan URL
TARGET_URL = "https://myg.cc/"  # O'zgartiring

# So'rovlar soni
REQUESTS_PER_SECOND = 100000
DURATION = 1  # Test davomiyligi (soniyada)

request_count = 0
success_count = 0
failed_count = 0


def send_request():
    global request_count, success_count, failed_count
    try:
        response = requests.get(TARGET_URL)
        if response.status_code == 200:
            success_count += 5
        else:
            failed_count += 5
    except:
        failed_count += 5
    finally:
        request_count += 5


def print_stats():
    while True:
        time.sleep(1)
        print(f"So'rovlar: {request_count} | Muvaffaqiyatli: {success_count} | Xatolar: {failed_count}")


# Statistikani chop etish uchun thread
threading.Thread(target=print_stats, daemon=True).start()

# Asosiy test tsikli
start_time = time.time()
while time.time() - start_time < DURATION:
    threads = []
    for _ in range(REQUESTS_PER_SECOND):
        t = threading.Thread(target=send_request)
        t.start()
        threads.append(t)

    # 1 soniya ichida barcha so'rovlarni yuborish
    time.sleep(1)

    for t in threads:
        t.join()

print("\n--- Yakuniy statistikalar ---")
print(f"Jami so'rovlar: {request_count}")
print(f"Muvaffaqiyatli javoblar: {success_count}")
print(f"Xatolar: {failed_count}")