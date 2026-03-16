import json
import argparse
import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", type=str)
    parser.add_argument("port", type=str)
    parser.add_argument("file", type=str)
    parser.add_argument("--substr", type=str, default="")
    parser.add_argument("--n", type=int, default=0)

    args = parser.parse_args()
    magicians = []
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    magicians.append(json.loads(line))
    except FileNotFoundError:
        return

    url = f"http://{args.host}:{args.port}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        students_data = response.json()
    except requests.RequestException:
        return

    results = {}

    for mag in magicians:
        mag_name = mag["magician"]
        mag_skill = mag["skill"]
        matched_students = []

        for stud in students_data:
            s_name, s_skill, s_level, s_char = stud

            if (
                s_skill == mag_skill
                and s_level >= args.n
                and args.substr in s_char
            ):
                matched_students.append(s_name)

        results[mag_name] = sorted(matched_students)

    for mag_name in sorted(results.keys()):
        students_str = ", ".join(results[mag_name])
        print(f"{mag_name}: {students_str}")


if __name__ == "__main__":
    main()
