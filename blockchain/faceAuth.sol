// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FaceAuth {

    mapping(string => string) private userHash;

    event Registered(string email);
    event Verified(string email, bool success);

    function registerFace(string memory email, string memory _hash) public {
        userHash[email] = _hash;
        emit Registered(email);
    }

    function verifyFace(string memory email, string memory _hash) public view returns (bool) {
        return keccak256(abi.encodePacked(userHash[email])) == keccak256(abi.encodePacked(_hash));
    }

    function getHash(string memory email) public view returns (string memory) {
        return userHash[email];
    }
}
