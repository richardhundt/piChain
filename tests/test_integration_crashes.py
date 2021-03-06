"""Integration test: Test crash and recovery behavior of piChain nodes.

Note: run tests with default setting values in config.py.
"""

import time

from tests.util import MultiNodeTest


class MultiNodeTestCrashes(MultiNodeTest):

    def test_scenario20_crash(self):
        self.start_processes_with_test_scenario(20, 3)
        time.sleep(3)
        self.terminate_single_process(1)
        node1_blocks_before = self.extract_committed_blocks_single_process(1)
        self.start_single_process_with_test_scenario(20, 1, 3)
        time.sleep(10)
        self.terminate_processes()

        node0_blocks = self.extract_committed_blocks_single_process(0)
        node1_blocks_after = self.extract_committed_blocks_single_process(1)
        node2_blocks = self.extract_committed_blocks_single_process(2)

        node1_blocks = node1_blocks_before + node1_blocks_after

        assert len(node0_blocks) > 0
        assert node0_blocks == node1_blocks
        assert node2_blocks == node1_blocks

    def test_scenario21_crash(self):
        self.start_processes_with_test_scenario(21, 3)
        time.sleep(3)
        self.terminate_single_process(0)
        node0_blocks_before = self.extract_committed_blocks_single_process(0)
        self.start_single_process_with_test_scenario(21, 0, 3)
        time.sleep(10)
        self.terminate_processes()

        node0_blocks_after = self.extract_committed_blocks_single_process(0)
        node1_blocks = self.extract_committed_blocks_single_process(1)
        node2_blocks = self.extract_committed_blocks_single_process(2)

        node0_blocks = node0_blocks_before + node0_blocks_after

        assert len(node0_blocks) > 0
        assert node0_blocks == node1_blocks
        assert node2_blocks == node1_blocks
