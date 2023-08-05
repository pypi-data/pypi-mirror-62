import os
import random
from typing import List

import pytest

from verifiable_credentials.components import Issuer, Assertion, Recipient, EthereumAnchorHandler


@pytest.fixture
def issuer() -> Issuer:
    yield Issuer(
        name='Chalmers University of Technology',
        id='https://gist.githubusercontent.com/faustow/98db76b26b4d297d0eb98d499e733f77/raw/71f034f76d50fbe8656d6843d72ba1ed42581837/vc_issuer.json',
        email='info@chalmers.se',
        image='',
        revocation_list='https://gist.githubusercontent.com/faustow/07a66855d713409067ff28e10778e2dd/raw/e08bb6d6f1350367d3f6d4f805ab3b1466b584d7/revocation-list-testnet.json',
        public_key=os.environ.get('PUBLIC_KEY'),
        main_url='https://www.dock.io',
        signature_name='Napoleon Dynamite',
        signature_job_title='President',
        signature_image='',
    )


@pytest.fixture
def assertion() -> Assertion:
    yield Assertion(
        id='2345678901',
        name='Automation and Mechatronics Engineer',
        description='https://www.pluggaz.se/',
        image='',
        narrative='Candidates must be smart.',
    )


@pytest.fixture
def recipients() -> List[Recipient]:
    yield [
        Recipient(
            name='Fausto Woelflin',
            email='fausto@dock.io',
            public_key='3456789012',
        ),
        Recipient(
            name='Eddie Vedder',
            email='ed@pearljam.net',
            public_key='4567890123',
        ),
        Recipient(
            name='Thomas Shellby',
            email='tom@shellbylimited.com',
            public_key='5678901234',
        ),
    ]


@pytest.fixture
def eth_anchor_handler() -> EthereumAnchorHandler:
    eth_account = random.choice(_get_eth_accounts())
    yield EthereumAnchorHandler(
        node_url=os.environ.get('ETH_NODE_URL'),
        public_key=eth_account.get('public'),
        private_key=eth_account.get('private'),
        key_created_at='2019-03-26T23:37:07.464654+00:00',
    )


def _get_eth_accounts() -> List:
    return [
        dict(
            public=os.environ.get('PUBLIC_KEY'),
            private=os.environ.get('PRIVATE_KEY')
        ),
        dict(
            public=os.environ.get('PUBLIC_KEY_2'),
            private=os.environ.get('PRIVATE_KEY_2')
        ),
        dict(
            public=os.environ.get('PUBLIC_KEY_3'),
            private=os.environ.get('PRIVATE_KEY_3')
        )
    ]
