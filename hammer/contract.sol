// SPDX-License-Identifier: MIT
pragma solidity ^ 0.5.16;

contract NFTContract {
    struct Land {
        address owner;
        uint256 farProposed;
        uint256 subLandNftId;
    }

    struct DRCInfo {
        bytes32 drcId;
        uint256 farAvailable;
        uint256 landCount;
        mapping(uint256 => Land) lands;
        address owner;
    }

    mapping(uint256 => DRCInfo) private _drcInfos;
    mapping(uint256 => string) private _tokenURIs;
    mapping(uint256 => address) private _tokenOwners;
    address private _contractOwner;
    uint256 private _tokenIdCounter;

    constructor() public {
        _contractOwner = msg.sender; // Set contract owner to the deployer
    }

    function mintDRC(
        bytes32 drcId,
        uint256 farAvailable,
        address owner,
        string memory tokenURI
    ) public {
        require(msg.sender == _contractOwner); // Only contract owner can mint DRC
        _tokenIdCounter += 1;

        DRCInfo storage drcInfo = _drcInfos[_tokenIdCounter];
        drcInfo.drcId = drcId;
        drcInfo.farAvailable = farAvailable;
        drcInfo.owner = owner;

        _tokenURIs[_tokenIdCounter] = tokenURI;
        _tokenOwners[_tokenIdCounter] = owner;
    }

    function mintLand(
        uint256 tokenId,
        address owner,
        uint256 farProposed,
        uint256 subLandNftId,
        string memory tokenURI
    ) public {
        require(msg.sender == _contractOwner); // Only contract owner can mint Land
        require(_tokenOwners[tokenId] != address(0)); // DRC does not exist

        DRCInfo storage drcInfo = _drcInfos[tokenId];
        drcInfo.lands[drcInfo.landCount] = Land(owner, farProposed, subLandNftId);
        drcInfo.landCount += 1;

        _tokenURIs[subLandNftId] = tokenURI;
        _tokenOwners[subLandNftId] = owner;
    }

    function getDRCInfo(uint256 tokenId)
        public
        view
        returns (
            bytes32,
            uint256,
            uint256,
            address
        )
    {
        require(_tokenOwners[tokenId] != address(0)); // DRC does not exist

        DRCInfo storage drcInfo = _drcInfos[tokenId];
        return (drcInfo.drcId, drcInfo.farAvailable, drcInfo.landCount, drcInfo.owner);
    }

    function getLandInfo(uint256 tokenId, uint256 landIndex)
        public
        view
        returns (
            address,
            uint256,
            uint256
        )
    {
        require(_tokenOwners[tokenId] != address(0)); // DRC does not exist

        DRCInfo storage drcInfo = _drcInfos[tokenId];
        Land storage land = drcInfo.lands[landIndex];
        return (land.owner, land.farProposed, land.subLandNftId);
    }
}
