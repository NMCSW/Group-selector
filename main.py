import flet as ft
import os
from settings import *
from datetime import datetime
import xml.etree.ElementTree as ET


class Vehicle:
    def __init__(self, name, modification_date, size, group=None):
        self.modification_date = modification_date
        self.name = name
        self.size = size
        self.data = None
        self.group = group


    def load_data(self):
        self.data = read_xml_file(self.name, glb.Directory)


    def unload_data(self):
        self.data = None


    def __repr__(self) -> str:
        return f"{self.name} | {self.modification_date} | {self.size}"


class Vehicles:
    def __init__(self):
        self.vehicles = []
        self.total_size = 0


    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)


    def add_vehicles(self, vehicles):
        self.vehicles.extend(vehicles)


    def remove_vehicle(self, vehicle):
        self.vehicles.remove(vehicle)


    def __str__(self) -> str:
        return str(self.vehicles)


class ConfigManager:
    def __init__(self, path):
        self.xml_file_path = path 
        self.tree = None
        self.root = None


    def load_from_file(self):
        try:
            self.tree = ET.parse(self.xml_file_path)
            self.root = self.tree.getroot()
        except Exception as e:
            print("Read exception", e)
            self.generate_xml()
            return


    def get_path(self):
        return self.root.find("paths").find("path_to_stormworks").get("value")


    def generate_xml(self):
        try:
            os.makedirs(f"{os.getenv('APPDATA')}\\xml_groups")
        except:
            pass
        try:
            with open(self.xml_file_path, 'w', encoding='utf-8') as f:
                pass
        except:
            pass
        self.root = ET.fromstring('<Settings name="Global">' + '\n\t<paths>'+ f'\n\t\t<path_to_stormworks value="{os.getenv('APPDATA')}\\Stormworks" />' + '\n\t</paths>' + '\n</Settings>')
        self.tree = ET.ElementTree(self.root)
        self.save_to_file()


    def save_to_file(self, file_path: str = None):
        if file_path is None:
            file_path = self.xml_file_path
        
        if file_path is None:
            raise ValueError("Не указан путь для сохранения файла")
    
        tree = ET.ElementTree(self.root)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)


class XmlGroupManager:
    def __init__(self, path):
        self.xml_file_path = path
        self.tree = None
        self.root = None



        


class Globals:
    Directory = None
    Vehicles = None
    ConfigManager = ConfigManager(f"{os.getenv('APPDATA')}\\xml_groups\\xml_groups.xml")


glb = Globals()

def read_xml_file(filename, directory):
    tree = ET.parse(os.path.join(directory, f"{filename}.xml"))
    root = tree.getroot()
    return root


def read_vehicles(directory):
    vehicles = Vehicles()
    total_size = 0
    for f in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, f)) and f.endswith(".xml"):
            stat = os.stat(os.path.join(directory, f))
            total_size += stat.st_size
            size_bytes = stat.st_size
            modification_time = stat.st_mtime
            vehicles.add_vehicle(Vehicle(f[:-4], datetime.fromtimestamp(modification_time).strftime("%d.%m.%Y"), size_bytes))

    vehicles.total_size = total_size
    return vehicles


def main(page: ft.Page):
    page.clean()
    page.title = APP_NAME
    page.window_width = 1920
    page.window_height = 1080


    def on_hover(e):
        if e.data == "true": e.control.opacity = 1
        else: e.control.opacity = 0.7
        e.control.update()


    vehicles = ft.GridView(
        height=900,
        width=1100,
        max_extent=420,
        #child_aspect_ratio=1.0,
        spacing=40,
    )
    
    for i in (glb.Vehicles.vehicles):
        path = f"{glb.Directory}\\data\\vehicles\\{i.name}.png"
        if not os.path.exists(path):
            path = "./template_vehicle.png"
        vehicles.controls.append(
            ft.Container(
                alignment=ft.alignment.center,
                opacity=0.7,
                on_hover=on_hover,
                content = ft.Container(
                    bgcolor="#0D0D0D",
                    width=300,
                    height=420,
                    alignment=ft.alignment.center,
                    border_radius=15,
                    content=ft.Container(
                        alignment=ft.alignment.center,
                        width = 200,
                        height = 420,
                        content = ft.Column(
                            alignment = ft.MainAxisAlignment.START,
                            horizontal_alignment = ft.alignment.center,
                            spacing = 10,
                            controls = [
                            
                            ft.Container(
                                alignment = ft.alignment.center,
                                image_src = path,
                                width = 200,
                                height = 200,
                                border_radius = 15,
                                image_fit = ft.ImageFit.CONTAIN,
                            ),
                            ft.Container(
                                alignment=ft.alignment.center,
                                bgcolor="#404040",
                                border_radius=15,
                                content=ft.Text(i.name, color="white", size=16, text_align="center"),
                            ),
                            ft.Container(
                                alignment=ft.alignment.center,
                                bgcolor="#404040",
                                border_radius=15,
                                content=ft.Text(i.modification_date, color="white", size=16, text_align="left"),
                            ),
                            ft.Container(
                                alignment=ft.alignment.center,
                                bgcolor="#404040",
                                border_radius=15,
                                content=ft.Text(f"{i.size/1024/1024:.2f} MB", color="white", size=16, text_align="left"),
                            ),
                            ft.Container(
                                alignment=ft.alignment.center,
                                bgcolor="#404040",
                                border_radius=15,
                                content=ft.Text(f"Group: {i.group}", color="white", size=16, text_align="left"),
                            )
                        ])
                    )
                )
            )
        )

    main_frame = ft.Container(
        expand=True,
        opacity=1,
        bgcolor="#212124",
        margin=ft.padding.only(left=20, top=20),
        adaptive=True,
        alignment=ft.alignment.top_center,
        content=ft.Column(
            horizontal_alignment=ft.alignment.center,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
            ft.Container(
                alignment=ft.alignment.center,
                opacity=1,
                content=vehicles,
            ),
            
            
            ft.Row(
                
                controls=[
                    ft.Text("Total size: ", color="grey", size=13),
                    ft.Text(f"{glb.Vehicles.total_size/1024/1024:.2f} MB", color="white", size=13),
                    ft.Text(glb.Directory, color="grey", size=13),
                    ft.Text(f"Total vehicles: {len(glb.Vehicles.vehicles)}", color="grey", size=13)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ])
    )


    page.add(main_frame)
    page.update()


if __name__ == "__main__":
    glb.ConfigManager.load_from_file()
    glb.Directory = glb.ConfigManager.get_path()
    glb.Vehicles = read_vehicles(glb.Directory+"\\data\\vehicles\\")
    #print(glb.Vehicles)

    ft.app(target=main)