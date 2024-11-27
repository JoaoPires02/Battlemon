import subprocess
from difflib import Differ
import battlemon

def run_test(cmd, t):
    t = str(t)
    with open("test-cases/"+t+".in", "r") as infile, open("test-cases/"+t+".out", "r") as outfile:
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

cmd = ["python", "battlemon.py", "n", "charizord.json", "nikachu.json"]
cmd2 = ["python", "battlemon.py", "n"]
cmd3 = ["python", "battlemon.py", "charizord.json", "nikachu.json"]

run_all_tests()

print("All tests passed.")
