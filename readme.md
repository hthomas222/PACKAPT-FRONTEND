# PACKAPT

PACKAPT is a web tool that allows the user to pull all of the packages for an Linux system and compares them to a list of packages you give it. The list will be in a file called packages.txt. Once you give it the list of packages, the website will allow you to update all the packages you give it or a single package. 

---

## Repository Structure

```text
PACKAPT/
├── app.py
├── computer_upgradable_packages.txt
├── docker-compose.yml
├── dockerfile
├── packages.txt
├── readme.md
├── requirements.txt
└── templates
    ├── index.html
    └── update.html
```