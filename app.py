from typing import IO, List, Tuple, Callable

import requests
import random
import tkinter as tk
import tkinter.filedialog as tkf

from bs4 import BeautifulSoup
from PIL import ImageTk, Image
from io import BytesIO


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Screenshot Loader')

        self.v_width: int = 1280
        self.v_height: int = 720

        # Image viewer
        self.viewer: tk.Canvas = tk.Canvas(
            background='#000000', width=self.v_width, height=self.v_height)
        self.viewer.grid(row=0, columnspan=2)

        # Refersh button
        self.btn_refresh: tk.Button = tk.Button(self, text='REFRESH')
        self.btn_refresh.grid(row=1, column=0)
        self.btn_refresh.bind('<ButtonRelease-1>', self.set_iamge)

        # Refersh button
        self.btn_save: tk.Button = tk.Button(self, text='SAVE')
        self.btn_save.grid(row=1, column=1)
        self.btn_save.bind('<ButtonRelease-1>', self.save_image)

        self.loaded_image: Image = None
        self.loaded_image_code: str = ''

        # Cache
        self.__image_disp: ImageTk = None

    def get_image_url(self, code: str) -> str:
        # Open page
        page: requests.Response = requests.get(
            f'https://prnt.sc/{code}', headers={'User-Agent': 'Chrome'})
        if page.status_code != 200:
            print(f'Page failed to load: {page.status_code}!')
            return None

        # Extract image URL
        soup: BeautifulSoup = BeautifulSoup(page.content, 'html.parser')
        image_elm = soup.find('img', id='screenshot-image')
        if image_elm is None:
            print('Couldn\'t find image DOM element!')
            return None
        return image_elm['src']

    def save_image(self, event: tk.Event) -> None:
        if self.loaded_image is not None:
            save_types: List[Tuple[str, str]] = [
                ('PNG (*.png)', '*.png'),
                ('JPEG (*.jpg;*.jpeg;*.jpe;*.jfif)', '*.jpg'),
                ('All Files (*.*)', '*.*'),
            ]
            file_to_save: IO = tkf.asksaveasfile(
                mode='w', initialfile=f'image_{self.loaded_image_code}', filetypes=save_types, defaultextension=save_types[0][1])
            if file_to_save is None:
                return
            self.loaded_image.save(file_to_save.name)
            print(f'Image saved to file \'{file_to_save.name}\'')

    def set_iamge(self, event: tk.Event) -> None:
        # Get image URL
        rand_char: Callable[[], str] = lambda: chr(random.randint(97, 122))
        rand_int: Callable[[], int] = lambda: str(random.randint(0, 9))
        self.loaded_image_code: str = rand_char() + rand_char() + rand_int() + \
            rand_int() + rand_int() + rand_int()
        image_url: str = self.get_image_url(self.loaded_image_code)
        if image_url is None:
            return

        # Load image
        image_response: requests.Response = requests.get(
            image_url, allow_redirects=True, headers={'User-Agent': 'Chrome'})
        if image_response.status_code != 200:
            print(
                f'Image {self.loaded_image_code} failed to load: {image_response.status_code}!')
            return

        # Extract image data
        image_data: bytes = image_response.content
        self.loaded_image: Image = Image.open(BytesIO(image_data))

        # Resize image
        im_width, im_height = self.loaded_image.size
        if im_width > im_height:
            resized_image = self.loaded_image.resize(
                (self.v_width, int(im_height * (self.v_width / im_width))))
            offset: Tuple[int, int] = (0, (self.v_height - im_height) / 2)
        else:
            resized_image = self.loaded_image.resize(
                (int(im_width * (self.v_height / im_height)), self.v_height))
            offset: Tuple[int, int] = ((self.v_width - im_width) / 2, 0)

        # Display image
        self.__image_disp: ImageTk.PhotoImage = ImageTk.PhotoImage(
            resized_image)
        self.viewer.delete('all')
        self.viewer.create_image(offset, image=self.__image_disp, anchor="nw")
        print(f'Image {self.loaded_image_code} loaded!')
        self.title(f'Screenshot {self.loaded_image_code} Loaded!')
        self.viewer.update()


def main():
    app: App = App()
    app.mainloop()


if __name__ == '__main__':
    main()
