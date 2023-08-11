import asyncio
import aiohttp
import re
import gi
import requests
from gi.repository import Gtk

gi.require_version("Gtk", "3.0")


class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Hello World")
        self.set_default_size(800, 600)
        self.box = Gtk.Box()
        self.add(self.box)
        """self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)"""

        self.goods_and_price = Gtk.ListStore(str, int)

        self.button_API = Gtk.Button(label="Загрузить из API")
        self.button_API.set_size_request(80, 80)
        self.button_API.connect("clicked", self.run_requests_API)
        self.box.pack_start(self.button_API, True, False, 0)

        self.button_file = Gtk.Button(label="Загрузить из файла")
        self.button_file.connect("clicked", self.on_button_clicked_file)
        self.box.pack_start(self.button_file, True, False, 0)


    def run_requests_API(self, widget):
        asyncio.run(self.async_request_API())

    @staticmethod
    async def async_request_API():
        API = ["https://paycon.su/api1.php", "https://paycon.su/api2.php"]

        async with aiohttp.ClientSession() as session:
            task = []
            for i in API:
                task.append(asyncio.create_task(session.get(i)))
            responses = await asyncio.gather(*task)
            result_response = "".join([await response.text() for response in responses])

        result_name = re.findall(r"name[^\r]+", result_response)
        result_price = re.findall(r"price[^\r]+", result_response)

        list_dict_name_price = {i[0][8:-2].replace('\\', ''): i[1][8:] for i in zip(result_name, result_price)}
        print(list_dict_name_price)


if __name__ == "__main__":
    main_window = MyWindow()
    main_window.connect("delete-event", Gtk.main_quit)
    main_window.show_all()
    Gtk.main()
