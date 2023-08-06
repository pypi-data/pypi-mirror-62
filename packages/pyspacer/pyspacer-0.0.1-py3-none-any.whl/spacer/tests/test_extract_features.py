import json
import unittest
import warnings

from PIL import Image

from spacer import config
from spacer.extract_features import feature_extractor_factory
from spacer.messages import \
    ExtractFeaturesMsg, \
    ExtractFeaturesReturnMsg
from spacer.data_classes import ImageFeatures
from spacer.storage import storage_factory


class TestDummyExtractor(unittest.TestCase):

    def test_simple(self):
        msg = ExtractFeaturesMsg(
            pk=1,
            feature_extractor_name='dummy',
            bucketname='spacer-test',
            storage_type='memory',
            imkey='not_used',
            rowcols=[(100, 100)],
            outputkey='not_used'
        )

        ext = feature_extractor_factory(msg.feature_extractor_name,
                                        dummy_featuredim=4096)

        features, return_msg = ext(Image.new('RGB', (100, 100)), msg.rowcols)

        self.assertTrue(isinstance(return_msg, ExtractFeaturesReturnMsg))
        self.assertTrue(isinstance(features, ImageFeatures))

        # Check some feature metadata
        self.assertEqual(features.point_features[0].row, 100)
        self.assertEqual(features.point_features[0].col, 100)

    def test_dims(self):

        feature_dim = 42
        ext = feature_extractor_factory('dummy',
                                        dummy_featuredim=feature_dim)
        self.assertEqual(ext.feature_dim, feature_dim)


class TestCaffeExtractor(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)

    @unittest.skipUnless(config.HAS_CAFFE, 'Caffe not installed')
    @unittest.skipUnless(config.HAS_S3_TEST_ACCESS, 'No access to tests')
    @unittest.skipUnless(config.HAS_S3_MODEL_ACCESS, 'No access to models')
    def test_simple(self):

        msg = ExtractFeaturesMsg(
            pk=1,
            feature_extractor_name='vgg16_coralnet_ver1',
            bucketname='spacer-test',
            storage_type='s3',
            imkey='edinburgh3.jpg',
            rowcols=[(100, 100)],
            outputkey='dummy',
        )

        storage = storage_factory(msg.storage_type, msg.bucketname)
        ext = feature_extractor_factory(msg.feature_extractor_name)

        features, return_msg = ext(storage.load_image(msg.imkey),
                                   msg.rowcols)

        self.assertTrue(isinstance(return_msg, ExtractFeaturesReturnMsg))
        self.assertTrue(isinstance(features, ImageFeatures))

        # Check some feature metadata
        self.assertEqual(features.point_features[0].row, 100)
        self.assertEqual(features.point_features[0].col, 100)

    @unittest.skipUnless(config.HAS_CAFFE, 'Caffe not installed')
    @unittest.skipUnless(config.HAS_S3_MODEL_ACCESS, 'No access to models')
    def test_dims(self):
        ext = feature_extractor_factory('vgg16_coralnet_ver1')
        self.assertEqual(ext.feature_dim, 4096)

    @unittest.skipUnless(config.HAS_CAFFE, 'Caffe not installed')
    @unittest.skipUnless(config.HAS_S3_TEST_ACCESS, 'No access to test bucket')
    @unittest.skipUnless(config.HAS_S3_MODEL_ACCESS, 'No access to models')
    def test_corner_case1(self):
        """
        This particular image caused trouble on the production server.
        The image file itself is lightly corrupted, and PIL doesn't like it.
        """

        msg = ExtractFeaturesMsg(
            pk=1,
            feature_extractor_name='vgg16_coralnet_ver1',
            bucketname='spacer-test',
            storage_type='s3',
            imkey='kh6dydiix0.jpeg',
            rowcols=[(148, 50), (60, 425)],
            outputkey='dummy',
        )

        storage = storage_factory(msg.storage_type, msg.bucketname)
        ext = feature_extractor_factory(msg.feature_extractor_name)

        features, return_msg = ext(storage.load_image(msg.imkey),
                                   msg.rowcols)

        self.assertTrue(isinstance(return_msg, ExtractFeaturesReturnMsg))
        self.assertTrue(isinstance(features, ImageFeatures))

        # Check some feature metadata
        self.assertEqual(features.point_features[0].row, 148)
        self.assertEqual(features.point_features[0].col, 50)

    @unittest.skipUnless(config.HAS_CAFFE, 'Caffe not installed')
    @unittest.skipUnless(config.HAS_S3_TEST_ACCESS, 'No access to test bucket')
    @unittest.skipUnless(config.HAS_S3_MODEL_ACCESS, 'No access to models')
    def test_cornercase2(self):
        """
        This particular image caused trouble on the production server.
        The image file itself is lightly corrupted, and PIL doesn't
        quite like it.
        """
        msg = ExtractFeaturesMsg(
            pk=1,
            feature_extractor_name='vgg16_coralnet_ver1',
            bucketname='spacer-test',
            storage_type='s3',
            imkey='sfq2mr5qbs.jpeg',
            rowcols=[(190, 226), (25, 359)],
            outputkey='dummy'
        )
        storage = storage_factory(msg.storage_type, msg.bucketname)
        ext = feature_extractor_factory(msg.feature_extractor_name)

        features, return_msg = ext(storage.load_image(msg.imkey),
                                   msg.rowcols)

        self.assertTrue(isinstance(return_msg, ExtractFeaturesReturnMsg))
        self.assertTrue(isinstance(features, ImageFeatures))

        # Check some feature metadata
        self.assertEqual(features.point_features[0].row, 190)
        self.assertEqual(features.point_features[0].col, 226)

    @unittest.skipUnless(config.HAS_CAFFE, 'Caffe not installed')
    @unittest.skipUnless(config.HAS_S3_TEST_ACCESS, 'No access to test bucket')
    @unittest.skipUnless(config.HAS_S3_MODEL_ACCESS, 'No access to models')
    def test_regression(self):
        """
        This tests run the extractor on a known image and compares the
        results to the features extracted with the
        https://github.com/beijbom/ecs_spacer/releases/tag/1.0
        """
        rowcols = [(20, 265),
                   (76, 295),
                   (59, 274),
                   (151, 62),
                   (265, 234)]

        msg = ExtractFeaturesMsg(
            pk=1,
            feature_extractor_name='vgg16_coralnet_ver1',
            bucketname='spacer-test',
            storage_type='s3',
            imkey='08bfc10v7t.png',
            rowcols=rowcols,
            outputkey='na'
        )
        storage = storage_factory(msg.storage_type, msg.bucketname)
        ext = feature_extractor_factory(msg.feature_extractor_name)

        features_new, _ = ext(storage.load_image(msg.imkey), msg.rowcols)

        features_legacy = ImageFeatures.deserialize(json.loads(
            storage.load_string('08bfc10v7t.png.featurevector')))

        for pf_new, pf_legacy in zip(features_new.point_features,
                                     features_legacy.point_features):
            self.assertEqual(pf_new.data, pf_legacy.data)
            self.assertTrue(pf_legacy.row is None)
            self.assertTrue(pf_new.row is not None)


if __name__ == '__main__':
    unittest.main()
