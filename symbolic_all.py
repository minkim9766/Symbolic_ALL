import os
import argparse
import sys
import subprocess

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def normalize_path(path_str):
    path_str = os.path.expandvars(os.path.expanduser(path_str))
    if len(path_str) == 2 and path_str[1] == ":":
        path_str += "\\"
    return os.path.abspath(path_str)

def add_to_path(install_path):
    current_path = os.environ.get("PATH", "")
    if install_path.lower() in [p.lower() for p in current_path.split(";")]:
        print(f"[INFO] PATH already contains: {install_path}")
        return
    try:
        subprocess.run(
            ["setx", "PATH", f"{current_path};{install_path}"],
            shell=True,
            check=True
        )
        print(f"[SUCCESS] Added to PATH: {install_path}")
    except Exception as e:
        print(f"[ERROR] Failed to add to PATH: {e}")

def create_symlinks(src_dir, dst_dir):
    print(f"[INFO] Creating symbolic links from:\n  SRC: {src_dir}\n  DST: {dst_dir}")
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
        print(f"[INFO] Created target directory: {dst_dir}")

    for item in os.listdir(src_dir):
        src_item = os.path.join(src_dir, item)
        dst_item = os.path.join(dst_dir, item)

        if os.path.exists(dst_item):
            print(f"[SKIP] Already exists: {dst_item}")
            continue

        try:
            if os.path.isdir(src_item):
                os.symlink(src_item, dst_item, target_is_directory=True)
                print(f"[DIR LINK] {src_item} -> {dst_item}")
            else:
                os.symlink(src_item, dst_item)
                print(f"[FILE LINK] {src_item} -> {dst_item}")
        except OSError as e:
            print(f"[ERROR] Failed to link {src_item} -> {dst_item}: {e}")

def delete_symlinks(dst_dir):
    print(f"[INFO] Deleting symbolic links in: {dst_dir}")
    if not os.path.exists(dst_dir):
        print("[ERROR] Target directory does not exist.")
        return

    for item in os.listdir(dst_dir):
        target_item = os.path.join(dst_dir, item)
        try:
            if os.path.islink(target_item):
                os.unlink(target_item)
                print(f"[DELETED LINK] {target_item}")
        except OSError as e:
            print(f"[ERROR] Failed to delete {target_item}: {e}")

def main():
    print("=== Symbolic-ALL Tool ===")
    print(f"[INFO] Running as admin: {is_admin()}")

    parser = argparse.ArgumentParser(description="Symbolic link creator & remover")
    parser.add_argument("-path", type=str, default=os.getcwd(),
                        help="Source path (default: current directory)")
    parser.add_argument("-to", type=str, required=True,
                        help="Target path (where links will be created or deleted)")
    parser.add_argument("--addpath", action="store_true",
                        help="Add current exe directory to PATH")
    parser.add_argument("--delete", action="store_true",
                        help="Delete all symbolic links in the target path")

    args = parser.parse_args()

    src_dir = normalize_path(args.path)
    dst_dir = normalize_path(args.to)

    if args.addpath:
        exe_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
        add_to_path(exe_dir)

    if args.delete:
        confirm = input(f"[CONFIRM] Delete ALL symbolic links in '{dst_dir}'? (y/n): ").strip().lower()
        if confirm == 'y':
            delete_symlinks(dst_dir)
        else:
            print("[CANCELLED] No links were deleted.")
        return

    if not os.path.exists(src_dir):
        print(f"[ERROR] Source path does not exist: {src_dir}")
        sys.exit(1)

    if src_dir == dst_dir:
        print("[ERROR] Source and target paths cannot be the same.")
        sys.exit(1)

    create_symlinks(src_dir, dst_dir)

if __name__ == "__main__":
    main()
