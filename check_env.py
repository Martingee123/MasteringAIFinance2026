"""Read the lab's two settings from .env beside this script."""

from pathlib import Path


def main():
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.is_file():
        raise SystemExit("Missing .env. Create it beside check_env.py.")

    settings = {}
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, separator, value = line.partition("=")
        if not separator:
            raise SystemExit("Invalid .env line. Use NAME=value.")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        settings[name.strip()] = value

    for name in ("API_KEY", "SEC_USER_AGENT"):
        if not settings.get(name):
            raise SystemExit(f"Missing or empty {name} in .env.")

    print(settings["API_KEY"][:4] + "...")
    print(settings["SEC_USER_AGENT"])


if __name__ == "__main__":
    main()
