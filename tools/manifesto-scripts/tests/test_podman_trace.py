import subprocess
import os
import unittest
import time

class TestA2ATrace(unittest.TestCase):
    def setUp(self):
        self.repo_path = "/home/citrullin/git/sovereign_stack_vision"
        self.test_trace = "test_session_automated"
        self.output_file = f"{self.repo_path}/docs/a2a_telemetry/traces/{self.test_trace}.cast"
        
        # Cleanup
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_podman_trace_execution(self):
        """
        Test that podman_trace.sh can start a session and produce a .cast file.
        We mock the user input by passing commands to stdin if possible,
        or just checking if the process starts and creates the file.
        """
        # Run the podman script with a timeout to simulate a short session
        # We use 'script' to provide a TTY which asciinema requires
        cmd = ["bash", "tools/manifesto-scripts/podman_trace.sh", self.test_trace]
        
        print(f"Starting automated trace test: {' '.join(cmd)}")
        
        # We'll use a subprocess that we kill after a few seconds
        # Asciinema needs to run for a bit to initialize the file
        process = subprocess.Popen(
            cmd,
            cwd=self.repo_path,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        try:
            print("[DEBUG] Waiting for container to initialize and run asciinema...")
            # Capture output in real-time
            for i in range(15):
                line = process.stdout.readline()
                if line:
                    print(f"[CONTAINER] {line.strip()}")
                time.sleep(1)
            
            print("[DEBUG] Sending 'exit' to terminate recording session.")
            process.communicate(input="exit\n", timeout=10)
        except subprocess.TimeoutExpired:
            print("[WARNING] Process timed out, forcing kill.")
            process.kill()
            process.wait()

        # Check if the file was created
        print(f"[DEBUG] Checking for output file: {self.output_file}")
        self.assertTrue(os.path.exists(self.output_file), f"Trace file {self.output_file} was not created.")
        
        # Check if file has asciinema header
        with open(self.output_file, 'r') as f:
            first_line = f.readline()
            self.assertIn('"version": 2', first_line)
            print("Trace file validated successfully.")

if __name__ == "__main__":
    unittest.main()
