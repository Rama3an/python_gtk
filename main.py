import asyncio
import aiohttp
import re
import csv
import gi
from gi.repository import Gtk

gi.require_version("Gtk", "3.0")


class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Application")
        self.set_size_request(600, 800)
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        self.goods_and_price = Gtk.ListStore(str, str)

        # кнопки
        self.buttons = list()
        self.button_API = Gtk.Button(label="Загрузить из API")
        self.buttons.append(self.button_API)
        self.button_API.connect("clicked", self.run_requests_API)

        self.button_file = Gtk.Button(label="Загрузить из файла")
        self.buttons.append(self.button_file)
        self.button_file.connect("clicked", self.reading_with_file)

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.EXTERNAL)
        self.scrollable_treelist.set_vexpand(False)
        self.grid.attach(self.buttons[0], 0, 5, 1, 1)
        self.grid.attach(self.buttons[1], 1, 5, 1, 1)
        # столбцы
        self.treeview = Gtk.TreeView(model=self.goods_and_price)
        self.renderer_text_goods = Gtk.CellRendererText()
        self.column_text_goods = Gtk.TreeViewColumn("Goods", self.renderer_text_goods, text=0)
        self.treeview.append_column(self.column_text_goods)

        self.renderer_text_price = Gtk.CellRendererText()
        self.column_text_price = Gtk.TreeViewColumn("Price", self.renderer_text_price, text=1)
        self.treeview.append_column(self.column_text_price)

        self.scrollable_treelist.add(self.treeview)
        self.grid.attach(self.scrollable_treelist, 0, 0, 2, 5)

    def reading_with_file(self, widget):
        with open("test_base.csv", "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.goods_and_price.append([row["Title"], row["Price"]])

    def run_requests_API(self, widget):
        asyncio.run(self.async_request_API())

    async def async_request_API(self):

        API = ["https://paycon.su/api1.php", "https://paycon.su/api2.php"]

        async with aiohttp.ClientSession() as session:
            task = []
            for i in API:
                task.append(asyncio.create_task(session.get(i)))
            responses = await asyncio.gather(*task)
            result_response = "".join([await response.text() for response in responses])

        result_name = re.findall(r"name[^\r]+", result_response)
        result_price = re.findall(r"price[^\r]+", result_response)

        list_dict_name_price = [(i[0][8:-2].replace('\\', ''), i[1][8:]) for i in zip(result_name, result_price)]
        for row in list_dict_name_price:
            self.goods_and_price.append(row)


class DownlandWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Spinner")
        self.set_default_size(150, 100)
        self.set_border_width(3)
        self.spinner = Gtk.Spinner()
        self.add(self.spinner)
        self.show_all()
        self.connect("destroy", Gtk.main_quit)


if __name__ == "__main__":
    main_window = MainWindow()
    main_window.connect("destroy", Gtk.main_quit)
    main_window.show_all()
    Gtk.main()
