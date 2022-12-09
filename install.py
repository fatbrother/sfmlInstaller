import os
import requests
from zipfile import ZipFile

env = os.environ
mingwUrl = "https://github.com/fatbrother/mingw64/archive/refs/heads/main.zip"
sfmlUrl = "https://www.sfml-dev.org/files/SFML-2.5.1-windows-gcc-7.3.0-mingw-64-bit.zip"
c_cpp_properties = """
{
    "configurations": [
        {
            "name": "Win32",
            "includePath": [
                "${workspaceFolder}/**",
                "C:/mingw64/include/c++",
                "C:/SFML-2.5.1/include"
            ],
            "defines": [
                "_DEBUG",
                "UNICODE",
                "_UNICODE"
            ],
            "compilerPath": "C:/mingw64/bin/g++.exe",
            "cStandard": "gnu17",
            "cppStandard": "gnu++20",
            "intelliSenseMode": "windows-gcc-x64"
        }
    ],
    "version": 4
}
"""

tasks = """
{
    "version": "2.0.0",
    "tasks": [
        {
            "type": "cppbuild",
            "label": "C++: Building file",
            "command": "C:/mingw64/bin/g++.exe",
            "args": [
                "-g",
                "${fileDirname}/**.cpp",
                "-o",
                "${fileDirname}/${fileBasenameNoExtension}.exe",
                "-Wall",
                "-Wextra",
                "-Wpedantic",
                "-IC:/SFML-2.5.1/include",
                "-LC:/SFML-2.5.1/lib",
                "-lsfml-graphics",
                "-lsfml-audio",
                "-lsfml-window",
                "-lsfml-system",
            ],
            "options": {
                "cwd": "C:/Program Files/mingw64/bin"
            },
            "problemMatcher": [
                "$gcc"
            ],
            "group": "build",
            "detail": "Compiler: C:/mingw64/g++.exe"
        }
    ]
}
"""

testCode = """
#include <SFML/Graphics.hpp>

int main()
{
    sf::RenderWindow window(sf::VideoMode(200, 200), "SFML works!");
    sf::CircleShape shape(100.f);
    shape.setFillColor(sf::Color::Green);

    while (window.isOpen())
    {
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        window.clear();
        window.draw(shape);
        window.display();
    }

    return 0;
}
"""

dllList = [
    "C:\\SFML-2.5.1\\bin\\openal32.dll",
    "C:\\SFML-2.5.1\\bin\\sfml-audio-2.dll",
    "C:\\SFML-2.5.1\\bin\\sfml-graphics-2.dll",
    "C:\\SFML-2.5.1\\bin\\sfml-network-2.dll",
    "C:\\SFML-2.5.1\\bin\\sfml-system-2.dll",
    "C:\\SFML-2.5.1\\bin\\sfml-window-2.dll",
]

def install():
    # create .vscode folder
    if not os.path.exists(".vscode"):
        os.mkdir(".vscode")

    # download mingw64
    if not os.path.exists("mingw64.zip"):
        print("Downloading mingw64...")
        r = requests.get(mingwUrl)
        with open("mingw64.zip", "wb") as f:
            f.write(r.content)
        print("Downloaded mingw64.zip")

    # download sfml
    if not os.path.exists("SFML.zip"):
        print("Downloading SFML...")
        r = requests.get(sfmlUrl)
        with open("SFML.zip", "wb") as f:
            f.write(r.content)
        print("Downloaded SFML.zip")

    # unzip mingw64
    if not os.path.exists("C:/mingw64"):
        print("Unzipping mingw64.zip...")
        with ZipFile("mingw64.zip", "r") as zipObj:
            zipObj.extractall("mingw64")
        print("Unzipped mingw64.zip")

    # unzip sfml
    if not os.path.exists("C:/SFML-2.5.1"):
        print("Unzipping SFML.zip...")
        with ZipFile("SFML.zip", "r") as zipObj:
            zipObj.extractall()
        print("Unzipped SFML.zip")

    # move mingw64 to C:/
    if not os.path.exists("C:/mingw64"):
        print("Moving mingw64 to C:/...")
        os.system("move mingw64 C:/")
        print("Moved mingw64 to C:/")

    # move sfml to C:/
    if not os.path.exists("C:/SFML-2.5.1"):
        print("Moving SFML to C:/...")
        os.system("move SFML-2.5.1 C:/")
        print("Moved SFML to C:/")

def setup():
    print("Setting up...")
    # create c_cpp_properties.json
    with open(".vscode/c_cpp_properties.json", "w") as f:
        f.write(c_cpp_properties)
    # create tasks.json
    with open(".vscode/tasks.json", "w") as f:
        f.write(tasks)

    # copy dlls
    for dll in dllList:
        os.system("cp " + dll + " .")

    # create test.cpp
    with open("test.cpp", "w") as f:
        f.write(testCode)

if __name__ == "__main__":
    install()
    setup()
