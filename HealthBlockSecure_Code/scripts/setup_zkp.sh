#!/usr/bin/env bash
set -euo pipefail
mkdir -p circuits/build
circom circuits/access_auth.circom --r1cs --wasm --sym -o circuits/build
# Development-only Powers of Tau. For production use a trusted ceremony artifact.
snarkjs powersoftau new bn128 12 circuits/build/pot12_0000.ptau -v
snarkjs powersoftau contribute circuits/build/pot12_0000.ptau circuits/build/pot12_final.ptau --name="HealthBlockSecure dev" -e="healthblocksecure"
snarkjs groth16 setup circuits/build/access_auth.r1cs circuits/build/pot12_final.ptau circuits/build/access_auth_0000.zkey
snarkjs zkey contribute circuits/build/access_auth_0000.zkey circuits/build/access_auth_final.zkey --name="HealthBlockSecure dev" -e="healthblocksecure-zkey"
snarkjs zkey export verificationkey circuits/build/access_auth_final.zkey circuits/build/verification_key.json
cp circuits/build/access_auth_js/access_auth.wasm circuits/build/access_auth.wasm
echo "Groth16 artifacts created in circuits/build"
