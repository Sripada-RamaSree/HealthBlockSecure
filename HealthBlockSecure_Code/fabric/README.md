# Hyperledger Fabric integration

The manuscript specifies Fabric 2.x, two organisations, four peers, one CA per organisation, and a Raft ordering service. The supplied Go chaincode is deployable to a Fabric 2.x test network.

Recommended research setup:

1. Install Fabric samples/binaries matching your Fabric 2.x release.
2. Start a two-organisation channel with LevelDB.
3. Package `chaincode/healthblocksecure` as Go chaincode.
4. Install on both organisations and approve/commit using your endorsement policy.
5. Expose Fabric Gateway calls from the application service.

The Python standalone ledger preserves the same record/policy/consent/token/audit abstractions so experiments remain runnable without Fabric.
