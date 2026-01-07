import json
import os
import subprocess
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(ROOT_DIR, "data.json")


def read_json():
    if not os.path.exists(DATA_PATH):
        return {"games": []}
    with open(DATA_PATH, "r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(payload):
    tmp_path = DATA_PATH + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    os.replace(tmp_path, DATA_PATH)


def run_git(args):
    return subprocess.run(
        ["git"] + args,
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/games":
            return self.handle_get_games()
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/save":
            return self.handle_save()
        if parsed.path == "/api/push":
            return self.handle_push()
        self.send_error(404, "Not found")

    def read_body_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return None

    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def handle_get_games(self):
        try:
            payload = read_json()
        except Exception as exc:
            return self.send_json(500, {"ok": False, "error": str(exc)})
        return self.send_json(200, payload)

    def handle_save(self):
        payload = self.read_body_json()
        if payload is None:
            return self.send_json(400, {"ok": False, "error": "Invalid JSON"})
        if not isinstance(payload, dict) or "games" not in payload or not isinstance(
            payload["games"], list
        ):
            return self.send_json(
                400,
                {
                    "ok": False,
                    "error": "Payload must be an object with a games array",
                },
            )
        try:
            write_json(payload)
        except Exception as exc:
            return self.send_json(500, {"ok": False, "error": str(exc)})
        return self.send_json(200, {"ok": True})

    def handle_push(self):
        payload = self.read_body_json()
        if payload is None:
            return self.send_json(400, {"ok": False, "error": "Invalid JSON"})
        message = ""
        if isinstance(payload, dict):
            message = str(payload.get("message") or "")
        message = message.strip().splitlines()[0] if message.strip() else "Update data"

        add_result = run_git(["add", "data.json"])
        if add_result.returncode != 0:
            return self.send_json(
                500,
                {
                    "ok": False,
                    "error": "git add failed",
                    "details": add_result.stderr or add_result.stdout,
                },
            )

        diff_result = run_git(["diff", "--cached", "--name-only", "--", "data.json"])
        if diff_result.returncode != 0:
            return self.send_json(
                500,
                {
                    "ok": False,
                    "error": "git diff failed",
                    "details": diff_result.stderr or diff_result.stdout,
                },
            )

        commit_output = ""
        if not diff_result.stdout.strip():
            return self.send_json(
                200,
                {
                    "ok": True,
                    "message": "No changes to push",
                },
            )

        commit_result = run_git(["commit", "-m", message, "--", "data.json"])
        commit_output = commit_result.stdout + commit_result.stderr
        if commit_result.returncode != 0:
            return self.send_json(
                500,
                {
                    "ok": False,
                    "error": "git commit failed",
                    "details": commit_output.strip(),
                },
            )

        pull_result = run_git(["pull", "--rebase"])
        if pull_result.returncode != 0:
            return self.send_json(
                500,
                {
                    "ok": False,
                    "error": "git pull --rebase failed",
                    "details": pull_result.stderr or pull_result.stdout,
                },
            )

        push_result = run_git(["push"])
        if push_result.returncode != 0:
            return self.send_json(
                500,
                {
                    "ok": False,
                    "error": "git push failed",
                    "details": push_result.stderr or push_result.stdout,
                },
            )

        status_result = run_git(["status", "-sb"])
        return self.send_json(
            200,
            {
                "ok": True,
                "message": "Push completed",
                "commit": commit_output.strip(),
                "pull": pull_result.stdout.strip(),
                "push": push_result.stdout.strip(),
                "status": status_result.stdout.strip(),
            },
        )


def main():
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Usage: python server.py [port]")
            sys.exit(1)

    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"Serving Quatuors on http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
