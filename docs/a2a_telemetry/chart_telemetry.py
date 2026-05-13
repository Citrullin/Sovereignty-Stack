import json
import sys

def parse_telemetry(file_path):
    print("=== Sovereignty Stack A2A Telemetry Flow ===")
    print(f"Parsing: {file_path}\n")
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if not line.strip(): continue
                data = json.loads(line)
                
                print(f"Commit Hash:   {data.get('commit_hash')}")
                print(f"Timestamp:     {data.get('timestamp')}")
                print(f"Target Intent: {data.get('target_feature')}")
                print(f"Trace Score:   {data.get('trace_score')} / 1.0")
                
                print("\nInformation Flow (GraphRAG Mappings):")
                for path in data.get('info_flow', []):
                    print(f"  -> {path}")
                    
                human = data.get('human_attestation', {})
                if human:
                    print("\n[!] HUMAN LIABILITY ATTESTATION [!]")
                    print(f"  QA Agent DID: {human.get('qa_did')}")
                    print(f"  Statement:    {human.get('statement')}")
                    print(f"  ZK Proof:     {human.get('signature')}")
                
                print("\n" + "="*45 + "\n")
    except FileNotFoundError:
        print("Telemetry log not found.")

if __name__ == "__main__":
    parse_telemetry("verification_history.jsonl")
