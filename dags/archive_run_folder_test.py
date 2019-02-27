import unittest

from archive_run_folder import generate_archive_work_dir_command


class TestArchiveCommand(unittest.TestCase):
    def test(self):
        work_dir = '/work/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX/'
        command = generate_archive_work_dir_command(work_dir)
        expected_command = 'rsync -av --checksum ' + \
                           '/work/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX.tar /archive/gencore/novaseq/raw/'
        self.assertEqual(command, expected_command)
