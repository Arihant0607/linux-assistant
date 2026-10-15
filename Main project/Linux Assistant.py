import subprocess
from pathlib import Path
import os
import shutil

def main():
    print("👋 Hey! I'm meru \n What can i do for you?")
    
    while True:
        if parser(input("> ").strip().lower()) == False:
            break
        
def get_intent(line):
    opening = ["open", "launch", "start", "run"]
    closing = ["close", "quit", "exit", "stop", "kill"]
    listing = ["list" , "show" , "ls"]
    navigation = ["cd", "go", "enter", "navigate"]
    create = ["create", "make", "new", "generate", "add"]
    rename = ["rename", "ren", "retitle", "relabel"]
    copy = ["copy" , "duplicate" , "clone" ]
    miscellaneous = ["change"]

    words = line.split()
    for word in (words):
        if word in opening:
            return "open"
        elif word in closing:
            return "close"
        elif word in listing:
            return "list"
        elif word in navigation:
            return "navigate"
        elif word in create:
            return "create"
        elif word in rename:
            return "rename"
        elif word in copy:
            return "copy"

def parser(line):
    # Removes puctuations from given input -> if any
    punctuations = ["!", "@", "#", "&", "(", ")", ":", "`", ";", "|", "?"]
    for punctuation in punctuations:
        line = line.replace(punctuation, " ")
    # Removes common filler from givven input
    filler_words = [
        "a", "an", "the", "please", "kindly", "can", "you", "could", "would", "i", "want", "bro", "hey"
    ]
    formated_input = []
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
    
    intent = get_intent(line)


    if intent is None:
        print("command not found")
        return
    
    if intent == "open":
            try:
                _, app = line.split(" ", 1)
                if not app.strip():
                    print("please enter an app to open")
                else:
                    command("open", app)
            except ValueError:
                print("can't open")
                pass
    elif intent == "close":
            try:
                _ , app = line.split(" ", 1)
                if not app.strip():
                    print("please enter an app to close")
                else:
                    command("close" , app)
            except ValueError:
                print("can't close")
                pass
    elif intent == "list":
            l = []
            remove_filler = ["file" , "files" , "in"]
            for _ in line.split():
                if _ not in remove_filler:
                    l.append(_) 
            try:
                command("list" , l[1])
            except IndexError:
                command("list")
                pass
    elif intent == "navigate":
            if "to" in line.split():
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
    elif intent == "create":
            directory_words = ["directory","dir", "folder"]
            plural = ["directories" , "folders"]
            
            if "in" in line.split():
                name , dest = line.rsplit("in", 1 )
                if not dest.strip():
                    print("please provide destination")
                else :
                    for _ in name.split():
                        if _ in directory_words:
                            _, name1 = name.split(_ , 1)
                            command("create", name1, "folder" , dest)
                        elif _ == "file":
                            _, name1 = name.split(_ , 1)
                            command("create" , name1 , "file" , dest)

            elif "in" not in line.split():
                for _ in line.split():
                    if _ in directory_words :
                        _ , name = line.split(_)
                        if not name.strip():
                            print("please enter folder name")
                        else:
                            command("create" , name , "folder" , "")
                    elif _ == "file":
                        _ , name = line.split(_)
                        if not name.strip():
                            print("please enter file name")
                        else:
                            command("create" , name , "file" , "" )
    elif intent == "rename":
            directory_words = ["directory", "dir", "folder"]
            
            if "to" in line.split():
                phrase , new_name = line.rsplit("to" , 1)

                if not new_name.strip():
                    print("please provide a name to change")
                else:
                    for _ in phrase.split():
                        if _ in directory_words:
                            _ , old_name = phrase.split(_ ,1)
                            if not old_name.strip():
                                print("please provide a file/folder to rename")
                            command("rename" , old_name , new_name)
                            break
                        elif "file" == _ :
                            _ , old_name = phrase.split(_ ,1)
                            if not old_name.strip():
                                print("please provide a file/folder to rename")
                            command("rename" , old_name , new_name)
                            break
                    else:
                        try:
                            old_name = phrase.split()[1]
                            command("rename", old_name, new_name)
                        except IndexError:
                            print("please provide a file/folder to rename")
                            pass                      
    elif intent == "copy":
            source_words = ["of" , "from"]
            destination_words = ["to" , "into" , "in" , "inside"]

            for _ in line.split():
                if _ in source_words:
                    src = line.split(_)[1].strip()
                    for sep in src.split():
                        if sep in destination_words:
                            src , dst = src.split(sep)
                            if not src.split():
                                print("source file is not provided")
                            elif not dst.split():
                                print("destination is not provided")
                            else:
                                command("copy" ,src , dst)
                else:
                    if _ in destination_words:
                        src , dst = line.split(_)
                        if not src.strip():
                            print("source file is not provided")
                        elif not dst.split():
                            print("destination is not provided")
                        else:
                            command("copy", src, dst)

def command(intent , target = None , work = None , kind = None):
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
        case "create":
            create(target , work , kind)
        case "rename":
            rename(target , work)
        case "copy":
            copy(target , work)
  

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

def create(name , kind , dst ):
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
    dst = directories.get(dst.strip(), dst.strip())
    target = Path(name.strip())
    
    if not dst:
        try:
            if kind == "file" :
                if target.exists() and target.is_file():
                    print(f"file {name.strip()} exists")
                    return
                else:
                    target.touch()
                    print(f"created {name.strip()} at {Path().cwd()}")
            
            elif kind == "folder":
                if target.exists() and target.is_dir():
                    print(f"folder {name.strip()} exists")
                    return
                else:
                    target.mkdir()
                    print(f"created {name.strip()} at {Path().cwd()}")
        except PermissionError:
            print("I don't have permission to do that")
            pass
    
    elif "/" in dst:
        p = Path(correct_path(dst))
        if p.exists() and p.is_dir():
            q = p / name.strip()
            if q.exists():
                if q.is_dir():
                    print(f"folder with {name.strip()} already exists")
                elif q.is_file():
                    print(f"file with {name.strip()} already exists")
            else:
                try:
                    if kind == "file":
                        q.touch()
                        print(f"created file {name.strip()} at {p}")
                    
                    elif kind == "folder":
                        q.mkdir()
                        print(f"created folder {name.strip()} at {p}")
                except PermissionError:
                    print(f"I don't have permission to access {p}")
                    pass
        else:
            print(f"{dst} does not exists")
    else:
        p = Path("/") / dst

        if p.is_dir():
            q = p / name.strip()
            if q.exists():
                if q.is_file():
                    print("file already Exists")
                elif q.is_dir():
                    print(f"folder with {name} exists")
            else:
                try:
                    if kind == "file":
                        q.touch()
                        print(f"created file {name.strip()} at {p}")

                    elif kind =="folder":
                        q.mkdir()
                        print(f"created folder {name.strip()} at {p}")
                except PermissionError:
                    print(f"I don't have permission to access {p}")
                    pass
        else:
            p = Path().home() / dst.strip()
            q = p / name.strip()
            if q.exists():
                if q.is_file():
                    print("file already Exists")
                elif q.is_dir():
                    print(f"folder with {name} exists")
            else:
                try:
                    if kind == "file":
                        q.touch()
                        print(f"created file {name.strip()} at {p}")
                    elif kind == "folder":
                        q.mkdir()
                        print(f"created folder {name.strip()} at {p}")
                except PermissionError:
                    print(f"I don't have permission to access {p}")
                    pass

def rename(old_name , new_name):
    old_name = old_name.strip()
    new_name = new_name.strip()
    p = Path(old_name)
    target = Path(new_name)
    if target.exists():
        if target.is_dir():
            print(f"A folder {new_name} exists")
        else:
            print(f"A file {new_name} exists")
    else:
        if p.exists():
            if  p.is_dir():
                try:
                    p.rename(target)
                    print(f"{old_name} Folder renamed to {new_name}")
                except PermissionError:
                    print("I don't have permission to do that")
                    pass
            elif p.is_file():
                try:
                    p.rename(target)
                    print(f"{old_name} file renamed to {new_name}")
                except PermissionError:
                    print("I don't have permission to do that")
                    pass
        else:
            print(f"No file/folder with {old_name} name exists")

def copy(src ,dst):
    src = src.strip()
    dst = dst.strip()

    if src.exists():
        if src.is_dir():
            print("source should be a file")
        elif src.is_file():
            print()


if __name__ == "__main__":
    main()