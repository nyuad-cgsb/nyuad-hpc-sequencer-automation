import unittest

from archive_run_folder import generate_archive_scratch_dir_command


class TestArchiveCommand(unittest.TestCase):
    def test(self):
        """
        Work dirs are always directories, even if they have a trailing '/', and should be accounted for.
        :return:
        """
        scratch_dir = '/scratch/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX/'
        command = generate_archive_scratch_dir_command(scratch_dir)
        expected_command = 'ssh gencore@archive3 "rsync -av --checksum  /scratch/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX /archive/gencore/novaseq/raw/"'
        self.assertEqual(command, expected_command)


if __name__ == '__main__':
    unittest.main()
