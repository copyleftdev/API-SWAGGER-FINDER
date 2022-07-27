import requests
from colorama import init
from colorama import Fore, Style
import multiprocessing

init()

NUM_WORKERS = 20


class SwaggerDetectionUtil:
    def get_route_list(self):
        hosts = []
        doc_routes = []
        targets = []
        with open("lists/domains.txt", "r") as f:
            for line in f.readlines():
                hosts.append(line.replace("\n", ""))
        with open('lists/swagger.txt', 'r') as f:
            for line in f.readlines():
                doc_routes.append(line.replace("\n", ""))

        for h in hosts:
            for r in doc_routes:
                targets.append(f"https://{h}{r}")
        return targets


def check_host_for_swagger_doc_path(target):
    try:
        Style.RESET_ALL
        req = requests.get(f"{target}", verify=True)
        if "Swagger UI" in req.text:
            print(Fore.GREEN + f"Document Found at: {target}")
            with open("found.txt", "a+") as f:
                f.write(target + "\n")
        else:
            print(Fore.RED + f"Document Not Found at: {target}", flush=True)
            pass
    except Exception as e:
        print(e)


sw = SwaggerDetectionUtil()
routes = sw.get_route_list()

with multiprocessing.Pool(processes=NUM_WORKERS) as pool:
    results = pool.map_async(check_host_for_swagger_doc_path, routes)
    results.wait()
