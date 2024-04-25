import requests
import json
import hashlib

# To get problem data from the server
def get_problem_data(access_token):
    problem_url = f"https://hackattic.com/challenges/mini_miner/problem?access_token={access_token}"
    response = requests.get(problem_url)
    response.raise_for_status()  # Ensure the request was successful
    return response.json()

# To find a nonce that meets the given difficulty
def find_valid_nonce(block, difficulty):
    nonce = 0
    while True:

        block['nonce'] = nonce

        block_json = json.dumps(block, separators=(',',":"), sort_keys=True) # Serialize without whitespace, sorted keys

        hash_object = hashlib.sha256(block_json.encode('utf-8'))
        hash_hex = hash_object.hexdigest()

        # Convert to binary and check leading zero bits
        binary_hash = bin(int(hash_hex, 16))[2:].zfill(256)

        if binary_hash.startswith("0" * difficulty):
            return nonce
        
        nonce += 1

# To submit the valid nonce as the solution
def submit_solution(access_token, nonce):
    solution_url = f"https://hackattic.com/challenges/mini_miner/solve?access_token={access_token}"
    solution_data = {"nonce": nonce}
    response = requests.post(solution_url, json=solution_data)
    response.raise_for_status()  # Ensure the POST request was successful
    return response.json()


if __name__ == "__main__":
    access_token = "ad7fd36ba45e7b41"

    # Get the problem data
    problem_data = get_problem_data(access_token)
    block = problem_data['block']
    difficulty = problem_data['difficulty']

    nonce = find_valid_nonce(block, difficulty)

    # Submit the data
    solution_response = submit_solution(access_token, nonce)

    print("Solution submitted successfully:", solution_response)