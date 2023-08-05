"""
    test_17_asset_purchase

    As a developer working with an Ocean marketplace,
    I want to record a purchase.

"""

import secrets
import logging
import json

from starfish.asset import DataAsset


def test_17_asset_purchase(ocean, resources, config, remote_agent, purchaser_account):
    test_data = secrets.token_hex(1024)
    asset_data = DataAsset.create('TestAsset', test_data)
    asset = remote_agent.register_asset(asset_data)
    assert(asset)
    listing = remote_agent.create_listing(resources.listing_data, asset.did)
    listing.set_published(True)
    logging.debug("create_purchase for listing_id: " + listing.listing_id)
    purchase = remote_agent.purchase_asset(listing, purchaser_account)
    assert(purchase['listingid'] == listing.listing_id)
    assert(purchase['status'] == 'wishlist')
    logging.debug("purchase: " + json.dumps(purchase))
