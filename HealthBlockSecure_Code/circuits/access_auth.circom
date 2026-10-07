pragma circom 2.1.6;

template AccessAuth() {
    signal input credential_valid;
    signal input role_eligible;
    signal input consent_eligible;
    signal input not_expired;
    signal output eligible;
    credential_valid * (credential_valid - 1) === 0;
    role_eligible * (role_eligible - 1) === 0;
    consent_eligible * (consent_eligible - 1) === 0;
    not_expired * (not_expired - 1) === 0;
    eligible <== credential_valid * role_eligible * consent_eligible * not_expired;
}
component main {public [eligible]} = AccessAuth();
