import subprocess
from pathlib import Path
import os


def main():
    print("👋 Hey! I'm meru \n What can i do for you?")
    
    while True:
        if parser(input("> ").strip().lower()) == False:
            break
        
def parser(line):
    # Removes puctuations from given input -> if any 
    punctuations = ["!", "@", "#", "&", "(", ")", ":", "`", ";", "|" ,"?"]
    for punctuation in punctuations:
        line = line.replace(punctuation, " ")
    # Removes common filler from givven input
    filler_words = [
        "a", "an", "the", "please", "kindly", "can", "you", "could", "would", "i", "want", "to", "bro" , "hey"
    ]
    formated_input =[]
    line = line.split()

    for i in line:
        if i not in filler_words:
            formated_input.append(i)
    
    
    line = (" ").join(formated_input)
    
    if "and" in line:
        line1, line2 = line.split("and", 1)
        if parser(line1.strip()) == False:
            return False
        if parser(line2.strip()) == False:
            return False
        return

    if line == "exit" or line == "quit" or line == "stop":
        return False

    opening = ["open", "launch", "start", "run"]
    closing = ["close", "quit", "exit", "stop", "kill"]
    listing = ["list" , "show" , "ls"]
    navigation = ["cd", "go", "enter", "navigate"]
    create = ["create", "make", "new", "generate", "add"]
    rename = ["rename", "ren", "retitle", "relabel"]
    miscellaneous = ["change"]

    words = line.split()
    for i,word in enumerate(words):
        if word in opening:
            try:
                _, app = line.split(" " , 1)
                command("open" , app)
            except ValueError:
                print("can't open")
                pass
        elif word in closing:
            try:
                _ , app = line.split(" ", 1)
                command("close" , app)
            except ValueError:
                print("can't close")
                pass
        elif word in listing:
            l = []
            remove_filler = ["file" , "files" , "in"]
            for _ in words:
                if _ not in remove_filler:
                    l.append(_) 
            try:
                command("list" , l[1])
            except IndexError:
                command("list")
                pass
        elif word in navigation:
            if "to" in words:
                try:
                    _ , directory = line.split("to", 1)
                    command("cd", directory)
                except ValueError:
                    print("please provide a directory")
                    pass
            else:
                try:
                    _, directory = line.split(" ", 1)
                    command("cd", directory)
                except ValueError:
                    print("please provide a directory")
                    pass
        elif word in create:
            directory_words = ["directory","dir", "folder" , "mkdir"]
            plural = ["directories" , "folders"]
            
            if "in" in words:
                name , dest = line.rsplit("in", 1 )
                if not dest.strip():
                    print("please provide destination")
                else :
                    for _ in name.split():
                        if _ in directory_words:
                            _, name1 = name.split(_ , 1)
                            command("create_dir", name1, dest)
                        elif _ == "file":
                            _, name1 = name.split(_ , 1)
                            command("create_file" , name1 , dest)

            elif "in" not in words:
                for _ in words:
                    if _ in directory_words :
                        _ , name = line.split(_)
                        if not name.strip():
                            print("please enter folder name")
                        else:
                            command("create_dir" , name)
                    elif _ == "file":
                        _ , name = line.split(_)
                        if not name.strip():
                            print("please enter file name")
                        else:
                            command("create_file" , name)
        elif word in rename:
            directory_words = ["directory", "dir", "folder", "mkdir"]
            
            if "to" in words:
                phrase , new_name = line.rsplit("to" , 1)

                if not new_name.strip():
                    print("please provide a name to change")
                else:
                    for _ in phrase.split():
                        if _ in directory_words:
                            _ , old_name = phrase.split(_ ,1)
                            command("ren_dir" , old_name , new_name)
                        elif "file" == _ :
                            _ , old_name = phrase.split(_ ,1)
                            command("ren_file" , old_name , new_name)


def command(intent , target = "" , name = "" ):
    match intent:
        case _ if "dont" in intent:
            pass
        case "open":
            open_app(target)
        case "close":
            close_app(target)
        case "list":
            check_folder(target)
        case "cd":
            change_directory(target)
        case "create_dir":
            create_dir(target , name)
        case "create_file":
            create_file(target , name)
        case "ren_dir":
            ren_dir(target , name)
        case "ren_file":
            ren_file(target , name)

        
def open_app(app ):
    try:
        subprocess.Popen([app] , stdout= subprocess.DEVNULL , stderr = subprocess.DEVNULL)
        print(f"opening {app}")
    except PermissionError  :
        print(f"can't open {app}")
    except FileNotFoundError:
        print(f"{app} not exists")

def close_app(app):
    output =  subprocess.run(["kill" , app] ,capture_output= True, text= True)
    if output.returncode == 0:
        print(f"closing {app}")
    else:
        print(f"can't close {app}")
        
def check_folder(target):
    directories = {
        "document": "Documents",
        "documents": "Documents",
        "desktop": "Desktop",
        "download": "Downloads",
        "downloads": "Downloads",
        "picture": "Pictures",
        "pictures": "Pictures",
        "music": "Music",
        "video": "Videos",
        "videos": "Videos"
    }
    target = directories.get(target,target)
    
    if not target:
        subprocess.run(["ls"] )
    elif "/" in target:
        try:
            subprocess.run(["ls"] , cwd = target)
        except FileNotFoundError:
            print(f"can't list {target} please check the path")
            pass
    else:
        p = Path("/") / target
        if p.is_dir():
            try:
                subprocess.run(["ls"], cwd=p)
            except FileNotFoundError:
                print(f"can't list {target} please check directory name")
                pass
        else:
            p = Path().home() / target
            try:
                subprocess.run(["ls"], cwd=p)
            except FileNotFoundError:
                print(f"can't list {target} check the name")
                pass

def correct_path(target):   
    p = Path(target.strip()).expanduser()

    if p.exists():
        return p
    
    current = Path(p.anchor)

    for part in p.parts[1:]:
        if not current.is_dir():
            return p
        
        matches = [
            item for item in current.iterdir()
            if item.name.lower() == part.lower()
        ]

        if not matches:
            return p

        current = matches[0]

    
    return current

def change_directory(target):
    
    directories = {
        "~" : "/home/arihant",
        "document": "Documents",
        "documents": "Documents",
        "desktop": "Desktop",
        "download": "Downloads",
        "downloads": "Downloads",
        "picture": "Pictures",
        "pictures": "Pictures",
        "music": "Music",
        "video": "Videos",
        "videos": "Videos"
    }

    target = directories.get(target,target)

    if not target:
        print("please provide a directory")
    elif "/" in target:
        try:
            os.chdir(correct_path(target))
        except FileNotFoundError:
            print("No such directory exists")
            pass
        except PermissionError:
            print("I don't have permission to open that")
            pass

    else:
        p = Path("/") / target

        if p.is_dir():
            try:
                os.chdir(p)
            except FileNotFoundError:
                print("No such directory exists")
                pass
            except PermissionError:
                print("I don't have permission to open that")
                pass
        else:
            p = Path().expanduser() / target
            try:
                os.chdir(p)
            except FileNotFoundError:
                print("No such directory exists")
                pass
            except PermissionError:
                print("I don't have permission to open that")
                pass

def create_dir(name ,dest):
    directories = {
        "~": "/home/arihant",
        "document": "Documents",
        "documents": "Documents",
        "desktop": "Desktop",
        "download": "Downloads",
        "downloads": "Downloads",
        "picture": "Pictures",
        "pictures": "Pictures",
        "music": "Music",
        "video": "Videos",
        "videos": "Videos"
    }

    dest = directories.get(dest.strip(), dest.strip())

    
    if not dest:
        try:
            Path(name.strip()).mkdir()
            print(f"created a folder {name} at {Path().cwd()}")
        except FileExistsError:
            print(f"folder {name} already exists")
            pass
        except PermissionError:
            print(f"I don't have permission to access {dest}")
    elif "/" in dest.strip():
        p = Path(correct_path(dest))/name.strip()
        try:
            p.mkdir()
            print(f"created a folder {name} at {dest}")
        except FileExistsError:
            print(f"folder {name} already exists")
            pass
        except PermissionError:
            print(f"I don't have permission to access {dest}")
        
    else:
        p = Path("/") / dest

        if p.is_dir():
            q = p / name.strip()
            try:
                q.mkdir()
                print(f"created a folder {name} at {p}")
            except FileExistsError:
                print(f"folder {name} already exists at {p}")
                pass
            except PermissionError:
                print(f"I don't have permission to access {dest}")
        else:
            p = Path().home() / dest.strip()
            q = p / name.strip()
            try:
                q.mkdir()
                print(f"created a folder {name} at {p}")
            except FileExistsError:
                print(f"folder {name} already exists at {p}")
                pass
            except PermissionError:
                print(f"I don't have permission to access {dest}")
            
def create_file(name , dest):
    directories = {
        "~": "/home/arihant",
        "document": "Documents",
        "documents": "Documents",
        "desktop": "Desktop",
        "download": "Downloads",
        "downloads": "Downloads",
        "picture": "Pictures",
        "pictures": "Pictures",
        "music": "Music",
        "video": "Videos",
        "videos": "Videos"
    }

    dest = directories.get(dest.strip(), dest.strip())

    if not dest:
        try:
            if Path(name.strip()).exists(): 
                if Path(name.strip()).is_file():
                    print("file already Exists")
                elif Path(name.strip()).is_dir():
                    print(f"folder with {name} exists")
            else:
                Path(name.strip()).touch()
                print(f"created a file {name} at {Path().cwd()}")
            pass
        except PermissionError:
            print(f"I don't have permission to access {dest}")
    elif "/" in dest.strip():
        p = Path(correct_path(dest))
        if p.exists() and p.is_dir():
            try:
                q = p / name.strip()
                if q.exists(): 
                    if q.is_file():
                        print("file already Exists")
                    elif q.is_dir():
                        print(f"folder with {name} exists")
                else:
                    q.touch()
                    print(f"created a file {name} at {dest}")
            except PermissionError:
                print(f"I don't have permission to access {dest}")
        else:
            print(f"{dest} does not exists ")

    else:
        p = Path("/") / dest

        if p.is_dir():
            q = p / name.strip()
            try:
                if q.exists():
                    if q.is_file():
                        print("file already Exists")
                    elif q.is_dir():
                        print(f"folder with {name} exists")
                else:
                    q.touch()
                    print(f"created a file {name} at {p}")
            except PermissionError:
                print(f"I don't have permission to access {dest}")
        else:
            p = Path().home() / dest.strip()
            q = p / name.strip()
            try:
                if q.exists(): 
                    if q.is_file():
                        print("file already Exists")
                    elif q.is_dir():
                        print(f"folder with {name} exists")
                else:
                    q.touch()
                    print(f"created a file {name} at {p}")
            except PermissionError:
                print(f"I don't have permission to access {dest}")

def ren_dir(old_name , new_name):
    p = Path(old_name)
    if p.exists() and p.is_dir():
            target = Path(new_name)
            if target.exists():
                if target.is_dir():
                    print(f"A folder with {new_name} exists")
                else:
                    print(f"A file with {new_name} exists")
            else:
                try:
                    p.rename(target)
                    print(f"{old_name} Folder renamed to {new_name}")
                except PermissionError:
                    print("I don't have permission to do that")
                    pass
    else:
        print(f"No folder {old_name} exists")

def ren_file(old_name , new_name):
    p = Path(old_name)
    if p.exists() and p.is_file():
            target = Path(new_name)
            if target.exists():
                if target.is_dir():
                    print(f"A folder with {new_name} exists")
                else:
                    print(f"A file with {new_name} exists")
            else:
                try:
                    p.rename(target)
                    print(f"{old_name} Folder renamed to {new_name}")
                except PermissionError:
                    print("I don't have permission to do that")
                    pass
    else:
        print(f"No file {old_name} exists")


if __name__ == "__main__":
    main()