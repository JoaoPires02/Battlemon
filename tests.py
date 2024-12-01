import subprocess
from difflib import Differ
import battlemon

def run_test(cmd, t):
    t = str(t)
    with open("test-cases/" + t + ".in", "r") as infile, open("test-cases/" + t + ".out", "r") as outfile:
        expected_output = outfile.read()

        result = subprocess.run(
            cmd,
            stdin=infile,
            capture_output=True,
            text=True
        )

        print(result.stderr)

        with open("test-results/"+t+"-gotten"+".out", "w") as output:
            output.write(result.stdout)

        assert result.stdout == expected_output

def run_all_tests():
    run_test(cmd, 1)
    run_test(cmd, 2)
    run_test(cmd2, 3)
    run_test(cmd2, 4)
    run_test(cmd2, 5)
    run_test(cmd2, 6)
    run_test(cmd2, 7)
    run_test(cmd2, 8)
    run_test(cmd, 9)
    run_test(cmd, 10)
    run_test(cmd3, 11)
    run_test(cmd, 12)
    run_test(cmd, 13)
    run_test(cmd, 14)
    run_test(cmd, 15)
    run_test(cmd4, 16)
    run_test(cmd5, 17)
    run_test(cmd4, 18)
    run_test(cmd6, 19)
    run_test(cmd7, 20)
    run_test(cmd8, 21)
    run_test(cmd10, 22)
    run_test(cmd10, 23)
    run_test(cmd10, 24)
    run_test(cmd13, 25)
    run_test(cmd11, 26)
    run_test(cmd12, 27)
    run_test(cmd12, 28)
    run_test(cmd8, 29)
    run_test(cmd9, 30)
    run_test(cmd, 31)
    run_test(cmd8, 32)
    run_test(cmd8, 33)
    run_test(cmd12, 34)
    run_test(cmd14, 35)
    run_test(cmd15, 36)


cmd = ["python", "battlemon.py", "n", "charizord.json", "nikachu.json"]
cmd2 = ["python", "battlemon.py", "n"]
cmd3 = ["python", "battlemon.py", "charizord.json", "nikachu.json"]
cmd4 = ["python", "battlemon.py", "n", "balastoise.json", "nikachu.json"]
cmd5 = ["python", "battlemon.py", "n", "charizord.json", "nikachu.json", "1"]
cmd6 = ["python", "battlemon.py", "n", "balastoise.json", "nikachu.json", "1"]
cmd7 = ["python", "battlemon.py", "n", "veinosaur.json", "nikachu.json"]
cmd8 = ["python", "battlemon.py", "n", "veinosaur.json", "charizord.json"]
cmd9 = ["python", "battlemon.py", "y", "veinosaur.json", "charizord.json"]
cmd10 = ["python", "battlemon.py", "n", "magikorp.json", "nikachu.json"]
cmd11 = ["python", "battlemon.py", "n", "nikachu.json", "magikorp.json"]
cmd12 = ["python", "battlemon.py", "n", "feeboss.json", "magikorp.json"]
cmd13 = ["python", "battlemon.py", "n", "magikorp.json", "feeboss.json"]
cmd14 = ["python", "battlemon.py", "n", "tymon.json", "magikorp.json"]
cmd15 = ["python", "battlemon.py", "n", "veinosaur.json", "momon.json"]

run_all_tests()

print("All tests passed.")
