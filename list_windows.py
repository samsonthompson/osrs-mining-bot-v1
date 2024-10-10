import pygetwindow as gw

def list_window_titles():
    windows = gw.getAllTitles()
    for title in windows:
        if title:  # Filter out empty titles
            print(title)

if __name__ == "__main__":
    list_window_titles()