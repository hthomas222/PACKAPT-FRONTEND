from flask import Flask, render_template, request
import subprocess


app = Flask(__name__)


@app.route('/')
def main():
    return render_template("index.html")

@app.route("/package-compare/", methods=["POST"])
def packagecompare():
    if request.method == 'POST':
        if 'pull' in request.form:
            subprocess.call("apt list --upgradable > computer_upgradable_packages.txt" , shell=True)
            test = "Pull Complete"
            return render_template("index.html",test=test)
    return render_template("index.html")

@app.route("/package-compare/packages", methods=["POST"])
def packages():
    if request.method == 'POST':
        if 'result' in request.form:
            final_upgrade_list = []
            with open("packages.txt") as p:
                li = p.readlines()
            with open("computer_upgradable_packages.txt") as updatable:
                li_2 = updatable.readlines()
                package_list = []
                for i in li_2:
                    i = i.split("/")
                    package_list.append(i[0])
                clean_li = []
                for i in range(len(li)):
                    elements = li.pop()
                    elements = elements.strip()
                    clean_li.append(elements)
                for i in package_list:
                    if i in clean_li:
                        final_upgrade_list.append(i)
                return render_template("index.html",final=final_upgrade_list)
    return render_template("index.html")



@app.route("/update-package/")
def update():
    if request.method == 'POST':
        if 'all' in request.form:
            final_upgrade_list = []
            with open("packages.txt") as p:
                li = p.readlines()
            with open("computer_upgradable_packages.txt") as updatable:
                li_2 = updatable.readlines()
                package_list = []
                for i in li_2:
                    i = i.split("/")
                    package_list.append(i[0])
                clean_li = []
                for i in range(len(li)):
                    elements = li.pop()
                    elements = elements.strip()
                    clean_li.append(elements)
                for i in package_list:
                    if i in clean_li:
                        final_upgrade_list.append(i)
                for i in final_upgrade_list:
                    subprocess.call(f"apt-get install --only-upgrade {i}" , shell=True)
                test = "Updates Complete"
                return render_template("update.html", test=test)
    return render_template("update.html")

@app.route("/update-package/single")
def supdate():
    if request.method == 'POST':
        if 'single' in request.form:
            pack = request.form["spack"]
            final_upgrade_list = []
            with open("packages.txt") as p:
                li = p.readlines()
            with open("computer_upgradable_packages.txt") as updatable:
                li_2 = updatable.readlines()
            package_list = []
            for i in li_2:
                i = i.split("/")
                package_list.append(i[0])
            clean_li = []
            for i in range(len(li)):
                elements = li.pop()
                elements = elements.strip()
                clean_li.append(elements)
            for i in package_list:
                if i in clean_li:
                    final_upgrade_list.append(i)
            for i in final_upgrade_list:
                if pack in final_upgrade_list:
                    subprocess.call(f"apt-get install --only-upgrade {pack}" , shell=True)
            sin = "Single package updated"
            return render_template("update.html", sin=sin)
    return render_template("update.html")

if __name__ == '__main__':
    app.run(port=8080)
