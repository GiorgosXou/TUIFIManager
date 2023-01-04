import nox


@nox.session
def package_installation(session: nox.Session):
    session.install("-r", "requirements.txt")
    session.install(".")

    session.run("python", "-c", "import TUIFIManager")
