import time
import threading

# Timer settings
work_duration = 25 * 60  # 25 minutes

# Control flag
is_running = False

# ASCII frames (Waschbär mit Tomato)
frames = [
    r"""
       🍅
     (\_/)  
     ( •_•)
     / >🍵   Fokus...
    """,
    r"""
       🍅
     (\_/)  
     ( •_•)👉
     / > 🍵  Umblättern...
    """,
    r"""
       🍅
     (\_/)  
     ( •o•)
     / > 🍵  Ups!
    """,
    r"""
       🍅
     (\_/)  
     ( -_-) zzz
     / > 🍵  Nap...
    """,
    r"""
       🍅
     (\_/)  
     ( •_•)☕
     / > 📖  Kaffee!
    """,
    r"""
       🍅
     (\_/)✨
     ( •‿•)
     / >🍰   Geschafft!
    """
]

def show_animation(stop_event, total_seconds):
    frame_index = 0
    progress_bar_length = 30
    elapsed = 0

    while not stop_event.is_set() and elapsed <= total_seconds:
        percent = elapsed / total_seconds
        filled = int(progress_bar_length * percent)
        
        # Farbige Progress Bar basierend auf Prozentsatz
        if percent <= 0.25:  # 0-25%: Rot
            filled_bar = f"\033[91m{'█' * filled}\033[0m"  # Rot
        elif percent <= 0.50:  # 25-50%: Gelb
            filled_bar = f"\033[93m{'█' * filled}\033[0m"  # Gelb
        elif percent <= 0.75:  # 50-75%: Blau
            filled_bar = f"\033[94m{'█' * filled}\033[0m"  # Blau
        else:  # 75-100%: Grün
            filled_bar = f"\033[92m{'█' * filled}\033[0m"  # Grün
            
        bar = filled_bar + "-" * (progress_bar_length - filled)
        percent_display = int(percent * 100)

        # Select motivational message
        if percent_display <= 25:
            quote = "💬 Fokus, Fokus, Fokus! 🎯"
        elif percent_display <= 50:
            quote = "💬 Weiter so, Waschbär-Champ! 🦝💪"
        elif percent_display <= 75:
            quote = "💬 Gleich geschafft! 🚀"
        elif percent_display < 100:
            quote = "💬 Endspurt! Du rockst das! 🤘"
        else:
            quote = "💬 BOOM! Geschafft! 🎉"

        # Clear screen + print frame
        print("\033c", end="")  # works on most terminals
        print(frames[frame_index % len(frames)])
        print(f"[{bar}] {percent_display}%")
        print(quote)

        time.sleep(10)  # Geändert von 2 auf 10 Sekunden
        elapsed += 10   # Geändert von 2 auf 10 Sekunden
        frame_index += 1

def start_pomodoro_timer():
    global is_running
    is_running = True
    stop_event = threading.Event()

    # Start animation thread
    anim_thread = threading.Thread(target=show_animation, args=(stop_event, work_duration))
    anim_thread.start()

    try:
        for remaining in range(work_duration, 0, -1):
            if not is_running:
                break
            mins, secs = divmod(remaining, 60)
            print(f"Time left: {mins:02}:{secs:02}", end="\r")
            time.sleep(1)
        if is_running:
            print("\nTime's up! Take a 5-minute break! 🎉🍅")
    except KeyboardInterrupt:
        print("\n[!] Timer interrupted.")
    finally:
        is_running = False
        stop_event.set()
        anim_thread.join()
        print("Returning to main menu...\n")

def main_menu():
    while True:
        print("\nWelcome to the Pomodoro Timer! 🦝🍅")
        print("1. Start Pomodoro Timer")
        print("2. Exit")
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            start_pomodoro_timer()
        elif choice == '2':
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
