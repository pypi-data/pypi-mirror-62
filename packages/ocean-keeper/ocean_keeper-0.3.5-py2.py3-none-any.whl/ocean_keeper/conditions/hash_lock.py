#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0

from ocean_keeper.conditions.condition_base import ConditionBase


class HashLockCondition(ConditionBase):
    """Class representing the HashLockCondition contract."""
    CONTRACT_NAME = 'HashLockCondition'

    def fulfill(self, agreement_id, preimage, account):
        """

        :param agreement_id: id of the agreement, hex str
        :param preimage:
        :param account: Account instance
        :return:
        """
        return self._fulfill(
            agreement_id,
            preimage,
            transact={'from': account.address,
                      'passphrase': account.password,
                      'account_key': account.key}
        )

    def hash_values(self, preimage):
        """
        Hash the values of the hash lock condition.

        :param preimage:
        :return:
        """
        return self._hash_values(preimage)
