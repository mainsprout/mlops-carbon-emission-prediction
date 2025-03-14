import unittest


class TestTrafficModelCd(unittest.TestCase):
    def test_get_next_branch(self):
        import models.traffic_model_cd.traffic_model_cd as model
        next_branch = model.get_next_branch()
        print(f"next_branch = {next_branch}")


if __name__ == '__main__':
    unittest.main()