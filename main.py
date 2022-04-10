import asyncio
import locale
import math

import colorama
from colorama import Fore
from pytube import YouTube

# Used for better number formatting
locale.setlocale(locale.LC_ALL, "")

video_link = input(f"YouTube Link >> ")


def on_complete(stream, file_path):
    print("Download complete")
    print("File path:", file_path)


video_obj: YouTube = YouTube(video_link, on_complete_callback=on_complete)


def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n


async def print_info():
    print(Fore.RED + f"Title: {Fore.RESET}", video_obj.title)
    print(Fore.RED + f"Duration: {Fore.RESET}" +
          "{} minutes".format(truncate(video_obj.length / 60, 2)))
    print(Fore.RED + f"Views: {Fore.RESET}{video_obj.views:n}")


async def get_user_input(callback):
    """Gets user input\n
    ``Args:``\n \t\tcallback: callback to handle user input"""
    user_in = input("choice >> ")
    await callback(user_in)


async def download_video(res: int, error_callback: callable, *, audio_only=False):
    """Downloads a video\n
    ``Args``:
        \tres: resolution to download
        \terror_callback: callback to handle errors
        \taudio_only: if true, downloads audio only
    """
    if audio_only:
        video_obj.streams.get_audio_only().download()
    resulutions = [720, 480, 360, 240, 144]
    if res in resulutions:
        video_obj.streams.get_highest_resolution().download()
    else:
        error_callback("Invalid resolution")


async def handle_user_input(input: str):
    """Handles user input"""
    match input.lower():
        case "b":
            await download_video(720, handle_error)
        case "w":
            await download_video(144, handle_error)
        case "a":
            await download_video(144, handle_error, audio_only=True)
        case "e":
            print("Good Bye!")
            exit()


def handle_error(msg: str):
    """Handles error messages"""
    print(msg)


def mark(char, backed_color=Fore.BLUE, color=Fore.WHITE):
    """Marks a character with a color"""
    return "{}{}{}".format(color, char, backed_color)


async def main():
    """Main function"""
    # initialize colorama
    colorama.init()
    # prints info about the video
    await print_info()
    # asks user whats he wants to do
    print(f"{Fore.GREEN}download: {Fore.BLUE}({mark('b')})est quality, ({mark('w')})worst quality, ({mark('a')})udio only, {Fore.RED}({mark('e', Fore.RED)})xit{Fore.RESET}")
    # awaits user input and handles it
    await get_user_input(handle_user_input)


if __name__ == "__main__":
    # runs the main function asyncronously
    asyncio.run(main())
