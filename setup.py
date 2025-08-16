from cx_Freeze import setup, Executable
import sys

# GUI 프로그램이 아니므로 base=None
base = None

build_options = {
    "packages": ["os", "argparse", "sys", "subprocess", "ctypes"],  # 필요한 표준 패키지들
    "excludes": [],
    "include_files": []  # 필요 시 추가
}

setup(
    name="Symbolic-ALL Tool",
    version="1.0",
    description="Symbolic link creator & remover",
    options={"build_exe": build_options},
    executables=[
        Executable("symbolic_all.py", base=base, target_name="symbolic_all.exe")
    ]
)
