from flask import Flask, render_template, request, flash, redirect, url_for
import subprocess
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-me"          # needed for flash

PACKAGES_FILE = Path("packages.txt")
UPGRADABLE_FILE = Path("computer_upgradable_packages.txt")

def get_upgradable_packages() -> list[str]:
    """Return intersection of packages.txt and currently upgradable packages."""
    if not PACKAGES_FILE.exists() or not UPGRADABLE_FILE.exists():
        return []

    allowed = {line.strip() for line in PACKAGES_FILE.read_text().splitlines() if line.strip()}
    upgradable = set()
    for line in UPGRADABLE_FILE.read_text().splitlines():
        # apt list --upgradable lines look like: package/version ...
        name = line.split("/", 1)[0].strip()
        if name and name != "Listing...":
            upgradable.add(name)

    return sorted(allowed & upgradable)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/package-compare/", methods=["POST"])
def packagecompare():
    if "pull" in request.form:
        # safer: capture output ourselves instead of shell redirect
        result = subprocess.run(
            ["apt", "list", "--upgradable"],
            capture_output=True, text=True, check=False
        )
        UPGRADABLE_FILE.write_text(result.stdout)
        flash("Pull complete")
    return render_template("index.html")


@app.route("/package-compare/packages", methods=["POST"])
def packages():
    if "result" in request.form:
        final = get_upgradable_packages()
        return render_template("index.html", final=final)
    return render_template("index.html")


@app.route("/update-package/", methods=["GET", "POST"])
def update():
    if request.method == "POST" and "all" in request.form:
        packages = get_upgradable_packages()
        for pkg in packages:
            # NEVER shell=True; also consider a root helper instead
            subprocess.run(
                ["apt-get", "install", "--only-upgrade", "-y", pkg],
                check=False
            )
        flash("Updates complete")
        return render_template("update.html")
    return render_template("update.html")


@app.route("/update-package/single", methods=["POST"])
def supdate():
    pack = request.form.get("spack", "").strip()
    if not pack:
        flash("No package specified")
        return redirect(url_for("update"))

    allowed = get_upgradable_packages()
    if pack not in allowed:
        flash(f"{pack} is not in the allowed upgradable list")
        return redirect(url_for("update"))

    subprocess.run(
        ["apt-get", "install", "--only-upgrade", "-y", pack],
        check=False
    )
    flash(f"Single package {pack} updated")
    return render_template("update.html")


if __name__ == "__main__":
    app.run(port=8080, debug=True)   # debug=False in production