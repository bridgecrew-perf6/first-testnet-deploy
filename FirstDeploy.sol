// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Simple Smart Contract That Allows You To Change the Greeting Message
contract FirstDeploy {
    string public greet = "Hello World";

    // Return the value of greet
    function getGreet() public view returns (string memory) {
        return greet;
    }

    //Change the value of greet
    function changeGreet(string memory newGreet)
        public
        returns (string memory)
    {
        greet = newGreet;
        return greet;
    }
}
