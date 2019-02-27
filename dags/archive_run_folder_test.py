import unittest

from archive_run_folder import generate_archive_work_dir_command


class TestArchiveCommand(unittest.TestCase):
    def test(self):
        """
        Work dirs are always directories, even if they have a trailing '/', and should be accounted for.
        :return:
        """
        work_dir = '/work/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX/'
        command = generate_archive_work_dir_command(work_dir)
        # expected_command = 'rsync -av --checksum ' + \
        #                    '/work/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX.tar /archive/gencore/novaseq/raw/'
        expected_command = 'ssh gencore@archive3 rsync -av --checksum /work/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX.tar /archive/gencore/novaseq/raw/'
        self.assertEqual(command, expected_command)


if __name__ == '__main__':
    unittest.main()
