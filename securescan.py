# import os
# import re
# import json
# import math
# import shutil
# import stat
# import subprocess
# from datetime import datetime

# REPO = "test_repository"


# def run(cmd, cwd=None):
#     return subprocess.run(
#         cmd,
#         cwd=cwd,
#         text=True,
#         capture_output=True,
#         check=True
#     ).stdout.strip()


# def git(*args, cwd=None):
#     return run(["git", *args], cwd)


# def entropy(s):
#     if not s:
#         return 0

#     probs = [s.count(c) / len(s) for c in set(s)]
#     return -sum(p * math.log2(p) for p in probs)


# def detect_secrets(text):
#     patterns = {
#         "API_KEY": r"CYBER137_API_[A-Za-z0-9_]+",
#         "PASSWORD": r"password\s*=\s*[\"'][^\"']+[\"']",
#         "TOKEN": r"CYBER137_TOKEN_[A-Za-z0-9_]+"
#     }

#     findings = []

#     for name, pattern in patterns.items():
#         for match in re.finditer(pattern, text, re.IGNORECASE):
#             value = match.group()

#             findings.append({
#                 "type": name,
#                 "value": value,
#                 "entropy": round(entropy(value), 2)
#             })

#     return findings


# def remove_readonly(func, path, exc):
#     os.chmod(path, stat.S_IWRITE)
#     func(path)


# def setup_demo_repo():
#     if os.path.exists(REPO):
#         shutil.rmtree(REPO, onexc=remove_readonly)

#     os.makedirs(REPO)

#     git("init", cwd=REPO)
#     git("config", "user.name", "CYBER-137 Demo", cwd=REPO)
#     git("config", "user.email", "demo@cyber137.local", cwd=REPO)

#     # Commit 1
#     with open(os.path.join(REPO, "app.py"), "w") as f:
#         f.write("print('Initial application')\n")

#     git("add", ".", cwd=REPO)
#     git("commit", "-m", "Initial application", cwd=REPO)

#     # Commit 2 - secret introduced
#     with open(os.path.join(REPO, "config.py"), "w") as f:
#         f.write(
#             'API_KEY = "CYBER137_API_VALID_DEMO_8F73K91X"\n'
#             'print("Application configuration")\n'
#         )

#     git("add", ".", cwd=REPO)
#     git("commit", "-m", "Add configuration", cwd=REPO)

#     # Commit 3 - secret removed
#     os.remove(os.path.join(REPO, "config.py"))

#     git("add", ".", cwd=REPO)
#     git("commit", "-m", "Remove exposed credential", cwd=REPO)

#     # Commit 4 - normal development
#     with open(os.path.join(REPO, "app.py"), "a") as f:
#         f.write("print('Normal development change')\n")

#     git("add", ".", cwd=REPO)
#     git("commit", "-m", "Normal development", cwd=REPO)

#     print("\nDemo repository created successfully.")


# def scan_repository():
#     print("\nScanning Git history...\n")

#     commits = git(
#         "log",
#         "--all",
#         "--pretty=format:%H",
#         cwd=REPO
#     ).splitlines()

#     findings = []

#     for commit in commits:

#         files = git(
#             "ls-tree",
#             "-r",
#             "--name-only",
#             commit,
#             cwd=REPO
#         ).splitlines()

#         for file in files:

#             try:
#                 content = git(
#                     "show",
#                     f"{commit}:{file}",
#                     cwd=REPO
#                 )
#             except subprocess.CalledProcessError:
#                 continue

#             secrets = detect_secrets(content)

#             for secret in secrets:

#                 findings.append({
#                     "commit": commit[:8],
#                     "file": file,
#                     "type": secret["type"],
#                     "secret": secret["value"],
#                     "entropy": secret["entropy"],
#                     "status": "DETECTED"
#                 })

#     return findings


# def validate_credentials(findings):
#     print("\nValidating detected credentials...\n")

#     for finding in findings:

#         if "VALID" in finding["secret"]:
#             finding["validation"] = "VALID"
#         else:
#             finding["validation"] = "INVALID"

#     return findings


# def rotate_credentials(findings):
#     print("Running rotation simulation...\n")

#     for finding in findings:

#         if finding["validation"] == "VALID":

#             finding["rotation"] = "COMPLETED"

#             finding["replacement"] = (
#                 "CYBER137_ROTATED_" + finding["commit"]
#             )

#         else:

#             finding["rotation"] = "NOT_REQUIRED"
#             finding["replacement"] = None

#     return findings


# def verify_rotation(findings):
#     print("Verifying remediation...\n")

#     for finding in findings:

#         if finding["rotation"] == "COMPLETED":
#             finding["verification"] = "PASSED"
#         else:
#             finding["verification"] = "NOT_REQUIRED"

#     return findings


# def generate_report(findings):

#     commits = git(
#         "log",
#         "--all",
#         "--pretty=format:%H",
#         cwd=REPO
#     ).splitlines()

#     report = {
#         "project": "CYBER-137",
#         "generated_at": datetime.now().isoformat(),
#         "repository": REPO,
#         "commits_scanned": len(commits),
#         "findings_count": len(findings),
#         "findings": findings
#     }

#     with open("report.json", "w") as f:
#         json.dump(report, f, indent=4)

#     print("\nEvidence report generated: report.json")


# def main():

#     print("=" * 60)
#     print("CYBER-137 - SECRET DETECTION PROTOTYPE")
#     print("=" * 60)

#     setup_demo_repo()

#     findings = scan_repository()

#     print(f"Secrets detected: {len(findings)}")

#     findings = validate_credentials(findings)

#     findings = rotate_credentials(findings)

#     findings = verify_rotation(findings)

#     print("\nDETAILED FINDINGS")
#     print("=" * 60)

#     for i, finding in enumerate(findings, 1):

#         print(f"\nFinding #{i}")
#         print("-" * 40)

#         print(f"Type          : {finding['type']}")
#         print(f"Commit        : {finding['commit']}")
#         print(f"File          : {finding['file']}")
#         print(f"Entropy       : {finding['entropy']}")
#         print(f"Validation    : {finding['validation']}")
#         print(f"Rotation      : {finding['rotation']}")
#         print(f"Verification  : {finding['verification']}")

#     generate_report(findings)


# if __name__ == "__main__":
#     main()

#-------------------------------------------------------------------

import os
import re
import json
import math
import shutil
import stat
import hashlib
import subprocess
from datetime import datetime


REPO = "test_repository"
REPORT = "report.json"


def run(cmd, cwd=None):
    return subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=True
    ).stdout.strip()


def git(*args, cwd=None):
    return run(["git", *args], cwd)


def entropy(s):
    if not s:
        return 0

    probs = [s.count(c) / len(s) for c in set(s)]

    return -sum(
        p * math.log2(p)
        for p in probs
    )


def fingerprint(value):
    return hashlib.sha256(
        value.encode()
    ).hexdigest()


def mask_secret(value):
    if len(value) <= 10:
        return "*" * len(value)

    return (
        value[:6]
        + "*" * (len(value) - 10)
        + value[-4:]
    )


def detect_secrets(text):

    patterns = {
        "API_KEY": r"CYBER137_API_[A-Za-z0-9_]+",
        "TOKEN": r"CYBER137_TOKEN_[A-Za-z0-9_]+",
        "PASSWORD": r"password\s*=\s*[\"']([^\"']+)[\"']"
    }

    findings = []

    for name, pattern in patterns.items():

        for match in re.finditer(
            pattern,
            text,
            re.IGNORECASE
        ):

            if name == "PASSWORD":
                value = match.group(1)
            else:
                value = match.group()

            findings.append({
                "type": name,
                "value": value,
                "entropy": round(
                    entropy(value),
                    2
                )
            })

    return findings


def remove_readonly(func, path, exc):
    os.chmod(
        path,
        stat.S_IWRITE
    )
    func(path)


def setup_demo_repo():

    if os.path.exists(REPO):
        shutil.rmtree(
            REPO,
            onexc=remove_readonly
        )

    os.makedirs(REPO)

    git(
        "init",
        cwd=REPO
    )

    git(
        "config",
        "user.name",
        "CYBER-137 Demo",
        cwd=REPO
    )

    git(
        "config",
        "user.email",
        "demo@cyber137.local",
        cwd=REPO
    )

    # Commit 1
    with open(
        os.path.join(REPO, "app.py"),
        "w"
    ) as f:

        f.write(
            "print('Initial application')\n"
        )

    git(
        "add",
        ".",
        cwd=REPO
    )

    git(
        "commit",
        "-m",
        "Initial application",
        cwd=REPO
    )

    # Commit 2 - secrets introduced
    with open(
        os.path.join(REPO, "config.py"),
        "w"
    ) as f:

        f.write(
            'API_KEY = "CYBER137_API_VALID_DEMO_8F73K91X"\n'
            'TOKEN = "CYBER137_TOKEN_INVALID_DEMO_12345"\n'
            'password = "CYBER137_VALID_PASSWORD_123"\n'
        )

    git(
        "add",
        ".",
        cwd=REPO
    )

    git(
        "commit",
        "-m",
        "Add configuration with credentials",
        cwd=REPO
    )

    # Commit 3 - secrets removed
    os.remove(
        os.path.join(
            REPO,
            "config.py"
        )
    )

    git(
        "add",
        ".",
        cwd=REPO
    )

    git(
        "commit",
        "-m",
        "Remove exposed credentials",
        cwd=REPO
    )

    # Commit 4 - normal development
    with open(
        os.path.join(REPO, "app.py"),
        "a"
    ) as f:

        f.write(
            "print('Normal development change')\n"
        )

    git(
        "add",
        ".",
        cwd=REPO
    )

    git(
        "commit",
        "-m",
        "Normal development",
        cwd=REPO
    )

    print(
        "\n[+] Demo repository created successfully."
    )


def scan_repository():

    print(
        "\n[*] Scanning complete Git history...\n"
    )

    commits = git(
        "log",
        "--all",
        "--pretty=format:%H",
        cwd=REPO
    ).splitlines()

    findings = []

    for commit in commits:

        files = git(
            "ls-tree",
            "-r",
            "--name-only",
            commit,
            cwd=REPO
        ).splitlines()

        for file in files:

            try:

                content = git(
                    "show",
                    f"{commit}:{file}",
                    cwd=REPO
                )

            except subprocess.CalledProcessError:

                continue

            secrets = detect_secrets(
                content
            )

            for secret in secrets:

                value = secret["value"]

                finding = {

                    "evidence_id":
                        "CYBER-" +
                        hashlib.sha256(
                            (
                                commit +
                                file +
                                value
                            ).encode()
                        ).hexdigest()[:10].upper(),

                    "commit":
                        commit[:8],

                    "file":
                        file,

                    "type":
                        secret["type"],

                    "masked_secret":
                        mask_secret(value),

                    "fingerprint":
                        fingerprint(value),

                    "entropy":
                        secret["entropy"],

                    "status":
                        "DETECTED",

                    "severity":
                        "HIGH",

                    # Internal value.
                    # This will NOT be written to report.json.
                    "_value":
                        value
                }

                findings.append(
                    finding
                )

    return findings


def validate_credentials(findings):

    print(
        "[*] Validating detected credentials...\n"
    )

    for finding in findings:

        value = finding["_value"]

        if "INVALID" in value:

            finding["validation"] = "INVALID"

        else:

            finding["validation"] = "VALID"

    return findings


def rotate_credentials(findings):

    print(
        "[*] Running rotation simulation...\n"
    )

    for finding in findings:

        if finding["validation"] == "VALID":

            finding["rotation"] = "COMPLETED"

            finding["replacement"] = (
                "CYBER137_ROTATED_"
                + finding["commit"]
            )

        else:

            finding["rotation"] = "NOT_REQUIRED"

            finding["replacement"] = None

    return findings


def verify_rotation(findings):

    print(
        "[*] Verifying remediation...\n"
    )

    for finding in findings:

        if finding["rotation"] == "COMPLETED":

            finding["verification"] = "PASSED"

        elif finding["validation"] == "INVALID":

            finding["verification"] = "NOT_REQUIRED"

        else:

            finding["verification"] = "FAILED"

    return findings


def generate_report(findings):

    commits = git(
        "log",
        "--all",
        "--pretty=format:%H",
        cwd=REPO
    ).splitlines()

    valid = sum(
        1
        for f in findings
        if f["validation"] == "VALID"
    )

    invalid = sum(
        1
        for f in findings
        if f["validation"] == "INVALID"
    )

    rotated = sum(
        1
        for f in findings
        if f["rotation"] == "COMPLETED"
    )

    verified = sum(
        1
        for f in findings
        if f["verification"] == "PASSED"
    )

    safe_findings = []

    for finding in findings:

        safe_finding = {
            key: value
            for key, value in finding.items()
            if key != "_value"
        }

        safe_findings.append(
            safe_finding
        )

    report = {

        "project":
            "CYBER-137",

        "description":
            "Detecting Secrets Across Version "
            "Control History and Live Systems",

        "generated_at":
            datetime.now().isoformat(),

        "repository":
            REPO,

        "commits_scanned":
            len(commits),

        "findings_count":
            len(findings),

        "summary": {

            "valid_credentials":
                valid,

            "invalid_credentials":
                invalid,

            "rotations_completed":
                rotated,

            "verifications_passed":
                verified
        },

        "findings":
            safe_findings
    }

    with open(
        REPORT,
        "w"
    ) as f:

        json.dump(
            report,
            f,
            indent=4
        )

    print(
        f"[+] Evidence report generated: {REPORT}"
    )


def print_results(findings):

    print("\n")

    print("=" * 65)

    print(
        "CYBER-137 DETECTION RESULTS"
    )

    print("=" * 65)

    print(
        f"\nTotal historical secrets detected : "
        f"{len(findings)}"
    )

    for i, finding in enumerate(
        findings,
        1
    ):

        print(
            "\n" + "-" * 65
        )

        print(
            f"Finding #{i}"
        )

        print(
            "-" * 65
        )

        print(
            f"Evidence ID   : "
            f"{finding['evidence_id']}"
        )

        print(
            f"Secret Type   : "
            f"{finding['type']}"
        )

        print(
            f"Commit        : "
            f"{finding['commit']}"
        )

        print(
            f"File          : "
            f"{finding['file']}"
        )

        print(
            f"Severity      : "
            f"{finding['severity']}"
        )

        print(
            f"Masked Secret : "
            f"{finding['masked_secret']}"
        )

        print(
            f"Entropy       : "
            f"{finding['entropy']}"
        )

        print(
            f"Validation    : "
            f"{finding['validation']}"
        )

        print(
            f"Rotation      : "
            f"{finding['rotation']}"
        )

        print(
            f"Verification  : "
            f"{finding['verification']}"
        )

    print(
        "\n" + "=" * 65
    )

    valid = sum(
        1
        for f in findings
        if f["validation"] == "VALID"
    )

    invalid = sum(
        1
        for f in findings
        if f["validation"] == "INVALID"
    )

    rotated = sum(
        1
        for f in findings
        if f["rotation"] == "COMPLETED"
    )

    verified = sum(
        1
        for f in findings
        if f["verification"] == "PASSED"
    )

    print("SUMMARY")

    print("=" * 65)

    print(
        f"Historical secrets : "
        f"{len(findings)}"
    )

    print(
        f"Valid credentials  : "
        f"{valid}"
    )

    print(
        f"Invalid credentials: "
        f"{invalid}"
    )

    print(
        f"Rotations complete : "
        f"{rotated}"
    )

    print(
        f"Verification passed: "
        f"{verified}"
    )

    print(
        "=" * 65
    )


def main():

    print("\n")

    print("=" * 65)

    print("CYBER-137")

    print(
        "SECRET DETECTION AND "
        "REMEDIATION PROTOTYPE"
    )

    print("=" * 65)

    setup_demo_repo()

    findings = scan_repository()

    findings = validate_credentials(
        findings
    )

    findings = rotate_credentials(
        findings
    )

    findings = verify_rotation(
        findings
    )

    print_results(
        findings
    )

    generate_report(
        findings
    )

    print(
        "\n[+] CYBER-137 prototype execution completed."
    )


if __name__ == "__main__":
    main()