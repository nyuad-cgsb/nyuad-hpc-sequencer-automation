import unittest
import tempfile

from tar_run_folder import generate_tar_command


class TestTarRunCommandIsCorrect(unittest.TestCase):
    def test(self):
        work_dir = '/work/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX/'
        command = generate_tar_command(work_dir)
        expected_command = 'cd /work/gencore/novaseq && tar -cvf 180710_A00534_0022_AHFY3KDMXX.tar ' + \
                           '/work/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX && ' + \
                           'md5sum 180710_A00534_0022_AHFY3KDMXX.tar > 180710_A00534_0022_AHFY3KDMXX.md5sum'
        self.assertEqual(command, expected_command)


if __name__ == '__main__':
    unittest.main()
