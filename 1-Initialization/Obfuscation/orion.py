import time
import sys

def orion():

    print('''
                                                                    
      ,ad8888ba,    88888888ba   88    ,ad8888ba,    888b      88  
     d8"'    `"8b   88      "8b  88   d8"'    `"8b   8888b     88  
    d8'        `8b  88      ,8P  88  d8'        `8b  88 `8b    88  
    88          88  88aaaaaa8P'  88  88          88  88  `8b   88  
    88          88  88""""88'    88  88          88  88   `8b  88  
    Y8,        ,8P  88    `8b    88  Y8,        ,8P  88    `8b 88  
     Y8a.    .a8P   88     `8b   88   Y8a.    .a8P   88     `8888  
      `"Y8888Y"'    88      `8b  88    `"Y8888Y"'    88      `888  
    ''')

    print(''' 
     __          __   __             __               __   __  
    |__) \ /    /__` /  \ |     /\  |__) |  | | |\ | |  \ /__` 
    |__)  |     .__/ \__/ |___ /~~\ |  \ |/\| | | \| |__/ .__/ 
                                                            
    ''')

    print("Manage and monitor your IT infrastructures !")
    print("This software is a proprietary software owned by Solarwinds. Partial or total reproduction is strictly forbidden.")

    time.sleep(3)
    print("\n")
    print("Launching auto-analysis of infrastructures...")
    time.sleep(1)
    print("Step 1/5 : Scanning network...")

    animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]

    for i in range(len(animation)):
        time.sleep(0.5)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()
    print("\n")

    print("Step 1/5 : Done")
    print("\n")
    time.sleep(0.5)
    print("Step 2/5 : Loading Orion Agent...")

    for i in range(4):
        time.sleep(0.5)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()
    print("\n")

    print("Fatal error (code 211-1) : No product key was found for running this software. Add your key to the Orion folder or purchase a license on solarwinds.com.")
    print("\n")
    print("Step 2/5 : aborting...")
    print("\n")
    time.sleep(5)
    print("This software will now exit...")
    time.sleep(2)
    sys.exit(1)

if __name__ == "__main__":
    orion()
