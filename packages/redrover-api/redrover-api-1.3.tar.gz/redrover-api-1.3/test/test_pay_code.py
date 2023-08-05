# coding: utf-8

"""
    Red Rover API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v1
    Contact: contact@edustaff.org
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import redrover_api
from redrover_api.models.pay_code import PayCode  # noqa: E501
from redrover_api.rest import ApiException

class TestPayCode(unittest.TestCase):
    """PayCode unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PayCode
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = redrover_api.models.pay_code.PayCode()  # noqa: E501
        if include_optional :
            return PayCode(
                id = 56, 
                code = '0', 
                name = '0'
            )
        else :
            return PayCode(
        )

    def testPayCode(self):
        """Test PayCode"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
